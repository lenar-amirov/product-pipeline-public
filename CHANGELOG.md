# Changelog

All notable changes to Product Discovery will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.4.1] — 2026-07-20

Docs sync: the README had drifted to the pre-redesign product (linear
19-step pipeline + workflow templates) while the tool became jobs-first
with a coverage map. A consistency audit found 1 hard contradiction +
several gaps; all fixed.

### Changed (README now describes the actual pipeline)

- "The pipeline" section → "How it works — jobs, not steps": a jobs table
  (10 jobs), the 7-phase coverage map (Frame→Learn) as the progress model,
  gate preconditions, and the post-launch Learn loop — none of which the
  README previously mentioned.
- Removed the workflow-template table (Quick/Full/Problem/Solution/Custom)
  and the FAQ "switch to quick template" — templates were deprecated in
  0.9 and CLAUDE.md forbids offering them; the README was promising a
  feature the tool refuses.
- "What you accumulate": status.json described via `dependencies[]` (not
  legacy "pending tasks"); registry views (`registry.md`, `ost.md`) and
  banked knowledge facts surfaced.
- "What's bundled": added coverage.py, render-ost/render-pdf, check-leaks;
  "intent matching" → "JOBS CATALOG"; link to REPO-MAP.
- steps.md table of contents: STEP 18 marked Optional (matched its header;
  a leftover from the 1.3.0 GTM-materials downgrade).

## [1.4.0] — 2026-07-06

One path (docs/ONE-PATH-1.4.md): a single distribution channel and a
60-second start.

### Removed — the plugin contour

- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and the
  `init` installer skill are gone. The plugin was a wrapper around "copy
  files": Claude Code doesn't load a plugin's CLAUDE.md into your project,
  so init copied files anyway — and marketplace auto-updates never reached
  scaffolded projects. `git clone` does the same job in one command with
  none of the ceremony.
- **Migration note for plugin users**: your scaffolded project is
  self-contained — it keeps working forever, nothing to do. For updates,
  clone this repository and move your `{pm}/` folders in (or keep working
  as is). `/plugin uninstall product-discovery` at your leisure.

### Changed

- README: one install path — `git clone … && claude` (no questions, no
  restart, no required dependencies) + Download ZIP for the git-less +
  `git pull` updates; explicit note that initiatives are created inside
  the clone and never conflict with updates. The "what happens next"
  section now describes the value-first flow (job first, initiative
  offered after).
- Welcome screen (both rich and plain) now shows the point-entry jobs:
  "read this deck" · "I need an analyst brief" · "break down problem X".
- Versioning lives in CHANGELOG headings only (plugin.json was the second
  copy and a recurring desync source).
- PRIVACY.md rewritten tool-first (install = clone/ZIP; marketplace
  paragraph removed); REPO-MAP updated (tree 80 → 77 files).
- check-leaks.py: deletions no longer trip the path check (removing an
  old path is not a leak).

## [1.3.0] — 2026-07-04

The pruning release: the repository now matches its manifesto 1:1
(see docs/CLEANUP-1.3.md). ~30 files / ~2500 lines removed, one job added.

### Removed

- **19 template content stubs** (13 output + 6 research): jobs create
  artifacts when they run; formats are canonical in output-formats.md.
  Stubs also made the web viewer report empty placeholders as existing
  artifacts. Template: 28 → 11 files; forms filled by external humans
  (design-comments, dev-estimate) stay.
- **Web dashboard mutations**: initiative-creation form (the
  upfront-questionnaire anti-pattern), share machinery (multi-user seed
  from the anti-scope; use static_export.py to share), CJM upload/reorder/
  delete, CONTEXT.md web editing. app.py 940 → ~610 lines; the dashboard
  is a read-only viewer.
- **consulting-problem-solving shell** (8-stage framework + references
  01-07 duplicating the pipeline): ~960 of 1360 lines deleted.

### Added

- **`/deep-think`** — 10th job: facilitated partner-led session for
  problems that are not initiatives yet (strategy, org, build-vs-buy),
  running on problem-structuring + pyramid + writing-style, with an
  always-offered bridge into Frame + /hypotheses.
- **`.claude/rules/writing-style.md`** (Strunk & White, transplanted) —
  path-scoped to artifacts; item 6 of the anti-generic self-check.
- **strategic-narrative-generator/references/** — mckinsey.md +
  exec-communication.md (transplanted), loaded only when assembling gate
  decks.
- Micro-examples: PRD living-doc versioning, tech-spec behavior contract,
  multi-source worked insight.

### Changed

- STEP 18 (GTM materials) Recommended → **Optional**, rewritten from a
  10-file batch factory to per-channel on-request artifacts (anti-scope:
  document generation is commoditized).
- Legacy `pending.*` support marked **REMOVE IN 2.0** in
  pipeline_constants.py, status.py and next-advisor — migrations get
  deadlines like dependencies do.
- ux-research-brief unified to `research/`; `template/slides/` turned into
  an explicit corporate-deck-template option.

## [1.2.1] — 2026-07-03

Skill audit against the canonical skill-creator checklist + domain-expert
review (two-agent pass over all 24 skills; 0 critical, 3 medium, batch of
minor findings — all fixed).

### Fixed (domain corrections)

- `problem-structuring`: leaves localize the gap, hypotheses explain it —
  the two are no longer conflated; SIF formula spelled out; "stop
  drilling" rule added.
- `solution-scoring`: numeric confidence stages for solutions (0.1–0.3
  untested → 0.4–0.6 concept-tested → 0.7+ experiment on our users);
  viability RED criteria defined (one disqualifier parks the solution
  regardless of ICE).
- `experiment-design`: MDE explicitly business-meaningful (not merely
  detectable); decision criteria pre-registered; primary decides,
  guardrail breach pauses — not silently vetoes.
- Minor: ingest source-quality check + AMBIGUOUS range; challenge spells
  out gate criteria; post-launch-review miss diagnosis (evidence vs sizing
  vs execution); user-testing result→confidence anchors; funnel SQL
  PARTITION BY note; design-critique anti-patterns.

### Changed

- `pipeline-steps` restructured per progressive disclosure: SKILL.md is
  now a 63-line navigation layer (jobs map, registry rules, step index);
  per-step details moved to `references/steps.md` with a table of
  contents — only the section being executed gets loaded.

## [1.2.0] — 2026-07-03

### Added

- **Pre-push leak guard**: `tools/scripts/check-leaks.py` blocks outgoing
  pushes containing initiative folders / personal top-level paths,
  credential files (.mcp.json, settings.local.json, …), token-like values,
  or personal markers from a gitignored `.leak-patterns` file.
  `tools/scripts/install-hooks.sh` installs it as a git pre-push hook.
- **Two-way Jira loop** (CLAUDE.md): at session start, open dependencies
  with a `jira` key are polled via MCP — closed issues prompt "mark done +
  ingest results", changed descriptions get noted; `/brief` and `/tickets`
  label created issues `initiative:<slug>` and record keys back into
  `dependencies[]`. Degrades silently without MCP.

## [1.1.0] — 2026-07-03

Skill portfolio rationalization: every skill now has exactly one clear
role in the jobs-first architecture. 23 skills before, 23 after — but
6 removed/merged, 6 added, 4 refocused.

### Removed / merged

- `ab-test-announcement-wizard` removed — announcement structure folded
  into pipeline-steps STEP 18 (its only consumer).
- `usability-test-plan` + `user-test-concept` → **`user-testing`** with
  two modes (quick concept test / full study); shared registry-output and
  frequency-honesty rules; `/user-test-concept` stays as an alias.
- `funnel-analysis-builder` + `product-analytics-setup` →
  **`tracking-and-funnels`**: schema derived from open hypotheses, funnel
  reading with definitions/windows discipline, quality checks; SQL walls
  and Amplitude/GA4/GDPR textbook content dropped (~500 → 70 lines).
- `product-discovery-template` → **`solution-scoring`** (assumption map +
  ICE/SIF + business viability for /solutions); its parallel discovery
  framework duplicated the pipeline itself and is gone.

### Added

- **`problem-structuring`** — MECE / pyramid / 80-20 extracted as the
  pipeline's structuring engine (steps 1/3/6);
  `consulting-problem-solving` remains as a standalone advanced mode, no
  longer referenced by pipeline steps.
- **`experiment-design`** — MDE, sample size, guardrails, pre-registered
  decision criteria, and "is an AB test even the right instrument"
  (step 14 engine, extracted from the deleted discovery template).
- **`interview-analysis`** — notes → coding → patterns with frequency
  honesty → registry verdicts; fills the 6c method gap (interviews are
  the highest-confidence qualitative REAL source and had no method).

### Refocused

- `ambiguity-resolver` — honest role: structuring briefs HANDED DOWN by
  stakeholders (out-of-scope boundaries, decision owner); the PM's own
  vague problems are FIRST LAUNCH territory.
- `design-critique-template` — hypothesis-fit is now the first and
  decisive critique pass; heuristics second; findings that overturn
  solution assumptions go to the registry.
- `setup-initiative`, pipeline-steps STEP 18 — see above.

## [1.0.1] — 2026-07-03

Full skill-layer revision after the 1.0 redesign (audited by a two-agent
review + init/rules pass).

### Fixed (migration leftovers)

- pipeline-steps: all 8 `activate pending.*` trackings → `dependencies[]`
  creation; steps 0/5.5 no longer mention templates/pendings; step 1 no
  longer blocks on empty CONTEXT.md (zero-setup).
- setup-initiative: template picker removed; reframed as the Frame-phase
  filler required by gates — never a forced first step.
- next-advisor diagnoses `dependencies[]` + the coverage map;
  post-launch-review closes its dependency; strategic-narrative sources
  point at the registry; output-formats states markdown is a narrative
  view of `hypotheses.json`.
- init skill: copies `.mcp.json.example` and `.gitignore`, 3-hook
  settings snippet, `rich` marked optional, frontmatter `name` added.

### Changed (registry as mandatory output)

- evidence-typing rule gains "Who writes to the registry"; concrete
  `hypotheses.py` commands wired into multi-source-signal-synthesiser,
  funnel-analysis-builder, product-analytics-setup, usability-test-plan,
  user-test-concept, product-discovery-template.
- Three generic skills rewritten tool-specific (613 → 141 lines):
  system-design-doc (PM feasibility view), technical-spec-document
  (implementation blueprint with sharp boundary), ui-pattern-library
  (pattern selection from the hypothesis mechanism for /sketch).
- Frontmatter hygiene: consulting-problem-solving description 1406 → 416
  chars; design-critique-template single-line YAML; step-number
  references generalized in user-persona-builder and
  ab-test-announcement-wizard.

## [1.0.0] — 2026-07-03

The map-and-gates release completes the redesign started in 0.8: hypotheses
are machine state, jobs are the interface, and now progress is an evidence
coverage map with real gates and a closed learning loop.

### Changed (E11 — coverage map)

- **"Step 4/20" is dead.** `tools/scripts/coverage.py` computes seven
  phases (Frame → Evidence → Solution → Bet → Build → Launch → Learn) from
  actual state: CONTEXT.md fields, registry verdicts and validation,
  artifact substance, gate statuses. Dashboard and digest show
  `Frame 2/4 · Evidence 2/3 · …` plus a focus line naming exactly what's
  missing. Template labels removed from the dashboard.

### Added (E12 — real gates)

- `validate-evidence.py --gate`: deck assembly is blocked until ≥2
  hypotheses are confirmed REAL, the registry is violation-free, and Frame
  is complete — wired as a mandatory precondition into steps 10 and 15.
- `challenge` skill (`/challenge`): adversarial gate rehearsal by three
  hostile personas (CFO, VP Product, skeptic engineer) armed with the
  registry; reports fatal/painful/cosmetic hits with concrete fixes and
  the three most likely real questions.

### Added (E13 — Opportunity Solution Tree)

- `tools/scripts/render-ost.py`: `output/ost.md` (Mermaid, zero deps) —
  outcome → tracks → hypotheses colored by status/evidence → linked
  solutions. Refreshed alongside registry.md by `/validate`.

### Added (E14 — the learning loop)

- `post-launch-review` skill: fact vs the Frame target, production
  verdicts for hypotheses, INFERRED-calibration, and a retrospective.
  Ship decision (step 16) now creates a `post_launch_review` dependency
  (launch + 90 days) so the loop cannot be silently skipped.
- `knowledge/facts.json` — PM-level knowledge base (personal, gitignored):
  product truths banked at review time surface in the initiatives digest,
  so every new initiative starts with what past ones learned.

## [0.9.0] — 2026-07-03

Jobs-first release: the pipeline stops being the interface and becomes the
bookkeeping. See docs/ROADMAP-0.8.md (epics E5–E10).

### Changed (E5+E6 — jobs-first interface, zero-setup)

- **JOBS CATALOG replaces the intent table** in CLAUDE.md: ~9 standalone
  jobs (`/hypotheses` `/ingest` `/brief` `/validate` `/solutions` `/sketch`
  `/challenge` `/tickets` `/next`); each works without an initiative and
  offers persistence after delivering value. Legacy `/commands` remain as
  aliases.
- **FIRST LAUNCH inverted**: run the matching job immediately, deliver the
  result, then offer to save as an initiative. CONTEXT.md fills
  incrementally; no upfront checklist. Pipeline **templates
  (quick/full/…) are deprecated** — never offered.
- `new-initiative.sh`: sed metacharacter escaping in initiative names;
  jobs-first next-steps output.

### Added (E7+E8 — advisor and dependencies)

- `next-advisor` skill (`/next`): diagnoses state — stalled dependencies →
  evidence violations → ready-but-unstarted work → frame gaps → uncovered
  hypotheses — instead of "next is step N". Dashboard prints a
  `! … — ask /next` hint when issues exist.
- `dependencies[]` in status.json: owner, deadline, jira key, blocked
  hypotheses. Dashboard shows age and OVERDUE; on overdue Claude must offer
  chase / move deadline / switch to synthetic (with confidence downgrade) /
  conscious skip. Legacy `pending.*` values now parse their leading ISO
  date, so ages display for old initiatives.

### Added (E9 — ingestion)

- `ingest` skill (`/ingest`): deck/export/Confluence/pasted data →
  extracted metrics with exact locations → mapped onto open hypotheses
  (upgrade / refute / flag `data_inconsistency` / new / inbox-notes), typed
  by source.
- `tools/scripts/render-pdf.py`: PDF → PNG with no Python deps
  (pdftoppm → mutool → compiled Swift/CoreGraphics fallback).

### Added (E10 — anti-generic guarantee)

- Anti-generic self-check in `.claude/rules/output-formats.md`: no
  unsourced claims, no placeholder advice, proof surfaces REAL-only,
  frequency honesty, numbers cross-checked. Wired as a mandatory step into
  `strategic-narrative-generator` and `product-requirements-doc`.

## [0.8.0] — 2026-07-03

### Added (E1 — hypothesis registry, see docs/ROADMAP-0.8.md)

- `output/hypotheses.json` — machine-readable single source of truth for
  hypothesis state (status, evidence type, confidence, sources, history).
  Narrative markdown stays authored prose; `output/registry.md` is a
  generated view.
- `tools/scripts/hypotheses.py` — registry engine (add / set / validate /
  render / show), stdlib-only. `set` writes history automatically;
  `validate` enforces evidence-typing confidence ranges and requires
  sources for REAL.
- `tools/scripts/migrate-hypotheses.py` — best-effort conversion of legacy
  `hypotheses.md` / `validated-hypotheses.md` into the registry.
- `template/output/hypotheses.json` — empty registry with `_schema` docs.
- Pipeline steps 1/2/6/7 and evidence-typing rule updated to route all
  hypothesis state changes through the registry.

### Added (E2 — evidence validators)

- `tools/scripts/validate-evidence.py` — SessionStart evidence audit: one
  line per initiative (confirmed REAL / open / refuted / flagged) plus
  violations; wired into root and template `.claude/settings.json` hooks.
- `data_inconsistency` flag (`hypotheses.py set <id> --flag/--unflag`):
  while sources disagree, confidence above 0.6 is reported as a violation
  every session until reconciled.
- Evidence-typing rule gains "Operational rules" — contradictions,
  upgrades and downgrades go through the registry so history captures
  every transition.

### Changed (E3 — single source of truth for pipeline structure)

- `tools/scripts/pipeline_constants.py` — canonical step list (0–19 plus
  sub-steps 5.5/8.5), labels, commands, phases, `enabled_total()` and
  `find_current_step()`. status.py, scan-initiatives.py, tools/web/app.py
  and static_export.py now import it instead of keeping four diverged
  copies (fallback totals were 18 vs 19 vs 21; app.py lacked step 0;
  status.py's current-step scan never reached step 19).
- Digest now reports hypothesis verdicts from the registry
  ("✅ REAL: … · ❌ … · открыто: N · ⚠️ flags: …") instead of relying
  solely on regex-parsed CONTEXT.md fields.

### Fixed / Security (E4 — 0.7.x audit debt)

- `tools/web/app.py` failed to import on Python < 3.12 (f-string with a
  backslash escape) — the web dashboard could not start at all on the
  system Python of current macOS.
- Web dashboard hardening: binds to 127.0.0.1 with debug off by default
  (`PIPELINE_HOST` / `PIPELINE_DEBUG=1` to override), rendered markdown is
  sanitized (script/iframe/object/embed, `on*` handlers, `javascript:`
  URLs), artifact paths are resolved and contained (`resolve()` check
  instead of a `..` substring test), CJM uploads restricted to an
  extension whitelist.
- `generate-pptx.py` looked for initiatives next to the script instead of
  the repo root — the PPTX step never worked.
- `setup-initiative` and `user-test-concept` skills had no frontmatter —
  they could not be triggered by intent, only by exact command.
- README refreshed: initiatives digest, hypothesis registry, web
  dashboard + static export documented; tracker integration rewritten for
  `.mcp.json`; requirement relaxed to Python 3.9+ (core needs no
  packages); comparison table now covers Anthropic's official PM plugin.

## [0.7.3] — 2026-07-02

### Security

- **Initiative folders (`{pm}/…`) are now gitignored.** Previously SESSION END
  instructed committing and pushing initiative data into this public repo,
  contradicting the local-first promise in PRIVACY.md. Every top-level
  directory except the tool's own (`template/`, `tools/`, `skills/`,
  `.claude*/`, `.github/`) is ignored; SESSION END in CLAUDE.md no longer
  commits initiative data (use your own private repo if you want history).
- **MCP credentials moved out of tracked files.** TRACKER INTEGRATION docs
  told users to put `mcpServers` into `.claude/settings*.json` — an invalid
  Claude Code settings field and, for `settings.json`, a tracked file that
  would leak tokens. Config now lives in gitignored `.mcp.json`; new
  `.mcp.json.example` ships as a placeholder template.

### Fixed

- `tools/scripts/status.py` crashed with `NameError` on machines without
  `rich` (module-level `Console()` ran before the `HAS_RICH` check), which
  broke the SessionStart hook — the product's entry point — on fresh forks.
  The plain-text fallback now works.
- `tools/scripts/scan-initiatives.py` truncated multi-line CONTEXT.md fields
  at the first line break, so `.initiatives-digest.md` contained sentences cut
  mid-phrase (e.g. a Baseline listing only its header line). Field values are
  now captured up to the next field/heading and collapsed into one line; the
  per-field cap raised 120 → 200 chars.

### Added

- `template/.claude/settings.json` is now actually tracked. The whole
  `template/.claude/` directory was missing from the repo (swallowed by
  `**/settings.local.json` plus never being added), so scaffolded initiatives
  got no SessionStart hook config.

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
