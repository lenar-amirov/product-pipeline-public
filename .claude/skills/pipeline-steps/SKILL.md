---
name: pipeline-steps
description: Detailed instructions for each pipeline step (0-18). Read this when PM calls a specific pipeline command like /analyze-cjm, /validate-problems, etc.
---

# Pipeline Step Instructions

Read the relevant step below when PM invokes a pipeline command.

---

## STEP 0 — `/setup-initiative` (Core)

**Type**: PM fills with AI guidance
**Output**: filled `CONTEXT.md` + `pipeline_config` in status.json
**Skills**: `setup-initiative` + `ambiguity-resolver` (if brief is vague)

Guide PM through alignment checklist:
1. Outcome: metric, baseline → target
2. Stakeholders: decision-maker, influencer, blocker
3. OKR alignment
4. Constraints: timeline, budget, team, tech
5. Success criteria
6. Kill criteria
7. User segment: who, how many, where
8. Available data: analytics, CJM, research, feedback
9. Tracker: Jira/Linear/GitHub/None + project key
10. Pipeline config: choose template or custom steps

After checklist — write CONTEXT.md and set pipeline_config in status.json.

---

## STEP 1 — `/analyze-cjm` (Core)

**Type**: Autonomous
**Input**: `CONTEXT.md` + `/CJM/` materials
**Output**: `output/hypotheses.md`
**PRD**: → §1, §2
**Skills**: `consulting-problem-solving` (MECE) + `user-persona-builder`

⚠️ Only PROBLEM hypotheses. No solutions.

**Readiness check** — before starting verify CONTEXT.md has:
- Metric + baseline (grounds hypotheses)
- Segment + size (assess Impact)
- "Why now" (justify Report)

If critical fields empty — ask PM, don't start.

**No CJM screenshots? Don't block.** Offer the PM 3 options:
- (a) "Describe the user journey in the chat — I'll work from your description (mark hypotheses INFERRED, confidence 0.3-0.5)"
- (b) "Take 5 minutes to capture screens — paste links or save to `CJM/` and I'll wait"
- (c) "Skip CJM analysis — go straight to /synthetic-research from CONTEXT.md alone"

Pick the path with the PM, then proceed.

1. Read `CONTEXT.md`
2. Analyze CJM materials if present (PNG/JPG directly, .fig via Figma MCP, .pdf via Read).
   If no CJM — work from PM's verbal description; mark each hypothesis as INFERRED.
3. For each step: what user sees, does, where friction occurs
4. Use MECE structure from `consulting-problem-solving`
5. Form 5-15 problem hypotheses in `output/hypotheses.md`
6. Create 2-3 initial personas from `user-persona-builder`
7. Add `## Blind spots` — what's unclear (especially valuable when no CJM was provided)
8. Fill PRD §1, §2

---

## STEP 2 — `/synthetic-research` (Recommended)

**Type**: Autonomous
**Input**: `CONTEXT.md` + `output/hypotheses.md`
**Output**: `research/synthetic-interviews.md` + updated hypotheses
**Skills**: `user-persona-builder`

⚠️ Only PROBLEM hypotheses. Don't ask about desired solutions.
Evidence typing: SYNTHETIC (confidence 0.2-0.4).

**Part A — applicability check:**
NOT applicable if: rare expertise needed, physical context matters, sensitive topic, high stakes.
→ If not applicable: Part C. If applicable: Part B.

**Part B — synthetic interviews:**
1. 4-5 personas: different patterns, context, experience
2. Problem interview: 5-7 questions per persona, "quotes"
3. Synthesis: patterns in 3+ personas → high priority
4. Update `output/hypotheses.md`

**Part C — real research task:**
Create `research/qual-research-brief.md` with justification + interview guide.

---

## STEP 3 — `/competitor-research` (Recommended)

**Type**: Autonomous
**Input**: `CONTEXT.md` + `output/hypotheses.md`
**Output**: `research/competitive-analysis.md` + `research/competitive/`
**PRD**: → §5
**Skills**: `consulting-problem-solving`

Look for **scenario analogues** — products where similar problem is solved.

1. 3-5 search queries (local + English)
2. WebSearch: competitors, analogous scenarios, best practices
3. For each: name, scenario, mechanism, link, insight
4. Materials in `research/competitive/`, summary in `research/competitive-analysis.md`
5. Show PM, ask what to add
6. Fill PRD §5

---

## STEP 4 — `/generate-research` (Recommended)

**Type**: Autonomous
**Input**: `CONTEXT.md` + `output/hypotheses.md`
**Output**: `research/analytics-brief.md` + `research/survey-questions.md`
**Skills**: `funnel-analysis-builder` + `product-analytics-setup` + `usability-test-plan`

1. For each hypothesis — what data needed
2. `research/analytics-brief.md`: goals, metrics, funnels, event schema
3. `research/survey-questions.md`: screening + problem block, ≤12 questions, sample size
   - Don't ask "would you like feature X"

**Tracking**: activate `pending.analytics_brief` and `pending.survey_brief`.

---

## STEP 5 — `/create-survey-audience` (Optional)

**Type**: Autonomous
**Input**: `research/survey-questions.md`
**Output**: `research/survey-audience-brief.md`
**Skills**: `funnel-analysis-builder` + `product-analytics-setup`

1. Translate screening questions into behavioral analytics signals
2. `research/survey-audience-brief.md`: criteria, period, format, SQL pseudocode

**Tracking**: activate `pending.audience_brief`.

---

## STEP 5.5 — Customer Research Pause (Recommended)

**Type**: Pause — PM conducts real research
**Output**: `research/analytics-data.md` + `research/survey-results.md` + `research/interview-notes.md`

PM conducts real research: analytics, survey, 5-8 interviews (Teresa Torres).
Dashboard tracks pending items. Resume at step 6 when data arrives.

---

## STEP 6 — `/validate-problems` (Core)

**Type**: Autonomous (when data arrives)
**Input**: `output/hypotheses.md` + research data
**Output**: `output/validated-hypotheses.md`
**PRD**: → §3, §4
**Skills**: `funnel-analysis-builder` + `consulting-problem-solving` + `multi-source-signal-synthesiser`

Three sub-steps (PM chooses how many):

**6a. Quick signal** (Core) — analytics confirm/deny?
- Input: analytics-data.md → confidence REAL 0.6-0.8

**6b. Survey validation** (Recommended) — quantitative
- Input: survey-results.md → confidence REAL 0.8-0.9

**6c. Interview validation** (Optional) — qualitative depth
- Input: interview-notes.md → confidence REAL 0.9-1.0

For each hypothesis: ✅/❌/⚠️, evidence, recalculated SIF.
Pyramid principle: data → insight → conclusion → recommendation.

**Branching**: confirmed → step 7 | partially → narrow | none → step 1 | insufficient → repeat

---

## STEP 7 — `/solution-hypotheses` (Core)

**Type**: PM chooses
**Input**: `output/validated-hypotheses.md`
**Output**: `output/solution-hypotheses.md`
**PRD**: → §6
**Skills**: `product-discovery-template`

1. For each ✅ problem: 2-3 solution hypotheses with assumption map
2. Comparative table with ICE, top-1 recommendation
3. Business viability check per hypothesis:
   - Unit economics, cannibalization, dependencies, compliance, effort S/M/L
4. Fill PRD §6

---

## STEP 8 — `/sketch-solution` (Core)

**Type**: Hybrid — autonomous draft + optional PM handoff
**Input**: `output/solution-hypotheses.md`
**Output**: `output/design-prototype-brief.md`, `design/prototype-draft.html`, `output/solution-sketch.md`
**PRD**: → §6 update, §7
**Skills**: `ui-pattern-library`

The step is a **sketchable, tool-agnostic prototype engine** with a soft gate. It reads
`design_config` from `status.json` and adapts; Claude Design is the recommended default, not a
hard dependency.

**Read `design_config` first** (block in `status.json`, next to `pipeline_config`):
`renderer` (claude-design | html | figma | text), `fidelity` (lofi | hifi),
`platform`, `scope` (single | flow | ask), `design_system` (generate | tokens-file | figma-lib),
`variants`.
- **Backward compatible**: if there is no `design_config` block, use the template defaults; a
  missing `pending.design_export` is not an error — never crash on old initiatives.
- Defaults inherit: `pm-profile.md` Design preferences → `design_config` (initiative override) →
  ask at runtime only when a field is `ask`. If `scope: ask`, ask the PM:
  "Top-1 hypothesis, or a multi-screen flow across the top 2–3?"
- `renderer: text` → legacy text-only behavior (no HTML). `renderer: figma` → Figma MCP branch
  (if connected).

### 8a — autonomous (never stalls the pipeline)
1. Select UI patterns (`ui-pattern-library`) and generate **two artifacts**:
   - `output/design-prototype-brief.md` — fill placeholders from `design_config` + hypotheses + tokens.
   - `design/prototype-draft.html` — a self-contained draft prototype on those tokens.
2. Create/update `output/solution-sketch.md`: screens, elements, user flow, screen→S[N]→patterns table.
3. PM sees a result immediately — the step is complete even with no handoff.

### Handoff (soft gate — encouraged, not blocking)
PM takes the brief + draft into the renderer (Claude Design: web-capture, inline knobs, share
links → export to `design/prototype.html`). Activate `pending.design_export` as a **soft** reminder;
correct degradation if skipped (draft remains current). On `design ready: <link>` → close it.

### 8b — fold back in
"Current prototype" = `design/prototype.html` if present, else `design/prototype-draft.html` (the
export supersedes the draft; the draft is kept as fallback). `solution-sketch.md` always links to
the current one. Update PRD §6, fill §7.

---

## STEP 8.5 — `/user-test-concept` (Optional)

**Type**: Pause — PM conducts test
**Input**: `output/solution-sketch.md`
**Output**: `research/concept-test-results.md`
**Skills**: `user-test-concept`

Generate: concept test scenario (15 min, 3-5 users), questions per screen, success/fail criteria.
PM conducts → enters results → hypotheses updated with REAL evidence.

---

## STEP 9 — `/review-design` (Recommended)

**Type**: PM comments
**Input**: comments + `output/solution-sketch.md`
**Output**: updated `output/solution-sketch.md`
**Skills**: `design-critique-template`

1. Comments from chat or `output/design-comments.md`
2. Run through heuristics
3. Update, add `## Changelog`

---

## STEP 10 — `/create-presentation` (Core) — Problem Research Report

**Type**: Autonomous
**Input**: `output/PRD.md` + `output/solution-sketch.md` + `research/competitive-analysis.md`
**Output**: `output/presentation.md` + `output/presentation.pptx`
**Skills**: `strategic-narrative-generator`

Read template: `template/slides/Problem Research Report Template.pptx.pdf` (if exists).

Structure: Title → Context → Problem → AS IS → Hypothesis → Solution → Estimate

For each slide: title, bullets, speaker notes, sources.
After `presentation.md` run `python3 tools/scripts/generate-pptx.py {initiative-folder}`.
If the script fails (no `python-pptx`), tell PM: "PPTX generation needs `pip install python-pptx`. The markdown is ready at `output/presentation.md` — you can convert it manually or install python-pptx and re-run." Don't block.

**Tracking**: activate `pending.gate1_challenge`.

---

## STEP 11 — `/create-design-brief` (Recommended)

**Type**: Autonomous → Pause
**Output**: `output/design-brief.md` + (optional) `output/ux-research-brief.md`
**Skills**: `usability-test-plan`

**Tracking**: activate `pending.design_brief`.

---

## STEP 12 — `/estimate-with-dev` (Core)

**Type**: Pause — dev lead fills
**Output**: `output/dev-estimate.md`
**PRD**: → §9, §10
**Skills**: `system-design-doc` + `technical-spec-document`

---

## STEP 13 — `/finalize-prd` (Core)

**Type**: Autonomous
**Output**: updated `output/PRD.md`
**Skills**: `product-requirements-doc` + `user-story-generator`

Fill §8 (User Stories), §11 (Open questions). Check consistency. Status → Review.

---

## STEP 14 — `/design-ab-test` (Recommended)

**Type**: PM + analyst
**Output**: `output/ab-test-design.md`
**Skills**: `product-discovery-template` + `funnel-analysis-builder` + `product-analytics-setup`

Calculate: baseline, MDE, sample size, duration, segmentation, guardrails, decision criteria.

---

## STEP 15 — `/create-gate2-presentation` (Core) — Solution Research Report

**Type**: Autonomous
**Output**: `output/gate2-presentation.md` + `output/gate2-presentation.pptx`
**Skills**: `strategic-narrative-generator`

Read template: `template/slides/Solution Research Report Template.pptx.pdf` (if exists).

Structure: Title → Hypothesis → Solution context → Solution → Demo → UX test → Experiment → Estimate

**Tracking**: activate `pending.gate2_challenge`.

---

## `/create-tickets` (after Solution Research Report)

**Type**: Autonomous → PM confirms → Push via MCP
**Input**: `output/PRD.md` + `output/solution-sketch.md` + `output/dev-estimate.md`
**Output**: `output/tickets.md` + tickets in tracker (if MCP connected)
**Skills**: `user-story-generator`

**Phase A — Generate markdown:**
1. Read PRD §6-8, dev estimate, solution sketch
2. Structure by tracker (CONTEXT.md → Tracker field): Jira (Epic→Story→Sub-task), Linear (Project→Issue→Sub-issue), GitHub (Milestone→Issue→Tasks)
3. Each ticket: title, user story, acceptance criteria, priority, estimate, dependencies, component
4. Write to `output/tickets.md` — show PM for review

**Phase B — Push via MCP (after PM confirms):**
1. Detect MCP: jira tools → Jira API; linear tools → Linear; gh CLI → GitHub Issues
2. Create parent first, then children with references
3. Save tracker URLs to `output/tickets.md`
4. If no MCP → inform PM, suggest setup (see Tracker integration section in README.md)

---

## STEP 16 — `/analyze-ab-test` (Recommended)

**Type**: Pause (waiting for AB test data) → Autonomous (when data arrives)
**Input**: `output/ab-test-design.md` + `research/ab-test-results.md` (raw test data from analyst)
**Output**: `output/ab-test-analysis.md`
**Skills**: `funnel-analysis-builder` + `multi-source-signal-synthesiser`

**External dependency** (optional): if PM has [pm-skills](https://github.com/phuryn/pm-skills) installed, prefer `pm-data-analytics:ab-test-analysis` skill or `/analyze-test` command — it has dedicated stat-sig validation tooling.

When the AB test concludes and data is in `research/ab-test-results.md`, analyze:
1. **Statistical significance**: p-value, confidence interval, sample size validation. Flag if underpowered.
2. **Primary metric**: did it move? Effect size, vs MDE from `ab-test-design.md`.
3. **Guardrails**: did any guardrail metric break? (engagement, churn, error rate, performance)
4. **Segments**: where did it work / not work? Heterogeneous treatment effects.
5. **Counter-metrics**: did anything we feared moved against us?
6. **Decision**: **Ship / Extend / Stop / Iterate** — with explicit reasoning tied to the win criteria from the design.

Evidence typing: REAL, confidence 0.7-0.95 (depending on sample size and stat-sig).

**Branching**:
- Ship → proceed to step 17 `/plan-gtm`
- Extend (need more power) → wait, re-analyze later
- Iterate (partial signal) → back to step 7 with refined hypothesis
- Stop → write retrospective to `output/decisions.md`, mark initiative as `archived` in status.json

**Tracking**: close `pending.ab_test_analysis` if active.

---

## STEP 17 — `/plan-gtm` (Core)

**Type**: Autonomous → PM reviews
**Input**: `output/PRD.md` + `output/ab-test-analysis.md` (if present) + `CONTEXT.md`
**Output**: `output/gtm-plan.md`
**Skills**: `strategic-narrative-generator` (for narrative structure)

GTM plan for **rolling out to existing product users** (this is not net-new product launch — existing users are getting a new feature/initiative).

**External dependency** (optional): if PM has [pm-skills](https://github.com/phuryn/pm-skills) installed, leverage their `pm-go-to-market:gtm-strategy`, `beachhead-segment`, `ideal-customer-profile` skills, or run `/plan-launch` first and adapt.

Plan must cover:

1. **Activation segment**: which subset of current users gets this first? (cohort, behavior, plan tier, geo)
   - Beachhead: smallest segment that proves the value
   - Expansion path: how we go from beachhead → broader rollout
2. **Value proposition for current users**: why should they care? (one sentence, then 3 bullet expansion)
   - Pain it solves for them specifically (different from net-new user value prop)
   - What changes in their workflow
3. **Rollout plan**: phased vs full
   - Phase 1: % users (or named cohort), success criteria, decision gate
   - Phase 2: expansion criteria
   - Full rollout: when, who decides
   - Kill switches: when to pause
4. **Channels** for activation (where current users will encounter the feature):
   - In-app: notification, banner, modal, tooltip, empty state
   - Lifecycle: email, push, SMS
   - Owned: blog, changelog, help center
   - Direct: CSM/sales for high-touch accounts
5. **Success metrics**:
   - Adoption rate (target % of activation segment using feature within X days)
   - Activation funnel (saw → tried → repeated)
   - Retention impact (does it improve the broader retention metric)
   - Counter-metrics to watch (drop in primary engagement, support load)
6. **Risk mitigation**:
   - What if adoption is lower than expected — escalation plan
   - What if support load spikes — staffing plan
   - What if guardrails break — rollback procedure

Show plan to PM for review. After approval, proceed to step 18.

---

## STEP 18 — `/create-gtm-materials` (Recommended)

**Type**: Autonomous → PM reviews each artifact
**Input**: `output/gtm-plan.md` + `output/PRD.md` + `output/solution-sketch.md`
**Output**: `output/gtm-materials.md` (index) + individual material files in `output/materials/`
**Skills**: `ab-test-announcement-wizard` (for communication patterns) + `user-persona-builder` (to tailor copy per segment)

**External dependency** (optional): if PM has [pm-skills](https://github.com/phuryn/pm-skills) installed, leverage `pm-marketing-growth:value-prop-statements`, `positioning-ideas` for richer copy variants.

Generate the actual materials referenced in the GTM plan. For each channel in the plan, produce one ready-to-publish artifact:

1. **In-app**:
   - `output/materials/in-app-notification.md` — first-touch notification (1 line, 1 CTA)
   - `output/materials/in-app-feature-banner.md` — banner copy with persistent display
   - `output/materials/in-app-empty-state.md` — empty-state copy if feature has one
2. **Lifecycle**:
   - `output/materials/email-announcement.md` — subject lines (3 variants), body, CTA
   - `output/materials/push-notification.md` — push copy if applicable
3. **Owned**:
   - `output/materials/blog-post.md` — full blog/changelog entry with screenshots placeholders
   - `output/materials/help-center-article.md` — help doc explaining the feature
4. **Internal enablement**:
   - `output/materials/sales-enablement.md` — talking points for sales/CSM
   - `output/materials/support-faq.md` — anticipated questions + answers (subset of step 19 support brief)
5. **Press/External** (if applicable):
   - `output/materials/press-release.md` — only if this is a notable launch

Each material:
- Tailored to the segment from the GTM plan
- Includes alternative versions where relevant (A/B copy)
- References screenshots/assets needed (placeholders if not yet produced)
- Notes who owns the asset (PM, marketing, design, support)

**Tracking**: activate `pending.gtm_materials_review` until PM signs off.

---

## STEP 19 — `/support-task` (Optional)

**Type**: Autonomous → Pause
**Input**: `output/PRD.md` + `output/solution-sketch.md` + `output/ab-test-design.md` + `output/gtm-plan.md`
**Output**: `output/support-brief.md`

Create support brief: what's changing, who's affected, support scenarios (5-10), FAQ, limitations, timeline, PM contact.

**Tracking**: activate `pending.support_brief`.
