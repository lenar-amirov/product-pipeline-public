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
9. Pipeline config: choose template or custom steps
10. Tracker: Jira/Linear/GitHub/None + project key

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

1. Read `CONTEXT.md`
2. Analyze `/CJM/` materials in order (PNG/JPG directly, .fig via Figma MCP, .pdf via Read)
3. For each CJM step: what user sees, does, where friction occurs
4. Use MECE structure from `consulting-problem-solving`
5. Form 5-15 problem hypotheses in `output/hypotheses.md`
6. Create 2-3 initial personas from `user-persona-builder`
7. Add `## Blind spots` — what's unclear from CJM
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

**Type**: PM comments
**Input**: `output/solution-hypotheses.md`
**Output**: `output/solution-sketch.md`
**PRD**: → §6 update, §7
**Skills**: `ui-pattern-library`

1. Select UI patterns, create `output/solution-sketch.md`: screens, elements, user flow
2. Figma MCP if connected
3. Update PRD §6, fill §7

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
4. If no MCP → inform PM, suggest setup (see ONBOARDING.md)

---

## STEP 16 — `/support-task` (Optional)

**Type**: Autonomous → Pause
**Input**: `output/PRD.md` + `output/solution-sketch.md` + `output/ab-test-design.md`
**Output**: `output/support-brief.md`

Create support brief: what's changing, who's affected, support scenarios (5-10), FAQ, limitations, timeline, PM contact.

**Tracking**: activate `pending.support_brief`.

---

## STEP 17 — `/announce-ab-test` (Optional)

**Type**: Autonomous → PM publishes
**Input**: `output/PRD.md` + `output/ab-test-design.md`
**Output**: `output/announce-ab-test.md`
**Skills**: `ab-test-announcement-wizard`

Generate internal AB test announcement.

---

## STEP 18 — `/announce-release` (Optional)

**Type**: Autonomous → PM publishes
**Input**: `output/PRD.md` + AB test results
**Output**: `output/announce-release.md`
**Skills**: `ab-test-announcement-wizard` (adapt for release)

Generate internal release announcement.
