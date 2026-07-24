# Repository Map

> Every tracked file and why it exists. If a file can't justify its line
> here, it gets pruned (see docs/CLEANUP-1.3.md). Updated for 1.4.0.

## Root — the front door

| File | Why it exists |
|---|---|
| `README.md` | Onboarding: what the tool is, install (clone/ZIP — the one path), jobs, tracker setup, FAQ |
| `CLAUDE.md` | **The master prompt.** Session lifecycle (SESSION START/END), FIRST LAUNCH value-first flow, JOBS CATALOG, external dependencies + two-way Jira loop. Loaded by Claude Code every session — this file IS the product's behavior |
| `CHANGELOG.md` | Release history from 0.1 to the current version — the honest record of what changed and why; also the only carrier of the version number |
| `PRIVACY.md` | Local-first promise: what stays on the user's machine (enforced by .gitignore + leak guard) |
| `LICENSE` | MIT |
| `.gitignore` | Two jobs: ignore secrets/personal files AND whitelist-ignore every non-tool top-level dir — initiative data physically can't be committed |
| `.mcp.json.example` | Jira/Confluence MCP template; user copies to gitignored `.mcp.json` and fills in the token |

## `.claude/` — behavior configuration

| File | Why it exists |
|---|---|
| `settings.json` | Three SessionStart hooks: initiatives digest, dashboard, evidence audit — the tool's heartbeat |
| `rules/evidence-typing.md` | REAL/SYNTHETIC/INFERRED/AMBIGUOUS with confidence ranges; operational rules (flags, upgrades through the registry); "who writes to the registry" |
| `rules/output-formats.md` | Canonical artifact formats + the anti-generic self-check every generated document must pass |
| `rules/writing-style.md` | Strunk & White prose discipline, path-scoped to artifacts; item 6 of the self-check |

## `.claude/skills/` — 23 skills, one clear role each

### Jobs (the primary interface)

| Skill | Job / role |
|---|---|
| `ingest` | `/ingest` — decks/exports/pages → metrics with locations → mapped onto registry hypotheses |
| `next-advisor` | `/next` — diagnoses state (stalled deps → violations → ready work) instead of "next step number" |
| `challenge` | `/challenge` — adversarial gate rehearsal by three hostile personas, armed with the registry |
| `deep-think` | `/deep-think` — partner-led session for problems that aren't initiatives yet; bridge into Frame |
| `post-launch-review` | Closes the loop: fact vs target, production verdicts, knowledge base, INFERRED calibration |
| `setup-initiative` | Fills the Frame phase (metric/target/kill criteria) — required by gates, never a forced first step |
| `ambiguity-resolver` | Structures briefs handed down by stakeholders (scope boundaries, decision owner) |

### Pipeline engines

| Skill | Role |
|---|---|
| `pipeline-steps` (+ `references/steps.md`) | Navigation layer: jobs↔steps map, registry rules, step index; per-step details in the reference (read only the section being executed) |
| `problem-structuring` | MECE trees, pyramid, 80/20 + SIF — the engine of `/hypotheses` and `/validate` synthesis |
| `solution-scoring` | Assumption map, staged ICE confidence, viability RED criteria — the engine of `/solutions` |
| `experiment-design` | MDE (business-meaningful), pre-registered decision criteria, guardrails — engine of step 14 |
| `interview-analysis` | Notes → coding → frequency-honest patterns → registry verdicts (the 6c method) |
| `user-testing` | Two modes: 15-min concept test / full usability study; results anchored to confidence |
| `tracking-and-funnels` | Event schema derived from open hypotheses; funnel reading with definition/window discipline |
| `multi-source-signal-synthesiser` | Reconciles conflicting sources (convergence/divergence/weighting) for `/validate` |
| `user-persona-builder` | Personas with JTBD + evidence typing, used by `/hypotheses` and synthetic research |

### Artifact craft

| Skill | Role |
|---|---|
| `product-requirements-doc` | The living PRD: structure, versioning, registry-backed §4 |
| `strategic-narrative-generator` (+ `references/mckinsey.md`, `references/exec-communication.md`) | Gate decks and strategy narratives; deck craft references load only when assembling a deck |
| `user-story-generator` | `/tickets`: INVEST stories, Given/When/Then, tracker push via MCP |
| `design-critique-template` | Step 9: hypothesis-fit first, heuristics second, severity-ranked feedback |
| `ui-pattern-library` | `/sketch`: pattern selection from the hypothesis mechanism, platform conventions |
| `system-design-doc` | PM feasibility view: affected components, dependencies, constraining NFRs (→ PRD §9-10) |
| `technical-spec-document` | Implementation blueprint: scope by component, behavior contracts, acceptance mapping |

## `template/` — what a new initiative starts with (12 files)

| File | Why it exists |
|---|---|
| `CONTEXT.md` | The initiative frame — fills incrementally as jobs run, no upfront checklist |
| `.claude/settings.json` | Per-initiative SessionStart hooks (digest + evidence audit) for PMs who open Claude inside the initiative folder |
| `output/status.json` | Machine state: steps, dependencies[], pipeline_config |
| `output/hypotheses.json` | Empty hypothesis registry with `_schema` documentation |
| `output/PRD.md` | Living-document skeleton (sections fill across the pipeline) |
| `output/decisions.md` | Decision log seed |
| `output/design-comments.md` | Form the PM fills after reviewing design (human-facing, hence pre-created) |
| `output/dev-estimate.md` | Form the dev lead fills (same reason) |
| `output/{html,materials,screens}/.gitkeep`, `research/.gitkeep` | Directory structure for renderers and research artifacts |

## `tools/scripts/` — 13 scripts, zero dependencies by design

| Script | Why it exists |
|---|---|
| `pipeline_constants.py` | Single source of truth: steps, phases, totals, `find_current_step` — imported by everything |
| `hypotheses.py` | The registry engine: add/set/validate/render/show; `set` writes history automatically |
| `validate-evidence.py` | SessionStart evidence audit + `--gate` preconditions (blocks deck assembly) |
| `coverage.py` | The coverage map: 7 phases with exit criteria computed from actual state |
| `scan-initiatives.py` | Regenerates `.initiatives-digest.md`: cross-initiative awareness + knowledge-base facts |
| `status.py` | The session-start dashboard: coverage line, dependencies with OVERDUE, `/next` hint |
| `new-initiative.sh` | Scaffolder: copies template, substitutes placeholders (sed-escaped), inits status |
| `migrate-hypotheses.py` | One-time conversion of legacy markdown registries → hypotheses.json |
| `render-ost.py` | Opportunity Solution Tree (Mermaid) generated from the registry |
| `render-pdf.py` | PDF → PNG for `/ingest` (pdftoppm → mutool → compiled Swift fallback) |
| `generate-pptx.py` | Gate presentations markdown → .pptx (needs python-pptx, degrades gracefully) |
| `check-leaks.py` | Pre-push guard: personal paths, credential files, token-like values, `.leak-patterns` markers |
| `install-hooks.sh` | Installs check-leaks as a git pre-push hook |

## `tools/web/` — optional read-only viewer

| File | Why it exists |
|---|---|
| `app.py` | Flask viewer (dashboard, initiative, artifacts, archive) — 127.0.0.1, sanitized markdown, no mutations |
| `static_export.py` | Zero-dependency single-file HTML export of an initiative — the sharing path |
| `templates/base.html` | Layout, theme toggle, screen modal |
| `templates/dashboard.html` | Initiative list |
| `templates/initiative.html` | Initiative detail: context, CJM gallery, steps, decisions |
| `templates/archive.html` | Archived initiatives |
| `templates/_macros.html` | Shared partials (progress segments, step rows, cards) |
| `static/style.css` | The one stylesheet |

## `.github/` — feedback intake

| File | Why it exists |
|---|---|
| `ISSUE_TEMPLATE/bug.yml`, `feedback.yml`, `config.yml` | Structured bug reports and PM feedback — the tool's own evidence intake |

## `docs/` — decision record

| File | Why it exists |
|---|---|
| `ONE-PATH-1.4.md` | The single-distribution-path decision: why the plugin contour died |
| `ROADMAP-0.8.md` | The redesign design-doc (0.8 → 1.0): principles, epics E1–E14, acceptance criteria — why the tool is shaped this way |
| `CLEANUP-1.3.md` | The pruning plan: what was removed and the reasoning |
| `REPO-MAP.md` | This file |
