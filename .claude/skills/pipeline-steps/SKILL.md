---
name: pipeline-steps
description: Map of pipeline steps (0-19) and jobs with registry rules; detailed per-step instructions live in references/steps.md. Read this whenever the PM calls a pipeline command (/analyze-cjm, /validate-problems, …) or a job, then read the matching section of references/steps.md.
---

# Pipeline Step Instructions

Navigation layer: jobs map + registry rules here, per-step details in
`references/steps.md` (read only the section you are executing).

**Jobs → steps.** Jobs are the primary interface (CLAUDE.md → JOBS CATALOG):
`/hypotheses` → steps 1–2 · `/brief` → 4/5/11 · `/validate` → 6 ·
`/solutions` → 7 · `/sketch` → 8 · `/tickets` → create-tickets ·
`/ingest` → skill `ingest` · `/next` → skill `next-advisor`.
Every job runs standalone: no initiative → work on chat context, type
evidence INFERRED, offer to persist afterwards; initiative exists → read and
write its registry and artifacts as described per step.

**Hypothesis registry (all steps).** Hypothesis STATE (status, evidence type,
confidence, sources, history) lives in `output/hypotheses.json` — manage it via
`python3 tools/scripts/hypotheses.py` (`add` / `set` / `validate` / `render`).
`set` records history automatically. Narrative markdown (hypotheses.md,
validated-hypotheses.md) stays authored prose and must not contradict the
registry. After changing the registry run `hypotheses.py render <dir>` to
refresh `output/registry.md`. Legacy initiatives: convert once with
`python3 tools/scripts/migrate-hypotheses.py <dir>`.

---

## Step index

Details for every step live in `references/steps.md` — **read the section
for the step you are executing** (table of contents at the top; don't load
other steps, they aren't needed).

| # | Command | Type | Note |
|---|---------|------|------|
| 0 | `/setup-initiative` | Core | |
| 1 | `/analyze-cjm` | Core | |
| 2 | `/synthetic-research` | Recommended | |
| 3 | `/competitor-research` | Recommended | |
| 4 | `/generate-research` | Recommended | |
| 5 | `/create-survey-audience` | Optional | |
| 6 | `/validate-problems` | Core | |
| 7 | `/solution-hypotheses` | Core | |
| 8 | `/sketch-solution` | Core | |
| 8.5 | `/user-test-concept` | Optional; alias for user-testing concept mode | |
| 9 | `/review-design` | Recommended | |
| 10 | `/create-presentation` | Core |Problem Research Report |
| 11 | `/create-design-brief` | Recommended | |
| 12 | `/estimate-with-dev` | Core | |
| 13 | `/finalize-prd` | Core | |
| 14 | `/design-ab-test` | Recommended | |
| 15 | `/create-gate2-presentation` | Core |Solution Research Report |
| — | `/create-tickets` | after Gate 2 | push to tracker via MCP |
| 16 | `/analyze-ab-test` | Recommended | |
| 17 | `/plan-gtm` | Core | |
| 18 | `/create-gtm-materials` | Optional | |
| 19 | `/support-task` | Optional | |

Gates (steps 10, 15) have machine preconditions — `validate-evidence.py
--gate` must be CLEAR before assembling a deck; offer `/challenge` to
rehearse. External handoffs (steps 4, 5, 11, 12, 14, 16, 18, 19) create
`dependencies[]` entries with owner + deadline.
