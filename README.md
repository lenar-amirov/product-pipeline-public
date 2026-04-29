# AI Diamond

AI-powered product discovery copilot built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Takes a product initiative from CJM analysis through research, validation, solution design, and gate presentations — with structured steps, Claude Code skills, and a terminal dashboard.

**Built on best practices**: Double Diamond, Teresa Torres' Continuous Discovery, Marty Cagan's Product Discovery, RICE/ICE frameworks.

## What's inside

- **CLAUDE.md** — master prompt: session lifecycle, configurable pipeline, confirmation commands, output formats
- **template/** — initiative scaffold (CONTEXT.md, output/, research/, slides/)
- **.claude/skills/** — 18 reusable Claude Code skills for product work (discovery, personas, funnels, PRD, design critique, AB test design, etc.)
- **tools/web/** — Flask dashboard for tracking initiatives, viewing artifacts, uploading CJM materials
- **tools/scripts/** — PPTX generation, Telegram reminder bot, initiative scaffolding

## Quick start

1. Clone this repo
2. Create `.pm-local` with your name (e.g. `echo "alice" > .pm-local`)
3. Open in Claude Code (CLI, desktop app, or IDE extension)
4. Say: `create initiative checkout-redesign`
5. Follow the pipeline: `/setup-initiative` -> `/analyze-cjm` -> `/synthetic-research` -> ...

## Pipeline overview

The pipeline has 4 phases with configurable steps:

| Phase | Steps | Gate |
|-------|-------|------|
| 0. Setup | `/setup-initiative` | — |
| 1. Problem research | `/analyze-cjm` -> `/validate-problems` | Problem Research Report |
| 2. Solution design | `/solution-hypotheses` -> `/create-gate2-presentation` | Solution Research Report |
| 3. Launch preparation | `/support-task` -> `/announce-release` | — |

### Configurable steps

Every step has a type that determines whether it can be skipped:

| Type | Meaning | Can disable? |
|------|---------|-------------|
| **Core** | Pipeline doesn't work without it | No |
| **Recommended** | Significantly improves results | Yes, with warning |
| **Optional** | Useful in specific contexts | Yes |

### Pipeline templates

| Template | Steps | Best for |
|----------|-------|----------|
| **Quick Discovery** | 6 steps | PM with existing data, tight timeline |
| **Full Discovery** | All steps | New initiative, unknown problem space |
| **Problem Only** | 5 steps | Understand the problem, solution not needed yet |
| **Solution Only** | 7 steps | Discovery done, need solution design |
| **Custom** | Pick & choose | PM knows exactly what's needed |

### All steps

#### Phase 0: Setup
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 0 | `/setup-initiative` | Core | Alignment checklist: metric, stakeholders, OKR, constraints, kill criteria |

#### Phase 1: Problem Research -> Problem Research Report
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 1 | `/analyze-cjm` | Core | Analyze CJM, formulate problem hypotheses (MECE) |
| 2 | `/synthetic-research` | Recommended | Synthetic interviews for hypothesis pre-validation |
| 3 | `/competitor-research` | Recommended | Scenario analogues and competitive analysis |
| 4 | `/generate-research` | Recommended | Analytics brief + survey questions design |
| 5 | `/create-survey-audience` | Optional | SQL pseudocode for survey audience selection |
| 5.5 | Customer research pause | Recommended | Real research: analytics, survey, 5-8 interviews (Torres) |
| 6 | `/validate-problems` | Core | Validate hypotheses with evidence (3 sub-steps: 6a/6b/6c) |
| 7 | `/solution-hypotheses` | Core | Solution hypotheses with ICE + business viability check |
| 8 | `/sketch-solution` | Core | UI wireframes, screens, user flow |
| 8.5 | `/user-test-concept` | Optional | Concept test with 3-5 real users |
| 9 | `/review-design` | Recommended | Heuristic evaluation + design iteration |
| 10 | `/create-presentation` | Core | Problem Research Report (problem + solution sketch) |

#### Phase 2: Solution Development -> Solution Research Report
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 11 | `/create-design-brief` | Recommended | Brief for designer with wireframes |
| 12 | `/estimate-with-dev` | Core | Dev lead fills tech estimate, dependencies |
| 13 | `/finalize-prd` | Core | User stories, acceptance criteria, open questions |
| 14 | `/design-ab-test` | Recommended | AB test design: baseline, MDE, sample size, guardrails |
| 15 | `/create-gate2-presentation` | Core | Solution Research Report |

After Solution Research Report: `/create-jira` for dev tickets.

#### Phase 3: Launch Preparation
| # | Command | Type | What it does |
|---|---------|------|-------------|
| 16 | `/support-task` | Optional | Support team brief: FAQ, scenarios, known limitations |
| 17 | `/announce-ab-test` | Optional | Internal AB test announcement |
| 18 | `/announce-release` | Optional | Internal release announcement |

See [CLAUDE.md](CLAUDE.md) for full pipeline documentation.

## Skills

| Skill | Purpose |
|-------|---------|
| `setup-initiative` | Alignment checklist, pipeline configuration |
| `consulting-problem-solving` | MECE structure, pyramid principle, synthesis |
| `product-discovery-template` | Hypotheses, ICE scoring, assumption mapping, business viability check |
| `user-persona-builder` | Behavioral personas from research data + synthetic research methodology |
| `funnel-analysis-builder` | Conversion funnels, cohort analysis, SQL patterns |
| `product-requirements-doc` | PRD structure and content |
| `user-story-generator` | User stories with Given/When/Then acceptance criteria |
| `usability-test-plan` | UX research methodology, sample size |
| `user-test-concept` | Concept testing with real users |
| `product-analytics-setup` | Event schema, naming conventions, tracking |
| `ui-pattern-library` | UI patterns for wireframes |
| `design-critique-template` | Heuristic evaluation of design decisions |
| `system-design-doc` | Technical architecture and dependencies |
| `technical-spec-document` | Implementation blueprints |
| `strategic-narrative-generator` | Strategic narratives + Gate presentation structure |
| `multi-source-signal-synthesiser` | Cross-source signal synthesis with evidence typing |
| `ab-test-announcement-wizard` | Internal AB test / release announcements |
| `ambiguity-resolver` | Resolving ambiguities in requirements (utility — any step) |

## Dashboard

Optional Flask web dashboard (`tools/web/app.py`) for team use:
- Initiative list with progress tracking
- Context editing and CJM upload
- Step-by-step navigation with Claude Code integration
- Artifact viewer (PRD, hypotheses, presentations)

## Key concepts

### Evidence confidence

Every piece of evidence is typed by source:
- **REAL** (0.6-1.0): Analytics data, survey results, user interviews
- **SYNTHETIC** (0.2-0.4): AI-generated interviews, synthetic research
- **INFERRED** (0.3-0.5): Logical deductions from other evidence
- **AMBIGUOUS** (0.1-0.3): Contradictory or unclear signals

### Living PRD

The PRD is built incrementally as you progress through the pipeline:
- Steps 1 -> sections 1-2 (context, user)
- Step 6 -> sections 3-4 (metrics, validated problems)
- Steps 7-8 -> sections 6-7 (solution, scope)
- Steps 12-13 -> sections 8-11 (stories, NFR, risks, open questions)

### Validation branching (step 6)

After validation, the pipeline branches:
- All confirmed -> step 7
- Partially confirmed -> narrow focus, step 7
- None confirmed -> back to step 1
- Insufficient data -> repeat data collection

## License

MIT
