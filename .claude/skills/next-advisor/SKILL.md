---
name: next-advisor
description: Diagnoses the initiative state and recommends the 1-3 most valuable next actions. Use when the PM says "what's next", "что дальше", "continue", "где мы", "продолжаем", "what should I do", or seems unsure where to go — instead of mechanically suggesting the next pipeline step number.
---

# Next Advisor — `/next`

Recommend the most valuable next action from **state**, not from step
numbers. "You are on step 6, next is step 7" is exactly what this skill
replaces.

## Inputs (read all that exist)

1. `output/hypotheses.json` — the registry (or `hypotheses.py show <dir>`)
2. `python3 tools/scripts/validate-evidence.py <dir>` — violations
3. `python3 tools/scripts/coverage.py <dir>` — phase map + focus
4. `output/status.json` — `dependencies[]` (ages, deadlines, blocks; legacy
   `pending.*` values count too) and `steps` statuses
4. Last 2-3 entries of `output/decisions.md` — what was promised last time
5. `CONTEXT.md` — is there a target? kill criteria?

## Diagnosis order (first match wins the top slot; report up to 3)

1. **Stalled external dependency** — an entry in `dependencies[]` past its
   deadline (or a legacy pending older than 7 days) → recommend: chase the
   owner / move the deadline / switch to synthetic (downgrading dependent
   hypotheses) / consciously skip (`status: "skipped"`). Name the blocked
   hypotheses from `blocks`.
2. **Evidence violations** — flagged `data_inconsistency` held above 0.6,
   confidence outside type range → recommend reconciling before anything
   built on those numbers (especially before a gate).
3. **Ready-but-unstarted work** — e.g. ≥2 hypotheses confirmed REAL and
   `/solutions` not run; solutions scored and `/sketch` empty; deck ready
   and gate not rehearsed → recommend the job that converts existing
   evidence into progress.
4. **Frame gaps that now matter** — no target/kill criteria AND a gate is
   near → recommend `/setup-initiative` (this is the only moment to push it).
5. **Open hypotheses without a validation path** — testing/draft hypotheses
   that no brief or dependency covers → recommend `/brief` or `/ingest`.

## Output format

Short. For each recommendation: **what → why now → one command/action to
start**. Reference hypothesis ids and real dates/ages. No generic advice
("keep validating") — every line must be executable today. If everything is
genuinely blocked on external people, say exactly that and list who owes
what since when.
