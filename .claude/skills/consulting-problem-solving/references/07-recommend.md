# Step 7: Develop Recommendations

The synthesis told us what's happening and why. Now tell the stakeholder what to do. Good recommendations are specific, actionable, prioritized, and evidence-backed.

## INPUT Phase

1. "What strategic direction are you leaning toward?"
2. "Any options off the table?" — Organizational, political, practical constraints.
3. "Appetite for risk and change?"
4. "Who needs to approve? What do they care about?"
5. "Budget and timeline for implementation?"
6. "Past initiatives or attempts to learn from?"

If the partner has a clear strategic preference, lead with it.

## Deliverable: Recommendation Brief (.md)

Contains: Core recommendation, Supporting recommendations, Implementation roadmap, Expected impact, Risks and mitigations.

## The SMART+E Test

Every recommendation must be: **Specific** (name the action), **Measurable** (target metrics), **Actionable** (feasible with available resources), **Relevant** (addresses key question, supported by analysis), **Time-bound** (milestones and deadlines), **Evidence-backed** (traces to Step 5 findings).

## Structuring Recommendations

### The Pyramid
```
Core Recommendation (the big move)
├── Supporting Rec A → Actions A1, A2
├── Supporting Rec B → Actions B1, B2
└── Supporting Rec C → Actions C1, C2
```

### Phasing
- **Immediate (0-3 months)**: Quick wins, no-regret moves, foundations
- **Near-term (3-12 months)**: Major initiatives, organizational changes
- **Medium-term (1-3 years)**: Structural changes, capability building

Each phase should deliver value independently.

### Quantifying Impact
For each: financial impact (range), effort required, payback period, confidence level.

## Presenting Options

Before finalizing, present 2-3 strategic directions with trade-offs:

**Option A: [Name]** — What it involves, Pros, Cons, Expected impact
**Option B: [Name]** — What it involves, Pros, Cons, Expected impact
**Option C: [Name]** — What it involves, Pros, Cons, Expected impact

"I'd lean toward Option [X] because [reasoning]. Which resonates?"

### Anticipate Objections

| Objection | Response |
|-----------|----------|
| "We tried this before" | What's different now |
| "Too risky" | Risk mitigation, benchmark evidence |
| "Too expensive" | ROI analysis, phased approach |
| "Politically difficult" | Stakeholder plan, quick wins for momentum |

## Output Template

```markdown
# Recommendations: [Key Question]

## Core Recommendation
> [1-2 sentence headline]
**Rationale**: [Link to synthesis] **Expected Impact**: [Quantified] **Confidence**: [H/M/L]

## Supporting Recommendations
### 1. [Title]
**What**: [Actions] **Why**: [Evidence] **Impact**: [Outcome] **Timeline**: [When] **Owner**: [Role]

## Implementation Roadmap
### Phase 1: [Name] (Months 0-3)
| Action | Owner | Milestone | Success Metric |
|--------|-------|-----------|----------------|

## Impact Summary
| Recommendation | Investment | Annual Impact | Payback | Confidence |
|---------------|-----------|---------------|---------|------------|

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

## Next Steps
[Immediate 3-5 actions]
```

### Frontmatter Template

```yaml
---
id: 07-recommendations
type: recommendations
step: 7
title: "Recommendations"
status: draft
addresses: "01-problem-definition.md#kq"
core_recommendation:
  anchor: "07-recommendations.md#rec-core"
  label: "[Core recommendation]"
  supported_by:
    - "06-synthesis.md#ins-[slug]"
  traces_from: "06-synthesis.md#ans"
supporting_recommendations:
  - anchor: "07-recommendations.md#srec-1"
    label: "[Supporting rec]"
    supported_by:
      - "05-analysis-findings.md#f-1"
implementation_phases:
  - anchor: "07-recommendations.md#phase-1"
    label: "[Phase name]"
    timeline: "[0-3 months]"
---
```

## REVIEW Phase

Present options and let user choose. After selection, present full brief. Validate feasibility, co-develop phasing, validate impact estimates, anticipate objections together, confirm core recommendation. **Do not proceed to Step 8 until explicitly approved.**

## Pitfalls

- **Vague recommendations**: "Improve customer experience" is aspiration, not recommendation
- **Not evidence-backed**: Every rec must trace to analysis findings
- **Too many**: Stakeholders absorb 3-5 major recommendations — consolidate
- **No implementation path**: A rec without a roadmap is a wish
- **Presenting a single option**: Always give choices — the user knows their organization
