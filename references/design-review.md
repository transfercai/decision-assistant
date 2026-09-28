# Public-source design review · 2026-09-28 (UTC)

Stars are a dated repository-level popularity signal, not usage of one skill, evidence of safety, or a quality benchmark. Read the actual files at pinned commits below. Scope: three skill collections and one related application; do not present all four as standalone decision skills. No candidate was installed or run, and no model-quality comparison was performed.

Counts, collection timestamps, commits and GitHub-detected licenses are in [research-snapshot.json](research-snapshot.json). Metadata came from public GitHub REST `GET /repos/{owner}/{repo}`, commit and recursive-tree endpoints; core files and available LICENSE files were read at the pinned commit. These are our recorded observations, not an independently archived API response. Stars will change.

## tjboudreaux/cc-thinking-skills — 1,333 stars

- Commit: `7b8fece345dfaa11773be7152ccd194589cb5437`
- Captured: `2026-09-28T07:12:44.386471+00:00`
- License: [MIT](https://github.com/tjboudreaux/cc-thinking-skills/blob/7b8fece345dfaa11773be7152ccd194589cb5437/LICENSE), checked against the file.
- Type: mental-model Agent Skills collection, closest fit despite fewer stars.
- Core evidence: [reversibility](https://github.com/tjboudreaux/cc-thinking-skills/blob/7b8fece345dfaa11773be7152ccd194589cb5437/skills/thinking-reversibility/SKILL.md) says “match process depth to undo cost”; [pre-mortem](https://github.com/tjboudreaux/cc-thinking-skills/blob/7b8fece345dfaa11773be7152ccd194589cb5437/skills/thinking-pre-mortem/SKILL.md) binds owner, checkpoint and ship/stage gate; [steel-manning](https://github.com/tjboudreaux/cc-thinking-skills/blob/7b8fece345dfaa11773be7152ccd194589cb5437/skills/thinking-steel-manning/SKILL.md) requires an overturn observation and an updated decision; [second-order](https://github.com/tjboudreaux/cc-thinking-skills/blob/7b8fece345dfaa11773be7152ccd194589cb5437/skills/thinking-second-order/SKILL.md) stops chains that no longer affect the decision.
- Adopt: concrete undo path plus waiting cost; risk-proportionate analysis; failure causes converted to verifiable changes; counterarguments with reversal conditions; mechanism-based downstream effects and stop rules.
- Do not adopt: a fixed number of consequence orders, generic probability scores, or mandatory separate skill calls. Do not use security red-team as a general decision ritual. Upstream evaluation artifacts are author-maintained, not independent proof that this adaptation works.
- Local changes: SKILL pipeline 1/4/6; engineering reference; reversible-configuration and retry cases.

## obra/superpowers — 292,257 stars

- Commit: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`
- Captured: `2026-09-28T07:12:44.246039+00:00`
- License: [MIT](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/LICENSE), checked against the file.
- Type: software-development workflow collection; brainstorming is relevant to clarifying decisions, not a universal life-decision assistant.
- Core evidence: [brainstorming](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/SKILL.md), “Separate what they said from assumptions.” The file distinguishes spike, bounded and architectural paths, asks focused questions, and requires explicit approval before implementation.
- Adopt: separate stated constraints from assumptions, ask the question that matters, scale process to the task, and distinguish recommendation from execution authority.
- Do not adopt: compulsory design documents, repeated implementation gates for ordinary advice, visual server, or automatic transition to other skills. Preserve authorization checks for actual external actions.
- Local changes: evidence labels; standalone section; light/full output; goal-clarification and self-report cases.

## alirezarezvani/claude-skills — 26,682 stars

- Commit: `19392f7a08264ed00486a251f5b2098321771f94`
- Captured: `2026-09-28T07:12:45.547389+00:00`
- License: [MIT](https://github.com/alirezarezvani/claude-skills/blob/19392f7a08264ed00486a251f5b2098321771f94/LICENSE), checked against the file.
- Type: broad professional-skills collection; decision-logger is the examined decision-specific component.
- Core evidence: [decision-logger](https://github.com/alirezarezvani/claude-skills/blob/19392f7a08264ed00486a251f5b2098321771f94/c-level-advisor/skills/decision-logger/SKILL.md), “Layer 2 stores only what the founder approved.” Its entry has owner, deadline, review, rationale and supersession fields; it also auto-loads approved decisions and blocks rejected topics until reopened.
- Adopt: distinguish proposed from user-approved decisions; actionable ownership/review and evidence-based updates.
- Do not adopt: automatic raw-transcript storage, board-agent choreography, auto-loaded personal memory, or a rejection lock that overrides new evidence. Logging here is opt-in and minimal.
- Local changes: privacy boundary and practice contract; no-auto-log case. The broader CEO framework was inspected as context, not imported as a scoring system.

## karpathy/llm-council — 25,036 stars

- Commit: `92e1fccb1bdcf1bab7221aa9ed90f9dc72529131`
- Captured: `2026-09-28T07:12:43.828021+00:00`
- License: GitHub API returned `null`; the inspected tree contains no license file. Treat reuse rights as unspecified; no code or prompt text copied.
- Type: multi-model web application, **not an Agent Skill**.
- Core evidence: [README](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/README.md) and [backend/council.py](https://github.com/karpathy/llm-council/blob/92e1fccb1bdcf1bab7221aa9ed90f9dc72529131/backend/council.py) describe/implement individual answers, anonymized peer rankings, and chairman synthesis via remote model calls.
- Useful distinction: hiding a recommendation or model name does not create independent factual evidence.
- Reject as a dependency: additional API cost, latency, external data sharing, and vote/ranking authority are not justified for ordinary decisions. No installation, API call, code reuse, or Council command added. It is a comparison/counterexample, not an adopted architecture.
- Local changes: optional review only, truthful self-review fallback, and no confidence increase from correlated agreement.

## Scope, attribution and limits

Wording and local implementations are original except the three short attributed quotations above. MIT notices for quoted sources are preserved in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Public URLs, pinned commits and repository-level counts identify inspiration, not endorsement. No private repository, user incident, financial record, or production log is source material for the examples.

The investment, urgency and uncertainty corrections are this project's own design judgments. Structural validation cannot establish that they improve model decisions. See [evaluation protocol](../evals/README.md) for a controlled behavioral comparison still to be run.
