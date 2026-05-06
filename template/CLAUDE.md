# Product Discovery — Initiative Context

<!-- This CLAUDE.md is copied into each initiative folder. It loads on demand when Claude reads initiative files. -->

## This initiative

Read `CONTEXT.md` for initiative details: metric, segment, baseline, target, constraints, stakeholders.

## Session workflow

1. Read `output/status.json` → current step, pending tasks, pipeline_config
2. Read last 3 entries from `output/decisions.md` → restore context
3. Suggest next step (skip disabled steps in pipeline_config)

## After each step

1. Update `output/status.json` — step status + 1-2 sentence summary
2. Append to `output/decisions.md` — what we did, decisions, open questions, next step
3. Git commit + push

## Pipeline steps

For detailed step instructions, read `.claude/skills/pipeline-steps/SKILL.md` at repo root.

Quick reference:

| # | Command | Type | Output |
|---|---------|------|--------|
| 0 | `/setup-initiative` | Core | CONTEXT.md, pipeline_config |
| 1 | `/analyze-cjm` | Core | output/hypotheses.md, PRD §1-2 |
| 2 | `/synthetic-research` | Rec | research/synthetic-interviews.md |
| 3 | `/competitor-research` | Rec | research/competitive-analysis.md, PRD §5 |
| 4 | `/generate-research` | Rec | research/analytics-brief.md, survey-questions.md |
| 5 | `/create-survey-audience` | Opt | research/survey-audience-brief.md |
| 6 | `/validate-problems` | Core | output/validated-hypotheses.md, PRD §3-4 |
| 7 | `/solution-hypotheses` | Core | output/solution-hypotheses.md, PRD §6 |
| 8 | `/sketch-solution` | Core | output/solution-sketch.md, PRD §6-7 |
| 9 | `/review-design` | Rec | updated solution-sketch.md |
| 10 | `/create-presentation` | Core | output/presentation.md + .pptx |
| 11 | `/create-design-brief` | Rec | output/design-brief.md |
| 12 | `/estimate-with-dev` | Core | output/dev-estimate.md, PRD §9-10 |
| 13 | `/finalize-prd` | Core | output/PRD.md §8, §11 |
| 14 | `/design-ab-test` | Rec | output/ab-test-design.md |
| 15 | `/create-gate2-presentation` | Core | output/gate2-presentation.md + .pptx |
| — | `/create-tickets` | Post | output/tickets.md + tracker push |
| 16 | `/support-task` | Opt | output/support-brief.md |
| 17 | `/announce-ab-test` | Opt | output/announce-ab-test.md |
| 18 | `/announce-release` | Opt | output/announce-release.md |

## Confirmation commands

| PM says | Action |
|---------|--------|
| "analytics brief sent" | close pending, activate analytics_results |
| "survey brief sent" | close pending, activate survey_results |
| "design brief sent" | close pending |
| "results: ..." | write to research/, close pending |
| "report passed: ..." | write to decisions.md, close pending |
