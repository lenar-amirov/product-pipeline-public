# Changelog

All notable changes to Product Discovery will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
