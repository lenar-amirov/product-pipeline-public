# Changelog

All notable changes to Product Discovery will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.7.2] — 2026-05-09

### Removed (further cleanup)

- `template/CLAUDE.md` — was a stale duplicate of repo-root CLAUDE.md.
  Still showed steps 17/18 as `/announce-ab-test` and `/announce-release`
  (removed in 0.4.0). Pipeline reference table was redundant with main
  CLAUDE.md. No code references it; nothing in `new-initiative.sh` depended
  on per-initiative CLAUDE.md existing.

### Fixed

- `tools/web/app.py` `PIPELINE_STEPS` and `STEP_ARTIFACTS` were stale —
  still referenced removed steps 17/18 (announcements). Updated to v0.4.0
  pipeline (16 = analyze-ab-test, 17 = plan-gtm, 18 = create-gtm-materials,
  19 = support-task).
- `ab-test-announcement-wizard` skill was self-described as "for steps
  17/18" (removed). Repurposed as a structural pattern provider for
  step 18 `/create-gtm-materials` (provides announcement-style scaffolding
  for in-app, email, blog materials).
- README "18 steps" → "19 steps" in two places (stale since 0.4.0).

## [0.7.1] — 2026-05-09

### Removed (cleanup)

- `ONBOARDING.md` — content was duplicating README, CLAUDE.md, and template
  files. Useful unique parts (Tracker MCP setup, FAQ, web dashboard hint)
  merged into README.
- `requirements.txt` — most users only need `rich`. Other dependencies
  (`python-pptx`, `flask`, `markdown`) install on-demand per feature.
  README now lists install commands per use case.
- `tools/web/templates/onboarding.html` and the `/onboarding` Flask route
  (orphaned after ONBOARDING.md removal).
- "Help" link in web dashboard header (pointed to removed onboarding route).

### Changed

- README now contains everything a user needs in one file: install,
  positioning, pipeline overview, configurable templates, tracker
  integration setup (Jira/Linear/GitHub), FAQ.
- Skills (`setup-initiative`, `pipeline-steps`) reference README's
  "Tracker integration" section instead of removed ONBOARDING.md.

Repo went from 84 → 81 tracked files. Top-level is now: CHANGELOG.md,
CLAUDE.md, LICENSE, README.md, skills/, template/, tools/, .gitignore,
.claude/, .claude-plugin/.

## [0.7.0] — 2026-05-09

### Added — Cross-initiative awareness (Step 3 of 3 personalization phases)

- `tools/scripts/scan-initiatives.py` — walks `{pm}/*/output/status.json`,
  `CONTEXT.md`, `validated-hypotheses.md`. Generates `.initiatives-digest.md`
  with two sections: Active (current/in-progress) and Archived (done).
  For each: name, current step, progress, metric, segment, baseline→target,
  validated hypotheses. Filters out unfilled placeholders.
- `.claude/settings.json` SessionStart hook now also runs scan-initiatives.py
  (before status.py, so digest is fresh when status.py displays).
- `.initiatives-digest.md` is gitignored (auto-generated, personal).
- CLAUDE.md SESSION START reads the digest after status.py.
- CLAUDE.md REGULAR SESSION now has explicit overlap detection: when PM
  describes a new problem in a regular session, Claude checks digest for
  same-metric/same-segment matches and surfaces relevant prior learnings
  BEFORE drilling down.
- New intent matching: "show my initiatives" → summarize from digest;
  "is this similar to something I did before" → check overlap.

This completes the 3-phase personalization plan (corrections, profile,
cross-initiative awareness). Together they make Claude remember:
- Past **corrections** (.product-corrections.md)
- PM's **identity** (pm-profile.md)
- All **prior work** (.initiatives-digest.md)

## [0.6.0] — 2026-05-09

### Added — PM Profile (Step 2 of 3 personalization phases)

- `pm-profile.md` — personal profile of the PM (Role, Active products,
  Working style, Recurring stakeholders, Domain knowledge, Constraints).
  Loaded by Claude at every session start to tailor responses.
- Sections marked `[auto]` are updated silently by Claude when it
  observes recurring patterns (e.g. third time PM uses SIF → noted).
  Non-auto sections (Role, Constraints) require PM confirmation before
  edit.
- FIRST LAUNCH "Name + create" step now asks one question that captures
  name + role + company in one sentence (e.g. "Alex, Senior PM at
  Acme on checkout flows"). No additional friction beyond what was there.
- New CLAUDE.md RULES entry: **Grow pm-profile.md lazily.** Concrete
  triggers for auto-updates (e.g. mentioned-twice product, repeated
  methodology, recurring stakeholder name).

Coming next:
- 0.7.0 — Cross-initiative awareness (`.initiatives-digest.md`)

## [0.5.0] — 2026-05-09

### Added — Product corrections (Step 1 of 3 personalization phases)

- `.product-corrections.md` — personal log of accumulated corrections,
  loaded by Claude at every session start. Five sections: Metrics,
  Segments, Methodology, Style, Process. Created by `init` skill if
  missing; never overwritten if exists. Gitignored (personal).
- CLAUDE.md SESSION START now reads `.product-corrections.md` after
  status.py and applies every rule in the file to all responses.
- New CLAUDE.md RULES entry: **Recognize corrections proactively.**
  When PM pushes back, Claude categorizes (local fact / universal
  preference / repeated correction) and either appends to decisions.md
  or proposes addition to `.product-corrections.md`.
- New CLAUDE.md RULES entry: **Apply corrections consistently.**
  Every rule in the file applies to every response.

Coming next:
- 0.6.0 — PM profile (`pm-profile.md`)
- 0.7.0 — Cross-initiative awareness (`.initiatives-digest.md`)

## [0.4.0] — 2026-05-09

### Added

- **Step 16 `/analyze-ab-test`** in Phase 2 — analyze AB test results for
  statistical significance, primary metric movement vs MDE, guardrails,
  segments. Produces ship/extend/iterate/stop decision with reasoning.
  Optional companion: `pm-skills:pm-data-analytics:ab-test-analysis`
  (`/analyze-test`) for dedicated stat-sig tooling.
- **Step 17 `/plan-gtm`** in Phase 3 — full GTM plan for rolling out the
  validated solution to **existing product users** (not net-new launch).
  Covers activation segment, value prop, channels, rollout phases,
  success metrics, risk mitigation. Optional companion:
  `pm-skills:pm-go-to-market:gtm-strategy` (`/plan-launch`).
- **Step 18 `/create-gtm-materials`** in Phase 3 — generates the actual
  materials referenced in the GTM plan: in-app notifications, email
  copy, blog posts, help center articles, sales/CSM enablement, support
  FAQ. Stores in `output/materials/`. Optional companion:
  `pm-skills:pm-marketing-growth:value-prop-statements`,
  `positioning-ideas`.
- New template stubs: `output/gtm-plan.md`, `output/gtm-materials.md`,
  `output/materials/` directory.
- New pending labels in dashboard: `ab_test_analysis`,
  `gtm_materials_review`.

### Removed

- **Step 17 `/announce-ab-test`** and **Step 18 `/announce-release`**
  (the old single-channel announcement steps). Replaced with
  `/create-gtm-materials` which generates a multi-channel package.

### Changed

- Phase 3 renamed: "Launch Preparation" → "Launch (rollout to existing
  users)" — clarifies that GTM here is for existing product users
  receiving a new feature, not net-new product launch.
- `/support-task` moved from step 16 to step 19.
- Pipeline now has 19 steps (was 18).
- Step 16 ab-test-analysis and step 17 plan-gtm are Recommended/Core,
  enabled by default in `full` template.

## [0.3.0] — 2026-05-08

### Changed

- **Repositioning**: Product Discovery is now framed as a "tracked initiative
  pipeline" rather than a generic "AI copilot for product discovery". The
  README explicitly contrasts with PM skill toolboxes (e.g. pm-skills): they're
  for one-shot answers, this is for multi-session work on a single initiative.
- README leads with "Why this, and not a PM skill toolbox?" comparison table.
- Plugin and marketplace descriptions emphasize: persistent state, living PRD,
  evidence-typed hypotheses, multi-session continuity.
- New keywords: `initiative-pipeline`, `living-prd`, `evidence-typing`.

## [0.2.0] — 2026-05-07

### Added

- `.claude/settings.json` with `SessionStart` hook that auto-runs
  `tools/scripts/status.py` on every session start. This guarantees the
  welcome screen / initiative dashboard appears, regardless of whether
  Claude reads CLAUDE.md proactively.

### Changed

- CLAUDE.md SESSION START block is now imperative ("STOP — READ THIS BEFORE
  RESPONDING"). Explicit anti-pattern guidance: don't give a polished
  consulting answer before completing the procedure.
- init skill: handles existing `.claude/settings.json` — warns the user
  and shows the hook snippet to merge manually.
- init skill: recommends `pip3` over `pip` (macOS often lacks `pip`).

### Fixed

- Pipeline procedure was being skipped when users asked product questions
  directly — Claude would answer as a generic consultant. The SessionStart
  hook + stronger CLAUDE.md instructions force the FIRST LAUNCH flow.

## [0.1.0] — 2026-05-06

Initial public release.

### Added

- Plugin distribution via Claude Code marketplace (`product-discovery`)
- `/product-discovery:init` skill — scaffolds the pipeline into a user's project
- 19 specialized skills covering product discovery (CJM analysis, hypothesis
  validation, solution design, PRD writing, AB test design, etc.)
- Pipeline of 18 configurable steps across 3 phases:
  - Phase 1: Problem Research → Problem Research Report
  - Phase 2: Solution Development → Solution Research Report
  - Phase 3: Launch Preparation
- 5 pipeline templates: Quick / Full / Problem-only / Solution-only / Custom
- Tracker integration for Jira / Linear / GitHub Issues via MCP
- Branded session-start dashboard (`status.py`) with first-launch onboarding
- First-launch flow: one sentence → initiative + hypotheses + research plan
- Evidence typing system (REAL / SYNTHETIC / INFERRED / AMBIGUOUS) with
  confidence scoring 0.0–1.0
- Living PRD that builds incrementally across pipeline steps
- Optional Flask web dashboard for visual tracking
