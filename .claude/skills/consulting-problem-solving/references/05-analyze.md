# Step 5: Conduct Analyses

Execute the analyses from the work plan, test hypotheses, and build an evidence base. This step has the most back-and-forth — the user validates assumptions before each analysis and reviews results as they emerge.

## INPUT Phase (per analysis or batch)

1. "Key assumptions: I need to assume [X], [Y], [Z]. Reasonable? Better numbers?"
2. "Sensitivity ranges: [low/base/high]. Feel right?"
3. "Data gap: I don't have [X]. Use [proxy], or can you provide it?"
4. "Methodology: I'll approach this by [method]. Concerns?"

Do not proceed with an analysis if the user flags an assumption as unreasonable.

## Deliverables

1. **Analysis Workbook** (.xlsx): Summary tab (one row per analysis: name, finding, implication) + one tab per analysis + assumptions tab
2. **Findings Document** (.md): Narrative summary per the template below

## Execution Per Analysis

1. State the question, 2. Execute the analysis, 3. Apply "so what?" test, 4. Assess hypothesis (confirmed/partially/disproven), 5. Identify follow-up questions.

### Data Handling

**With user data**: Use xlsx skill, create clean workbook, document assumptions and transformations.
**Without data**: Do NOT silently estimate. For each assumption, present a suggested value with reasoning. Provide sensitivity ranges. Cite public sources. Ask if user has better internal data.

**Source tracking (mandatory)**: For every data point used in analysis, record the source (e.g., "Company 10-K, FY2024", "Bureau of Labor Statistics", "Management estimates", "Team analysis"). Include a `sources` column in the analysis workbook's assumptions tab. These sources will be carried through to Steps 6-8 and displayed on every final deliverable page/slide that quotes numbers.

### Data Quality and Consistency

Curate data ruthlessly — only numbers that earn their place should survive to Step 8.

- **Freshness**: Record the year. For fast-moving domains (AI, crypto, biotech), data older than 18 months is suspect. Flag or drop stale figures.
- **Cross-check**: Compare all numbers that will coexist in the deliverable. If figures imply contradictory stories (e.g., wildly different TAMs for similar industries), investigate, reconcile, or drop. Present unresolvable inconsistencies to the user.
- **Less is more**: Two solid, cross-validated data points beat ten scraped from different reports.
- **Insight first**: Lead findings with the strategic implication, not the number. Reframe "TAM is $4.2B" as "The market is large enough to support multiple entrants — estimated at ~$4B."

### Analysis Execution Guides

**Trend**: Chart over time, CAGR, inflection points. So what: accelerating, decelerating, or stable?
**Segmentation**: Break by dimensions, find outliers, calculate share of total. So what: where is concentration/variance?
**Benchmarking**: Compare to peers, normalize for scale, quantify gap. So what: how big is the gap, closing or widening?
**Financial Modeling**: Inputs → calculations → outputs, base + sensitivity cases, key metrics (NPV/IRR/payback). So what: does the economic case hold?
**Root Cause**: Drill into branches with data, quantify each branch's contribution, identify top 2-3 drivers.

## Findings Document Template

```markdown
# Analysis Findings

## Summary of Key Findings
| # | Finding | So What? | Confidence |
|---|---------|----------|------------|
| 1 | [What the analysis showed] | [Implication for key question] | High/Medium/Low |

## Detailed Findings
### Analysis 1: [Name]
**Question**: [What we were answering]
**Key Finding**: [What we learned]
**Supporting Evidence**: [Data points, workbook references]
**So What?**: [Meaning for key question]
**Hypothesis Status**: [Confirmed / Partially confirmed / Disproven]

## Emerging Themes
[Patterns across analyses — feed into Step 6]

## Open Questions
[New questions raised]

## Key Assumptions and Limitations
[What was assumed, what's missing, impact on confidence]
```

### Frontmatter Template

```yaml
---
id: 05-analysis-findings
type: analysis-findings
step: 5
title: "Analysis Findings"
status: draft
addresses: "01-problem-definition.md#kq"
findings:
  - anchor: "05-analysis-findings.md#f-1"
    label: "[Finding headline]"
    investigates: "04-work-plan.md#ax-ws1-a1"
    branch: "02-issue-tree.md#br-[slug]"
    confidence: high
hypothesis_status:
  - anchor: "05-analysis-findings.md#hs-[slug]"
    hypothesis: "01-problem-definition.md#hyp-[slug]"
    status: confirmed  # confirmed | disproven | partially_confirmed
    evidence: "05-analysis-findings.md#f-1"
    note: "[Brief explanation]"
---
```

## REVIEW Phase

Present findings as they emerge. Check against user's experience, surface hypothesis outcomes, flag unexpected patterns, validate interpretations.

**Handling corrections**: User may challenge assumptions (→ revise and re-run), dispute findings (→ investigate discrepancy), request deeper analysis, provide new data, or request a pivot. For any correction that changes a finding, re-present the updated result for approval.

**Pause and get direction**: After each P1 batch, when findings contradict hypotheses significantly, when judgment calls arise, when assumptions are heavy, before pivoting direction.

**Do not proceed to Step 6 until all key findings are reviewed and approved.**

## Pitfalls

- **Analysis without "so what?"**: A chart without insight is decoration
- **False precision**: Round appropriately
- **Confirmation bias**: If analysis disproves your hypothesis, that's valuable — don't bury it
- **Silent assumptions**: Never estimate without asking the user first
- **Not re-presenting after corrections**: Always show the updated version
