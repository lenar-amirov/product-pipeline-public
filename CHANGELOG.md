# Changelog

All notable changes to Product Discovery will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
