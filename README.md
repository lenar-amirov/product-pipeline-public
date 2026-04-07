# Product Pipeline

AI-powered product management pipeline built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Takes a product initiative from CJM analysis through research, validation, solution design, and gate presentations — with 18 structured steps, Claude Code skills, and a web dashboard.

## What's inside

- **CLAUDE.md** — master prompt: session lifecycle, 18-step pipeline, confirmation commands, output formats
- **template/** — initiative scaffold (CONTEXT.md, output/, research/, slides/)
- **.claude/skills/** — 16 reusable Claude Code skills for product work (discovery, personas, funnels, PRD, design critique, AB test design, etc.)
- **tools/web/** — Flask dashboard for tracking initiatives, viewing artifacts, uploading CJM materials
- **tools/scripts/** — PPTX generation, Telegram reminder bot, initiative scaffolding

## Quick start

1. Clone this repo
2. Create `.pm-local` with your name (e.g. `echo "alice" > .pm-local`)
3. Open in Claude Code (CLI, desktop app, or IDE extension)
4. Say: `создай инициативу checkout-redesign`
5. Follow the pipeline: `/analyze-cjm` → `/synthetic-research` → ...

## Pipeline overview

| Phase | Steps | Gate |
|-------|-------|------|
| Problem research + Solution sketch | 1-10 | Gate 1 |
| Solution refinement | 11-15 | Gate 2 |
| Launch preparation | 16-18 | — |

See [CLAUDE.md](CLAUDE.md) for full pipeline documentation.

## Skills

| Skill | Purpose |
|-------|---------|
| `consulting-problem-solving` | MECE structure, pyramid principle, synthesis |
| `product-discovery-template` | Hypotheses, ICE scoring, assumption mapping |
| `user-persona-builder` | Behavioral personas from research data |
| `funnel-analysis-builder` | Conversion funnels, cohort analysis, SQL patterns |
| `product-requirements-doc` | PRD structure and content |
| `user-story-generator` | User stories with Given/When/Then acceptance criteria |
| `usability-test-plan` | UX research methodology, sample size |
| `product-analytics-setup` | Event schema, naming conventions, tracking |
| `ui-pattern-library` | UI patterns for wireframes |
| `design-critique-template` | Heuristic evaluation of design decisions |
| `system-design-doc` | Technical architecture and dependencies |
| `technical-spec-document` | Implementation blueprints |
| `strategic-narrative-generator` | Strategic narratives for presentations |
| `multi-source-signal-synthesiser` | Cross-source signal synthesis |
| `ab-test-announcement-wizard` | Internal AB test / release announcements |
| `ambiguity-resolver` | Resolving ambiguities in requirements |

## Dashboard

Optional Flask web dashboard (`tools/web/app.py`) for team use:
- Initiative list with progress tracking
- Context editing and CJM upload
- Step-by-step navigation with Claude Code integration
- Artifact viewer (PRD, hypotheses, presentations)

## License

MIT
