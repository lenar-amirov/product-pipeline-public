---
name: strategic-narrative-generator
description: Generates the strategic story connecting your roadmap to company
  goals in a form non-technical stakeholders can repeat. Also structures Gate
  presentation narratives with source-backed claims. Use when user needs to
  "explain the roadmap", "present strategy to leadership", "create a narrative
  for all-hands", "build Problem Research Report", "build Solution Research Report",
  or "make the roadmap tell a story".
metadata:
  author: Mohit Aggarwal
  version: 2.0.0
  category: roadmapping
  tags: [strategy, roadmap, executive-communication, narrative, presentations, gate]
---
# Strategic Narrative Generator Skill

## Purpose
Turn a prioritised initiative list into a strategic narrative — the story that
explains not just what you're building but why, why now, and why this sequence.
The kind of narrative a board member can repeat back correctly after one hearing.

Also structures Gate presentation narratives where every claim must be backed by
a specific source from research and output artifacts.

## Required Inputs
- Prioritised initiative list (with rough timelines)
- Current OKRs or strategic priorities (1-3)
- Competitive or market context (optional but improves output significantly)

## Process
1. Read the initiative list and identify 2-3 natural strategic themes
2. For each theme: articulate the problem it addresses, the customer it serves,
   and the metric it moves
3. Build the progression narrative: how does Q1 set up Q2? How does H1 set up H2?
4. Write executive summary in under 100 words (the version someone can repeat)
5. Anticipate the 3 hardest questions a sceptical board member would ask —
   and draft answers
6. Identify what's NOT on the roadmap and why (this builds credibility)

## Output Format

### Product Strategy Narrative: [Period]

**The One-Paragraph Context:**
[Market moment + key challenge + our response — for the CFO, not the engineer]

**Strategic Theme 1: [Name]**
- The problem: [customer pain in plain language]
- Our response: [initiatives in this theme]
- The metric it moves: [specific and measurable]
- Why now: [timing rationale]

**Strategic Theme 2: [Name]**
[Same structure]

**The Progression Story:**
[How each quarter sets up the next — this is the narrative arc]

**Executive Summary (under 100 words — shareable):**
[Version someone can quote at a board meeting]

**Questions to Prepare For:**
1. [Hard question] -> [Prepared answer]
2. [Hard question] -> [Prepared answer]
3. [Hard question] -> [Prepared answer]

**What's Not on the Roadmap (and Why):**
[2-3 items — shows strategic discipline, not just prioritisation]

## Tone Rules
- Write for a CFO, not an engineer
- Lead with outcomes, not features
- Every sentence should answer "so what?"
- Avoid jargon — if you can't say it plainly, the strategy isn't clear enough yet

---

## Report Presentation Narratives (Steps 10 and 15)

### Problem Research Report Structure (Step 10: /create-presentation)

**Purpose**: Convince stakeholders the problem is real, validated, and worth solving.

```markdown
## Slide 1: Title
[Initiative name + PM name + date]

## Slide 2: Context
- Where this task comes from (OKR, user feedback, data signal)
- Why now (what changed)
- **Source**: CONTEXT.md — "Why now" field

## Slide 3: Problem
- Problem thesis (one sentence)
- Who's affected: segment + size
- Signal strength: how many sources confirm this
- **Sources**: hypotheses.md, validated-hypotheses.md

## Slide 4: AS IS Scenario
- Current user behavior (from CJM analysis)
- Pain points with evidence
- Quotes from research (if REAL) or synthetic insights (marked)
- **Sources**: CJM/ materials, synthetic-interviews.md, interview-notes.md

## Slide 5: Hypothesis
- Formula: "If [X], then [Y], because [Z], metric [M] +[N%]"
- Confidence level with evidence type breakdown
- **Sources**: solution-hypotheses.md

## Slide 6: Solution
- Job-to-be-done
- Key screens / user flow (from solution-sketch.md)
- Use cases: 2-3 concrete scenarios
- **Sources**: solution-sketch.md, competitive-analysis.md

## Slide 7: Estimate
- Timeline and effort
- Key risks and dependencies
- What we need to proceed (Gate decision)
- **Sources**: CONTEXT.md constraints, dev-estimate.md (if available)
```

**Speaker notes template for each slide:**
```markdown
### Speaker Notes — Slide [N]: [Title]
**Key message** (say this first): [One sentence the audience should remember]
**Supporting points**: [2-3 bullets to elaborate]
**Anticipated question**: [What someone might ask here]
**Answer**: [Prepared response with source]
**Transition**: [How to move to next slide]
```

### Solution Research Report Structure (Step 15: /create-gate2-presentation)

**Purpose**: Convince stakeholders the solution is ready for development and testing.

```markdown
## Slide 1: Title
[Initiative name + PM name + date]

## Slide 2: Hypothesis Recap
- Formula from Problem Research Report
- Metrics: primary + guardrail + proxy
- Target audience and size
- **Sources**: solution-hypotheses.md, PRD.md §3

## Slide 3: Solution Context (AS IS)
- Current user journey + pain points (recap)
- What changed since Problem Research Report (new data, design feedback)
- **Sources**: validated-hypotheses.md, concept-test-results.md

## Slide 4: Solution Design
- Job-to-be-done
- Key screens / mockups (from designer or wireframes)
- User flow
- **Sources**: solution-sketch.md, design-brief.md

## Slide 5: Demo
- Live demo or clickthrough of key screens
- [PM presents this live — slides as backup]

## Slides 6-7: UX Test Results (if conducted)
- Methodology: who, how many, how
- Key findings: what worked, what didn't
- Changes made based on feedback
- **Sources**: concept-test-results.md, ux-research-brief.md

## Slide 8: Experiment Design
- AB test parameters: baseline, MDE, sample, duration
- Guardrail metrics
- Decision criteria: ship / iterate / kill
- **Sources**: ab-test-design.md

## Slide 9: Estimate & Timeline
- Dev effort (from dev lead)
- Dependencies and risks
- Proposed timeline: development -> AB test -> decision
- **Sources**: dev-estimate.md, PRD.md §9-§10
```

### Source Reference Rules

Every claim in a Gate presentation must include a source:
- **Format**: `[Source: filename.md]` or `[Source: filename.md, section]`
- **Evidence typing**: If the claim is based on SYNTHETIC data, mark it: `[Synthetic — needs validation]`
- **No unsourced claims**: If you can't trace a claim to a file, either find the source or remove the claim
- Qualitative data (interviews, synthetic) is illustration only — don't present as proof without quantitative backing
