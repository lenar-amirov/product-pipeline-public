# Step 6: Synthesize Findings

Synthesis is not summary. Summary says "here's what we found." Synthesis says "here's what it all means together." Take individual findings and weave them into a coherent narrative answering the key question.

## INPUT Phase

1. "Any context or interpretive lens I should apply?"
2. "Looking at the findings, what jumps out as most important?"
3. "Any findings that surprised you or contradicted expectations?"
4. "How will your stakeholders react to these findings?"
5. "Any findings to present cautiously or frame carefully?"

Their answers shape what to lead with, emphasize, and qualify.

## Deliverable: Synthesis Document (.md)

Contains: The answer (1-2 sentences), Supporting logic (3-5 insights), Evidence base, Uncertainties and risks.

## The Synthesis Process

1. **Lay out all findings** together. Look for patterns, reinforcement, contradictions, overall story.
2. **Build the "so what?" chain**: Finding A + B → Insight 1; Insight 1 + 2 → Answer to Key Question.
3. **Stress-test the answer**: Completeness, evidence strength, counterarguments, actionability.

### Synthesis Patterns

- **Convergent**: Multiple independent findings point to same conclusion (strongest case)
- **Tension**: Findings point different directions; synthesis resolves the tension
- **Sequencing**: Findings suggest time-ordered actions rather than single answer
- **Conditional**: Answer depends on unresolved uncertainty

## Output Template

```markdown
# Synthesis: [Key Question]

## The Answer
> [1-2 sentence direct answer with appropriate confidence]

## Supporting Logic

### Insight 1: [Headline]
[2-3 sentences] **Evidence**: [Key data points]

### Insight 2: [Headline]
[2-3 sentences] **Evidence**: [Key data points]

## How the Pieces Fit Together
[1-2 paragraphs: logical chain, how insights build on each other]

## What Could Make Us Wrong
| Risk / Uncertainty | Likelihood | Impact on Answer | Mitigation |
|-------------------|------------|-----------------|------------|
| [Risk] | [H/M/L] | [How it changes answer] | [What to do] |

## Confidence Assessment
- **Overall**: [High/Medium/Low]
- **Strongest part**: [Best-supported insight]
- **Weakest part**: [Where evidence is thinnest]
- **What would increase confidence**: [Additional data needed]
```

### Frontmatter Template

```yaml
---
id: 06-synthesis
type: synthesis
step: 6
title: "Synthesis"
status: draft
addresses: "01-problem-definition.md#kq"
synthesizes:
  - "05-analysis-findings.md#f-1"
  - "05-analysis-findings.md#f-2"
the_answer:
  anchor: "06-synthesis.md#ans"
  text: "[1-2 sentence answer]"
insights:
  - anchor: "06-synthesis.md#ins-[slug]"
    label: "[Insight headline]"
    supported_by:
      - "05-analysis-findings.md#f-1"
confidence_assessment:
  overall: medium
  strongest: "[Best-supported insight]"
  weakest: "[Where evidence is thinnest]"
validates:
  - criterion: "01-problem-definition.md#sc-[slug]"
    met: true  # true | false | partial
    note: "[How validated]"
---
```

## REVIEW Phase

Present proposed answer and narrative. Always offer at least one alternative interpretation. Check for missing organizational context. Calibrate confidence together. Address tensions between findings.

The user may redirect: adjust framing, restructure around a different insight, challenge an insight. **Do not proceed to Step 7 until explicitly approved** — the synthesis is the foundation for recommendations.

## Pitfalls

- **Summary masquerading as synthesis**: Create meaning beyond individual findings
- **Burying the lead**: State the answer upfront
- **Overconfidence**: If evidence is mixed, say so
- **Ignoring contradictory evidence**: Address it explicitly
- **Dismissing user's alternative reading**: Take it seriously — they may be right
