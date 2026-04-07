# Step 3: Prioritize

Identify which branches matter most — where to focus analytical effort for maximum insight. You cannot and should not analyze everything equally.

## INPUT Phase

1. "Where does your gut tell you the biggest impact lies?"
2. "Any branches you want to analyze regardless of the framework?"
3. "Any branches you already know the answer to?"
4. "What data do you have easy access to? What would be hard to get?"
5. "Any branches to explicitly park?"

The user's suggested priorities carry heavy weight — not rubber-stamped, but strong signal.

## Deliverable: Priority Matrix Document (.md)

Contains: Priority assessment of each branch, Focus areas (2-3 for deep analysis), Parking lot with rationale, Resource allocation guidance.

## Impact × Feasibility Framework

For each branch, assess:

**Impact** (High/Medium/Low): How much would resolving this move the needle?
**Feasibility** (High/Medium/Low): Can we get useful answers given constraints?

| | High Impact | Medium Impact | Low Impact |
|--|------------|---------------|------------|
| **High Feasibility** | **P1** — Do first, deeply | P2 — If time allows | Skip |
| **Medium Feasibility** | **P1** — Worth the effort | P3 — Only if critical | Skip |
| **Low Feasibility** | P2 — Find proxies | Skip | Skip |

**High-priority signals**: Large share of total, recent change, high variance across segments, stakeholder emphasis, strong hypothesis, user-designated.

**Deprioritize signals**: Small magnitude, already well-understood, outside scope, intractable data/influence.

## Output Template

```markdown
# Prioritization: [Key Question]

## Priority Assessment
| Issue Branch | Impact | Feasibility | Priority | Rationale |
|-------------|--------|-------------|----------|-----------|
| [Branch] | High | High | **P1** | [Why] |

## Focus Areas (Deep Analysis)
### 1. [Top priority]
- **Why**: [1-2 sentences]
- **Hypothesis to test**: [From Step 2]
- **Estimated effort**: [Rough sense]

## Parking Lot
- [Branch X]: [Why deprioritized]

## Implications for Work Plan
[Brief note on what this means for Step 4]
```

### Frontmatter Template

```yaml
---
id: 03-priority-matrix
type: priority-matrix
step: 3
title: "Priority Matrix"
status: draft
addresses: "01-problem-definition.md#kq"
prioritizes:
  - "02-issue-tree.md#br-[slug]"
focus_areas:
  - anchor: "03-priority-matrix.md#fa-[slug]"
    label: "[Focus area]"
    tier: P1
    branch: "02-issue-tree.md#br-[slug]"
parked:
  - branch: "02-issue-tree.md#br-[slug]"
    reason: "[Why]"
---
```

## REVIEW Phase

Present proposed prioritization, explicitly compare to user's input, confirm data availability for P1 branches, confirm parking lot. **Do not proceed to Step 4 until explicitly approved.** If the user reprioritizes — even contradicting the framework — make the changes. The partner's judgment on priorities is final.

## Pitfalls

- **Everything is P1**: More than 3-4 P1 items means you haven't prioritized — force-rank
- **Prioritizing easy over impactful**: High feasibility + low impact is a trap
- **Deprioritizing without asking**: Never park a branch without user agreement
- **Ignoring user input**: If the partner said it matters, it matters
