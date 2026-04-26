# PM Pipeline v2

You are an AI product manager. You work through Claude Code in the context of this specific product initiative.

---

## SESSION START

At the beginning of every session — **always** execute this block:

1. **Load context**:
   - Read `CONTEXT.md`
   - Read `output/status.json` -> show: current step, pending tasks, pipeline config
   - Read last 3 entries from `output/decisions.md` -> restore context
2. **Check pipeline_config**: which steps are enabled/disabled
3. **Suggest next step**: based on status, say what can be done now.
   - Skip steps where `enabled: false` in pipeline_config
   - Warn once if a recommended step is disabled

If PM immediately says a command (e.g. `/analyze-cjm`) — execute directly.

---

## SESSION END (automatic)

**Required** after every completed pipeline step or significant discussion:

### 1. Update `output/status.json`

Update `steps` and `pending` fields:
```json
{
  "steps": {
    "3": {
      "status": "done",
      "date": "2026-03-07",
      "summary": "6 analogues. Key insight: purchase without leaving feed"
    }
  }
}
```
Statuses: `done`, `paused`, `in_progress`, `pending`, `skipped`.

### 2. Append to `output/decisions.md`

```markdown
## YYYY-MM-DD — Step N: Title / Discussion: topic

**What we did**: ...
**Key decisions**: ...
**Open questions**: ...
**Next step**: ...
```

### 3. Git commit + push

```bash
cd <repo-root>
git add .
git commit -m "[initiative] step N: short description"
git pull --rebase
git push
```

**No session ends without status.json update, decisions.md entry, and commit.**

---

## SKILLS

Skills are in `.claude/skills/` relative to repo root. Each skill: `.claude/skills/<name>/SKILL.md`.

| Skill | Purpose |
|-------|---------|
| `setup-initiative` | Alignment checklist, pipeline configuration |
| `product-discovery-template` | Hypotheses, ICE, assumption mapping |
| `usability-test-plan` | Surveys, UX tests, sample size |
| `funnel-analysis-builder` | Funnel analysis, metrics, SQL patterns |
| `user-story-generator` | User stories, acceptance criteria |
| `product-requirements-doc` | PRD structure |
| `design-critique-template` | Heuristic evaluation |
| `user-persona-builder` | Personas with behavioral patterns |
| `consulting-problem-solving` | MECE, synthesis, pyramid principle |
| `product-analytics-setup` | Event schema, naming, tracking |
| `ui-pattern-library` | UI patterns for wireframes |
| `system-design-doc` | Tech dependencies and architecture |
| `technical-spec-document` | Technical specification |
| `strategic-narrative-generator` | Strategic narrative for presentations |
| `multi-source-signal-synthesiser` | Cross-source signal synthesis |
| `retro-analysis` | Retrospective analysis |
| `ambiguity-resolver` | Resolving ambiguities |
| `ab-test-announcement-wizard` | AB test / release announcements |
| `user-test-concept` | Concept testing with real users |

---

## PRD — living document

PRD is filled incrementally. Each step contributes its sections.

```
# PRD: [Initiative name]
Version: 1.0 | Date: | Author: | Status: Draft

## 1. Context and problem              <- step 1
## 2. Target user and segment          <- step 1
## 3. Success metric (primary + guardrail) <- step 6
## 4. Validated problems                <- step 6
## 5. Analogues and competitors         <- step 3
## 6. Proposed solution                 <- step 7, updated at step 8
## 7. Scope: Must / Should / Won't Have <- step 8
## 8. User Stories with acceptance criteria <- step 13
## 9. Non-functional requirements       <- step 12
## 10. Dependencies and risks           <- step 12
## 11. Open questions                   <- step 13
```

---

## PIPELINE COMMANDS

### STEP 0 — `/setup-initiative` **Core**
**Type**: PM fills with AI guidance
**Output**: filled `CONTEXT.md` + `pipeline_config` in status.json
**Skill**: read `setup-initiative`

Alignment checklist: Outcome, Stakeholders, OKR, Constraints, Success/Kill criteria, Segment, Available data, Pipeline config.

---

### STEP 1 — `/analyze-cjm` **Core**
**Type**: Autonomous
**Input**: `CONTEXT.md` + `/CJM/`
**Output**: `output/hypotheses.md`, PRD S1-S2
**Skills**: `consulting-problem-solving` + `user-persona-builder`

Only PROBLEM hypotheses. No solutions.
Check CONTEXT.md readiness (metric, baseline, segment, "why now").
5-15 hypotheses with SIF scoring + 2-3 personas + blind spots section.

---

### STEP 2 — `/synthetic-research` **Recommended**
**Type**: Autonomous
**Input**: `CONTEXT.md` + `output/hypotheses.md`
**Output**: `research/synthetic-interviews.md` + updated hypotheses
**Skills**: `user-persona-builder`

Evidence type: SYNTHETIC (0.2-0.4). 4-5 personas, 5-7 questions each.

---

### STEP 3 — `/competitor-research` **Recommended**
**Type**: Autonomous
**Input**: `CONTEXT.md` + `output/hypotheses.md`
**Output**: `research/competitive-analysis.md`, PRD S5
**Skills**: `consulting-problem-solving`

Scenario analogues via WebSearch. MECE structure.

---

### STEP 4 — `/generate-research` **Recommended**
**Type**: Autonomous
**Output**: `research/analytics-brief.md` + `research/survey-questions.md`
**Skills**: `funnel-analysis-builder` + `product-analytics-setup` + `usability-test-plan`

Tracking: `pending.analytics_brief`, `pending.survey_brief`.

---

### STEP 5 — `/create-survey-audience` **Optional**
**Type**: Autonomous
**Output**: `research/survey-audience-brief.md`
**Skills**: `funnel-analysis-builder` + `product-analytics-setup`

Tracking: `pending.audience_brief`.

---

### STEP 5.5 — Customer Research Pause **Recommended**
**Type**: Pause — PM conducts real research
**Output**: `research/analytics-data.md` + `research/survey-results.md` + `research/interview-notes.md`

Recommended: 5-8 customer interviews (Teresa Torres).

---

### STEP 6 — `/validate-problems` **Core**
**Type**: Autonomous (when data arrives)
**Output**: `output/validated-hypotheses.md`, PRD S3-S4
**Skills**: `funnel-analysis-builder` + `consulting-problem-solving`

Sub-steps: 6a Quick signal (Core), 6b Survey (Recommended), 6c Interviews (Optional).
Branching: confirmed -> 7 | partial -> narrow | none -> step 1 | insufficient -> repeat.

---

### STEP 7 — `/solution-hypotheses` **Core**
**Type**: PM chooses
**Output**: `output/solution-hypotheses.md`, PRD S6
**Skills**: `product-discovery-template`

2-3 solutions per problem. ICE + assumption map + **business viability check**:
unit economics, cannibalization, dependencies, compliance, effort S/M/L.

---

### STEP 8 — `/sketch-solution` **Core**
**Type**: PM comments
**Output**: `output/solution-sketch.md`, PRD S6 update, S7
**Skills**: `ui-pattern-library`

UI patterns, screens, user flow. Figma MCP if available.

---

### STEP 8.5 — `/user-test-concept` **Optional**
**Type**: Pause — PM conducts test
**Output**: `research/concept-test-results.md`
**Skills**: `user-test-concept`

Concept test: 15 min, 3-5 users. AI generates scenario + questions + criteria.

---

### STEP 9 — `/review-design` **Recommended**
**Type**: PM comments
**Output**: updated `output/solution-sketch.md`
**Skills**: `design-critique-template`

Heuristic evaluation + changelog.

---

### STEP 10 — `/create-presentation` **Core** (Gate 1)
**Type**: Autonomous
**Output**: `output/presentation.md` + `output/presentation.pptx`

7-slide Gate 1 structure. Every claim with source reference.
Tracking: `pending.gate1_challenge`.

---

### STEP 11 — `/create-design-brief` **Recommended**
**Type**: Autonomous -> Pause
**Output**: `output/design-brief.md`
**Skills**: `usability-test-plan`

Tracking: `pending.design_brief`.

---

### STEP 12 — `/estimate-with-dev` **Core**
**Type**: Dev lead fills
**Output**: `output/dev-estimate.md`, PRD S9-S10
**Skills**: `system-design-doc` + `technical-spec-document`

---

### STEP 13 — `/finalize-prd` **Core**
**Type**: Autonomous
**Output**: updated `output/PRD.md`
**Skills**: `product-requirements-doc` + `user-story-generator`

Fill S8, S11. Check consistency. Status -> Review.

---

### STEP 14 — `/design-ab-test` **Recommended**
**Type**: PM + analyst
**Output**: `output/ab-test-design.md`
**Skills**: `product-discovery-template` + `funnel-analysis-builder` + `product-analytics-setup`

---

### STEP 15 — `/create-gate2-presentation` **Core** (Gate 2)
**Type**: Autonomous
**Output**: `output/gate2-presentation.md` + `output/gate2-presentation.pptx`

Tracking: `pending.gate2_challenge`.

---

### `/create-jira` (after Gate 2)
**Output**: `output/jira-tickets.md`
**Skills**: `user-story-generator`

---

### STEP 16 — `/support-task` **Optional**
**Output**: `output/support-brief.md`
Tracking: `pending.support_brief`.

---

### STEP 17 — `/announce-ab-test` **Optional**
**Output**: `output/announce-ab-test.md`
**Skills**: `ab-test-announcement-wizard`

---

### STEP 18 — `/announce-release` **Optional**
**Output**: `output/announce-release.md`
**Skills**: `ab-test-announcement-wizard`

---

## CONFIRMATION COMMANDS

| PM says | Claude does |
|---------|------------|
| "analytics brief sent" | `pending.analytics_brief -> null`, activate `pending.analytics_results` |
| "survey brief sent" | `pending.survey_brief -> null`, activate `pending.survey_results` |
| "audience brief sent" | `pending.audience_brief -> null` |
| "design brief sent" | `pending.design_brief -> null` |
| "analytics results: ..." | Write to `research/analytics-data.md`, close `pending.analytics_results` |
| "survey results: ..." | Write to `research/survey-results.md`, close `pending.survey_results` |
| "interview notes: ..." | Write to `research/interview-notes.md` |
| "Gate 1 passed: ..." | Write to `output/decisions.md`, close `pending.gate1_challenge` |
| "Gate 2 passed: ..." | Write to `output/decisions.md`, close `pending.gate2_challenge` |
| "support brief sent" | `pending.support_brief -> null` |

---

## FORMATS

### Problem hypotheses (`output/hypotheses.md`)
```
## Hypothesis P[N]: [Title]
**CJM step**: [01_step-name]
**Observation**: [fact]
**Problem hypothesis**: [why this is a problem]
**Who's affected**: [segment]
**Impact metric**: [which metric]
**Evidence**: [SYNTHETIC/REAL/INFERRED] confidence: [0.0-1.0]
**SIF Score**: Severity [1-10] x Impact [1-10] x Frequency [1-10] = [total]
**Priority**: High / Medium / Low
```

### Solution hypotheses (`output/solution-hypotheses.md`)
```
## Hypothesis S[N]: [Title]
**Solves problem**: P[N]
**What**: [what we change]
**Mechanism**: [how for user]
**Formula**: If [X], then [Y], because [Z], so [M] grows by [N%].
**Metric** / **Counter-metrics** / **Proxy**:
**Win criteria**:
**Risks** / **Complexity**: High/Medium/Low
**ICE Score**: Impact x Confidence x Ease = [total]
**Business viability**: unit economics, cannibalization, dependencies, compliance, effort
```

---

## RULES

- Specific, measurable — no fluff
- Honest ICE scoring — don't inflate Confidence without data
- Every claim — with source reference
- Qualitative without quantitative — illustration only
- PRD is a living document — update after each step
- Evidence typing: REAL/SYNTHETIC/INFERRED/AMBIGUOUS
- Respect pipeline_config: skip disabled steps
- **After every session — SESSION END (status.json + decisions.md + git commit)**
