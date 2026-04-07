# Step 2: Structure the Problem

Decompose the key question into a MECE set of sub-issues. The output is an issue tree — the analytical backbone of the engagement.

## INPUT Phase

1. "How would you structure this problem? Do you have a framework in mind?" — If they say "you pick," present 2-3 options with trade-offs and a recommendation. The user's choice is final.
2. "Are there dimensions that absolutely need to be in the tree?"
3. "How deep should we go? High-level (2 levels) or detailed (3-4 levels)?"

## MECE: The Core Discipline

**Mutually Exclusive**: No overlap between branches. **Collectively Exhaustive**: No gaps.

Test: "If I answered every leaf node, would I have a complete answer to the key question?" (CE) and "Could any data point belong to more than one branch?" (ME).

## Common Frameworks

Present as options — don't force-fit. Sometimes a custom structure is better.

### Profitability
```
Why is profitability declining?
├── Revenue issues
│   ├── Volume decline (market shrinkage, share loss)
│   └── Price/mix deterioration (pricing pressure, mix shift)
└── Cost issues
    ├── Variable costs (materials, labor, manufacturing efficiency)
    └── Fixed costs (headcount, real estate, overhead)
```

### Market Entry
```
Should we enter Market X?
├── Market attractiveness (size/growth, profitability, competitive dynamics)
├── Our ability to win (capabilities fit, leverageable assets, gaps)
└── Economic case (investment, returns NPV/IRR, risk)
```

### Operational Improvement
```
How can we reduce costs by X%?
├── Quick wins 0-6mo (procurement, process waste, discretionary spend)
├── Medium-term 6-18mo (org redesign, automation, supply chain)
└── Structural 18+mo (footprint, outsourcing, business model)
```

### Customer / Growth
```
How do we grow revenue by X%?
├── Grow existing customers (frequency, basket size, reduce churn)
├── Acquire new customers (segments, channels, geography)
└── New products/services (adjacent, innovation, M&A)
```

### Custom Tree

Start from key question → 2-4 Level 1 branches → recurse → stop when branches can be answered with specific analysis (usually 2-3 levels) → MECE-check at every level.

## Hypothesis Generation

For each major branch, form a hypothesis that is **specific**, **testable**, and **actionable**. Present to the user — they often have stronger hypotheses from domain knowledge.

## Output Template

```markdown
# Issue Tree: [Key Question]

## Framework Used
[Name and why — reference user's choice]

## Tree Structure
[Indented tree using ├── └── │ notation]

## Hypotheses
| Branch | Hypothesis | How to Test |
|--------|-----------|-------------|
| [Branch] | [Specific hypothesis] | [Analysis approach] |

## MECE Check
- **Mutually Exclusive**: [Confirmation]
- **Collectively Exhaustive**: [Confirmation]
```

### Frontmatter Template

```yaml
---
id: 02-issue-tree
type: issue-tree
step: 2
title: "Issue Tree"
status: draft
addresses: "01-problem-definition.md#kq"
decomposes: "01-problem-definition.md#kq"
branches:
  - anchor: "02-issue-tree.md#br-[slug]"
    label: "[Branch name]"
    level: 1
    children:
      - anchor: "02-issue-tree.md#br-[slug]"
        label: "[Sub-branch]"
        level: 2
hypotheses:
  - anchor: "02-issue-tree.md#bh-[slug]"
    label: "[Hypothesis]"
    branch: "02-issue-tree.md#br-[slug]"
    testable_by: "[Analysis approach]"
---
```

## REVIEW Phase

Present for review: framework validation, branch validation, depth check, hypotheses review, MECE check together. If the user wants to change the framework entirely, rebuild. **Do not proceed to Step 3 until explicitly approved.**

## Pitfalls

- **Too many branches**: Level 1 should have 3-5 branches max — consolidate if more
- **Not MECE**: Test rigorously at every level
- **Too shallow** (<2 levels) or **too deep** (>4 levels gets into analysis territory)
- **Framework worship**: Let the problem drive the structure, not vice versa
- **Overriding the user's framework choice**: Build what they chose, even if you'd choose differently
