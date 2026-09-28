#!/usr/bin/env python3
"""Deterministic repository checks, not a model-behavior evaluator."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml

REQUIRED_TAGS = {
    "proportional_health", "urgent_safety", "deadline", "no_fake_lr", "provenance",
    "offline", "standalone", "dividend", "valuation", "release", "config", "retry",
    "rollback", "irreversible_data", "delay_cost", "privacy",
}
REQUIRED_FILES = {
    "SKILL.md", "README.md", "LICENSE", "agents/openai.yaml", "agents/blind-review.md",
    "evals/cases.yaml", "evals/README.md", "references/investment-decisions.md",
    "references/work-decisions.md", "references/engineering-decisions.md",
    "references/design-review.md", "references/research-snapshot.json",
    "THIRD_PARTY_NOTICES.md",
}
SKIP_DIRS = {".git", ".venv", "__pycache__"}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys that ordinary safe_load silently overwrites."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def validate(root: Path) -> tuple[list[str], dict]:
    root = root.resolve()
    errors: list[str] = []
    stats = {"files": 0, "yaml_documents": 0, "local_links": 0, "cases": 0, "sources": 0}
    for name in sorted(REQUIRED_FILES):
        if not (root / name).is_file():
            errors.append(f"missing file: {name}")
    parsed = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(f"symlink not allowed: {relative}")
            continue
        if not path.is_file():
            continue
        stats["files"] += 1
        text = path.read_text(encoding="utf-8")
        # Deliberately limited patterns. This is not a full secret/history scanner.
        patterns = {
            "home path": r"/(?:Users|home)/[A-Za-z0-9_.-]+",
            "private key": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
            "credential": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
            "personal email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                errors.append(f"privacy pattern ({label}): {relative}")
        if path.suffix in {".yaml", ".yml"}:
            try:
                parsed[str(relative)] = yaml.load(text, Loader=UniqueLoader)
                stats["yaml_documents"] += 1
            except (yaml.YAMLError, ValueError, TypeError) as exc:
                errors.append(f"YAML error {relative}: {exc}")
        if path.name == "SKILL.md":
            match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
            if not match:
                errors.append("missing skill frontmatter")
            else:
                try:
                    meta = yaml.load(match.group(1), Loader=UniqueLoader)
                    if not isinstance(meta, dict) or set(meta) != {"name", "description"}:
                        raise ValueError("expected name and description only")
                    if meta["name"] != "decision-assistant" or not isinstance(meta["description"], str) or not meta["description"].strip():
                        raise ValueError("invalid skill metadata")
                    stats["yaml_documents"] += 1
                except (yaml.YAMLError, ValueError, TypeError) as exc:
                    errors.append(f"frontmatter: {exc}")
        if path.suffix == ".md":
            # Inline Markdown targets only; external URLs and heading anchors are not fetched.
            for target in re.findall(r"\]\(([^\s)]+)\)", text):
                if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                dest = (path.parent / unquote(target.split("#")[0])).resolve()
                stats["local_links"] += 1
                if not dest.is_relative_to(root) or not dest.exists():
                    errors.append(f"broken/local escaping link: {relative} -> {target}")
    cases = parsed.get("evals/cases.yaml")
    if not isinstance(cases, dict) or cases.get("version") != 2 or not isinstance(cases.get("cases"), list):
        errors.append("invalid cases schema/version")
    else:
        ids, tags = set(), set()
        for case in cases["cases"]:
            if not isinstance(case, dict):
                errors.append("case must be a mapping")
                continue
            cid = case.get("id")
            if not isinstance(cid, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", cid):
                errors.append("invalid case id")
            elif cid in ids:
                errors.append(f"duplicate case id: {cid}")
            else:
                ids.add(cid)
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"missing prompt: {cid}")
            if case.get("expected_mode") not in {"light", "full", "urgent", "crisis"}:
                errors.append(f"invalid mode: {cid}")
            for field in ("required", "forbidden", "tags"):
                values = case.get(field)
                if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
                    errors.append(f"invalid {field}: {cid}")
                elif field == "tags":
                    tags.update(values)
            if isinstance(case.get("required"), list) and isinstance(case.get("forbidden"), list):
                if any(v in case["forbidden"] for v in case["required"]):
                    errors.append(f"contradictory exact criteria: {cid}")
        missing = REQUIRED_TAGS - tags
        if missing:
            errors.append(f"missing regression tags: {sorted(missing)}")
        scoring = cases.get("scoring", {})
        if not isinstance(scoring, dict) or not scoring.get("dimensions") or not scoring.get("hard_failures"):
            errors.append("missing scoring rubric")
        stats["cases"] = len(cases["cases"])
    metadata = parsed.get("agents/openai.yaml")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("interface"), dict):
        errors.append("invalid agent interface metadata")
    else:
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(metadata["interface"].get(field), str) or not metadata["interface"][field].strip():
                errors.append(f"missing agent interface {field}")
    try:
        records = json.loads((root / "references/research-snapshot.json").read_text())
        if not isinstance(records, list) or not 3 <= len(records) <= 5:
            raise ValueError("expected 3–5 public candidates")
        seen = set()
        review = (root / "references/design-review.md").read_text()
        for record in records:
            if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", record["repo"]) or record["repo"] in seen:
                raise ValueError("invalid/duplicate source repository")
            seen.add(record["repo"])
            if not re.fullmatch(r"[a-f0-9]{40}", record["commit"]):
                raise ValueError("source commit not pinned")
            if type(record["stars"]) is not int or record["stars"] < 0:
                raise ValueError("invalid stars")
            if datetime.fromisoformat(record["collected_at"]).tzinfo is None:
                raise ValueError("collection timestamp needs timezone")
            if (record["commit"] not in review or record["collected_at"] not in review
                    or f"{record['repo']} — {record['stars']:,} stars" not in review):
                raise ValueError("source snapshot/review mismatch")
            if record["license"] not in {"MIT", None}:
                raise ValueError("unexpected license: re-review needed")
        stats["sources"] = len(records)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"research snapshot: {exc}")
    return errors, stats


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    errors, stats = validate(root)
    print(json.dumps({"status": "FAIL" if errors else "PASS", **stats, "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(bool(errors))
