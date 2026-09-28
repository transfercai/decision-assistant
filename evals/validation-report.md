# Local validation record · 2026-09-28 (UTC)

Baseline: public commit `1afe6506eace0013d483ce772d2e42d2fbdb4598`.
Candidate: the commit containing this report on `improve/decision-evidence-and-portability` (use the branch's full SHA when reproducing).
Environment: Python 3.12.14, PyYAML 6.0.3. No extra model, subagent, Council or hosted evaluation was invoked.

## Actual deterministic results

| Command | Result |
|---|---|
| `python3 scripts/validate.py` | PASS; 18 text files, 3 YAML documents including skill frontmatter, 19 local inline links, 35 case schemas, 4 research sources; 0 errors |
| `python3 -m unittest discover -s tests -v` | 15 tests passed, including deliberately corrupted temporary copies |
| `python3 -W error -m compileall -q scripts tests` | Passed; no syntax warnings/errors |
| `git diff --check` and `git diff --cached --check` | Passed; no whitespace errors |

Mutation coverage: missing file, broken link, duplicate case ID, missing required counterexample, invalid mode, empty/contradictory criteria, duplicate/invalid YAML, absent frontmatter, synthetic home-path leak, symlink, unpinned source and inconsistent source count/documentation. The valid-repository test covers the happy path. Earlier development found a Python escape-sequence warning and a trailing blank line in a new notice file; both were corrected before the final checks.

## Manual review performed

- Read baseline skill, domain references, review template and evaluation criteria; checked the revised text for generic likelihood-ratio removal, price/total-return correction, proportionate risk gates, deadline exceptions, provenance labels and honest standalone fallback.
- Read public candidate core files and available MIT licenses at fixed commits; distinguished three skill collections from the Council application with unspecified licensing.
- Checked examples for fictional names and removal of personal identifiers; no real production logs, personal records or private-repository references were added. Checked this change's content, not every historical commit.

## Not verified

The 35 prompts were **not** executed against a language model. There is no behavioral pass rate, A/B win rate, independent blind review or empirical quality improvement claim. No integration run across different Agent Skills hosts was performed. The link checker checks local inline targets only, not Markdown anchors or live external URLs; source URLs were fetched during research. Privacy regexes are limited and do not prove absence of every secret or inferential identifier. Commit history was not rewritten or certified sanitized.
