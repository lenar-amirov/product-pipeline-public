# Step 4: Build the Work Plan

Translate priorities into concrete analyses with clear outputs. This defines what gets done, what data is needed, and in what order.

## INPUT Phase

1. "What data do you have readily available?" — Critical; a plan without data is useless.
2. "Are there specific analyses your stakeholders expect to see?"
3. "Any timeline constraints or interim milestones?"
4. "Approach preferences for key analyses?"
5. "What estimation approach is acceptable where data is missing?" — Conservative vs. aggressive.

## Deliverable: Work Plan Spreadsheet (.xlsx)

Use the xlsx skill. Structure:

**Tab 1 — Summary**: Project name, key question, date, workstream overview table (name, # analyses, effort, milestone), timeline if specified.

**Tab 2 — Detailed Analysis Plan**: Columns: ID (WS1-A1 format), Workstream, Analysis Name, Question to Answer, Approach, Data Needed, Data Source, Data Status (Available/Needed/Gap), Output Format, Hypothesis, Priority, Dependencies, Status.

**Tab 3 — Data Inventory** (when applicable): Data Item, Source, Status (Have/Need/Unavailable), Format, Notes, Workaround if unavailable.

### Analysis Definition

Each analysis answers one specific question. Define: Workstream, Analysis name, Question, Approach, Data needed, Data source, Output, Hypothesis, Priority.

### Sequencing

Map dependencies: **Independent** (parallel), **Dependent** (needs prior output), **Gating** (must complete before deciding next steps).

### Typical Analysis Types

**Quantitative**: Trend, segmentation, benchmarking, sensitivity, financial modeling, regression/correlation.
**Qualitative**: Best practice review, process mapping, stakeholder analysis, risk assessment.

### Frontmatter Template (.md summary)

```yaml
---
id: 04-work-plan
type: work-plan
step: 4
title: "Work Plan"
status: draft
addresses: "01-problem-definition.md#kq"
plans_for:
  - "03-priority-matrix.md#fa-[slug]"
workstreams:
  - anchor: "04-work-plan.md#ws-[slug]"
    label: "[Workstream]"
    focus_area: "03-priority-matrix.md#fa-[slug]"
    analyses:
      - anchor: "04-work-plan.md#ax-ws1-a1"
        label: "[Analysis name]"
---
```

## REVIEW Phase

Validate analysis list, confirm data status, review approach choices, confirm sequencing, validate assumptions approach. **Do not proceed to Step 5 until explicitly approved.**

## Pitfalls

- **Too vague**: "Analyze the market" is not an analysis — specify the question, data, and method
- **Missing data plan**: Every analysis needs an identified data source
- **No sequencing**: Map dependencies to avoid rework
- **Over-planning**: 15-25 analyses is typical; >30 suggests insufficient prioritization
- **Assuming data availability**: Always confirm with the user first
