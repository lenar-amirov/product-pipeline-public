# Step 1: Define the Problem

The single most important step. A well-defined problem is half-solved. Produce a crisp problem statement that everyone would agree captures what we're actually trying to solve.

## INPUT Phase

Ask the user before writing anything:
1. "What's the situation? Walk me through what's happening."
2. "What would success look like?"
3. "What's in scope and out of scope?"
4. "Constraints — budget, timeline, politics, data availability?"
5. "Do you have an initial hypothesis about what's going on?"

Their language, emphasis, and framing should directly shape the deliverable.

## Deliverable: Problem Definition Document (.md)

Contains: Context, Key Question, Scope, Success Criteria, Constraints, Stakeholders, Initial Hypotheses (1-3).

### Extracting the Key Question

Convert the user's situation description into a precise question — then present it for approval.

| User says | Key question pattern |
|-----------|---------------------|
| "Revenue is declining" | "What are the primary drivers of revenue decline, and what actions can reverse the trend within 12 months?" |
| "We need to enter a new market" | "Should we enter [market X], and if so, what is the optimal entry strategy?" |
| "Our costs are too high" | "How can we reduce operating costs by [X]% while maintaining service quality?" |
| "Employee turnover is killing us" | "What is driving attrition among [segment], and what interventions would reduce it to [target]%?" |

The key question always implies a decision or action. Push toward "What should we do?" not just "What's happening?" — but the user decides the framing.

### Scoping Discipline

Be explicit about: time horizon, geography, business scope, decision scope. If the user hasn't specified, do NOT assume — ask directly with options.

### Template

```markdown
# Problem Definition

## Context
[2-3 paragraphs: situation, stakeholder, what prompted this]

## Key Question
> [One clear, decision-oriented question]

## Scope
- **In scope**: [what we will address]
- **Out of scope**: [what we will not address]
- **Time horizon**: [timeframe]

## Success Criteria
[Specific, measurable where possible]

## Constraints
[Budget, timeline, data, political, regulatory]

## Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| [Name/Group] | [Decision maker / Influencer / Implementer] | [What they care about] |

## Initial Hypotheses
[1-3 preliminary hypotheses to test in later steps]
```

### Frontmatter Template

```yaml
---
id: 01-problem-definition
type: problem-definition
step: 1
title: "Problem Definition"
status: draft  # draft | approved | revised
addresses: null  # Step 1 is the root
entities:
  key_question:
    anchor: "01-problem-definition.md#kq"
    text: "[The key question verbatim]"
  hypotheses:
    - anchor: "01-problem-definition.md#hyp-[slug]"
      label: "[Hypothesis text]"
  success_criteria:
    - anchor: "01-problem-definition.md#sc-[slug]"
      label: "[Criterion text]"
      measure: "[How measured]"
---
```

## REVIEW Phase

Present the draft and ask for explicit review on: Key Question framing, Scope, Success criteria, Constraints, Initial hypotheses. Be ready for the user to completely rewrite the key question. **Do not proceed to Step 2 until explicitly approved.**

## Pitfalls

- **Too broad**: "How do we grow?" — push for specifics, let user decide which
- **Solution-first**: "Should we build a new app?" — back up to the problem
- **Assuming scope without asking**: Never fill in scope, time horizon, or geography without asking
- **Rushing past user input**: Extra time on framing saves enormous effort downstream
