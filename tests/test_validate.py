"""Mutation tests of the checker, not skill-answer tests."""
from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))

    def errors(self):
        return "\n".join(validate(self.root)[0])

    def mutate_cases(self, change):
        p = self.root / "evals/cases.yaml"
        doc = yaml.safe_load(p.read_text())
        change(doc)
        p.write_text(yaml.safe_dump(doc, allow_unicode=True))

    def test_valid_repository(self):
        self.assertEqual(self.errors(), "")

    def test_missing_file(self):
        (self.root / "agents/blind-review.md").unlink()
        self.assertIn("missing file", self.errors())

    def test_broken_link(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n[bad](not-present.md)\n")
        self.assertIn("broken/local escaping link", self.errors())

    def test_duplicate_case_id(self):
        self.mutate_cases(lambda d: d["cases"].append(d["cases"][0]))
        self.assertIn("duplicate case id", self.errors())

    def test_missing_counterexample(self):
        self.mutate_cases(lambda d: d.update(cases=[c for c in d["cases"] if "retry" not in c["tags"]]))
        self.assertIn("missing regression tags", self.errors())

    def test_invalid_mode(self):
        self.mutate_cases(lambda d: d["cases"][0].update(expected_mode="unknown"))
        self.assertIn("invalid mode", self.errors())

    def test_empty_criteria(self):
        self.mutate_cases(lambda d: d["cases"][0].update(forbidden=[]))
        self.assertIn("invalid forbidden", self.errors())

    def test_contradictory_criteria(self):
        self.mutate_cases(lambda d: d["cases"][0]["forbidden"].append(d["cases"][0]["required"][0]))
        self.assertIn("contradictory exact criteria", self.errors())

    def test_duplicate_yaml_key(self):
        with (self.root / "agents/openai.yaml").open("a") as f:
            f.write("\ninterface: {}\n")
        self.assertIn("duplicate YAML key", self.errors())

    def test_missing_frontmatter(self):
        (self.root / "SKILL.md").write_text("# Skill without metadata\n")
        self.assertIn("missing skill frontmatter", self.errors())

    def test_private_path_pattern(self):
        synthetic = "/" + "Users" + "/fictional-test/example"
        (self.root / "fixture.txt").write_text(synthetic)
        self.assertIn("privacy pattern", self.errors())

    def test_symlink(self):
        (self.root / "linked.md").symlink_to("SKILL.md")
        self.assertIn("symlink not allowed", self.errors())

    def test_snapshot_review_mismatch(self):
        p = self.root / "references/research-snapshot.json"
        records = json.loads(p.read_text())
        records[0]["stars"] += 1
        p.write_text(json.dumps(records))
        self.assertIn("source snapshot/review mismatch", self.errors())

    def test_invalid_yaml(self):
        (self.root / "agents/openai.yaml").write_text("interface: [unterminated")
        self.assertIn("YAML error", self.errors())

    def test_unpinned_source(self):
        p = self.root / "references/research-snapshot.json"
        records = json.loads(p.read_text())
        records[0]["commit"] = "main"
        p.write_text(json.dumps(records))
        self.assertIn("source commit not pinned", self.errors())


if __name__ == "__main__":
    unittest.main()
