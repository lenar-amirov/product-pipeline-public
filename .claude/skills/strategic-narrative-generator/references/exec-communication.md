# Step 8: Communicate

Package all the work into a compelling deliverable. The best analysis is worthless if it isn't communicated clearly.

## INPUT Phase: Collect Communication Preferences

Use **AskUserQuestion** to collect 7-8 structured choices in 2-3 batches (up to 4 questions each).

### Batch 1: Visual Style, Narrative, Title

**Q1 — Visual Style** (header: "Visual Style"): Clean & Minimal / Data-Heavy / Visually Rich / Corporate/Branded (custom). **Ask this first** — visual style shapes every subsequent design decision.

**Q2 — Brand Styling** (header: "Brand", PowerPoint only): Check `references/styles/` for available profiles. Options: each found brand + "None (Recommended)" + "Custom." If selected, read the brand file and apply all specified properties. If "Custom," collect brand elements and create a new file from `references/brand-styling-template.md`.

**Q3 — Narrative Structure** (header: "Narrative", multiSelect: false):
1. **Answer-First (Pyramid)** — Lead with conclusion, support with arguments, then evidence. Best for: aligned/senior/time-constrained audiences.
2. **Evidence-First (Build)** — Observations → pattern → conclusion. Best for: skeptical audiences, counterintuitive conclusions.
3. **Narrative Arc (SCR)** — Situation → Complication → Resolution. Best for: persuasion, audiences that need to feel the problem first.
4. **Transformation (Current → Future → Bridge)** — As-is → to-be → path. Best for: change management, vision-setting.
5. **Comparative Evaluation (Options → Criteria → Rec)** — Alternatives → evaluation → selection. Best for: board decisions, vendor selections.
6. **Sequential / Process (Step-by-Step)** — Temporal/logical order. Best for: implementation plans, project updates.

**Q4 — Title and Subtitle** (header: "Title"): Auto-generate from problem statement, or user enters custom.

### Batch 2: Structure, Page Count, Appendix

**Q5 — Executive Summary** (header: "Exec Summary"): Yes (recommended) / No.

**Q6 — Context & Objectives** (header: "Context"): Yes (recommended) / No.

**Q7 — Content Pages** (header: "Page Count"): Compact (4-6) / Standard (8-12) / Comprehensive (15-20) / Custom. Count excludes title, exec summary, and context slides.

**Q8 — Appendix** (header: "Appendix"): Yes (recommended) / No.

### Follow-up Questions (conversational, after structured choices)

1. **Audience**: Who, what level, what they know
2. **Key message**: The one thing to remember
3. **Tone**: Bold/decisive vs. cautious/options-oriented
4. **Sensitive content**: Anything to frame carefully or put in appendix

## CRITICAL: No Literal Framework Labels

**Never use framework terminology as slide titles, section headers, or labels.** The frameworks shape structure — the audience sees only context-specific content.

Instead of "Situation" → describe the actual context. Instead of "Complication" → describe the actual disruption. Instead of "Resolution" → describe the actual solution. Instead of "Current State" / "Future State" / "Bridge" → describe what's happening, the vision, and the path. Instead of "The Options" / "Evaluation Criteria" → describe what's being compared and what criteria reflect.

**Exception**: "Executive Summary" is a standard navigational label and should be used as-is.

## Deliverable: .pptx or .docx

Use the pptx or docx skill accordingly.

### Assembly Order

```
1. Title Slide/Page                    ← ALWAYS
2. Executive Summary                   ← if Q3 = Yes
3. Context & Objectives                ← if Q4 = Yes
4. Content Pages (per narrative)       ← count from Q5
5. Appendix                            ← if Q6 = Yes
```

### Frontmatter Template

```yaml
---
id: 08-final-deliverable
type: communication
step: 8
title: "Final Deliverable"
status: draft
addresses: "01-problem-definition.md#kq"
presents:
  - "07-recommendations.md#rec-core"
  - "06-synthesis.md#ans"
narrative_structure: answer-first  # answer-first | evidence-first | narrative-arc | transformation | comparative | sequential
visual_style: clean-minimal  # clean-minimal | data-heavy | visually-rich | corporate-branded
page_count: 0
---
```

## Narrative Structure Playbooks

### 1. Answer-First (Pyramid)
**Arc**: Conclusion → Supporting Arguments → Evidence
```
Title → [Exec summary] → [Context] → THE ANSWER (core rec) → Argument 1 + evidence → Argument 2 + evidence → Argument 3 + evidence → Implementation/next steps → [Appendix]
```

### 2. Evidence-First (Build)
**Arc**: Observations → Pattern → Conclusion
```
Title → [Exec summary] → [Context] → Observation 1 → Observation 2 → Observation 3 → The pattern/insight → Implication → Recommendation → Next steps → [Appendix]
```

### 3. Narrative Arc (SCR)
**Arc**: Situation → Complication → Resolution
```
Title → [Exec summary] → [Context] → Baseline context (2 slides) → Disruption + stakes (2 slides) → Key insight → Recommendation → Specific initiatives → Quantified benefit → Next steps → [Appendix]
```
Use context-specific headlines — never label sections "Situation," "Complication," "Resolution."

### 4. Transformation (Current → Future → Bridge)
**Arc**: As-Is → To-Be → How to Get There
```
Title → [Exec summary] → [Context] → Today's reality + what's broken → The vision + what good looks like → The path (initiatives) → Roadmap → [Appendix]
```
Never use "Current State," "Future State," "Bridge" as labels.

### 5. Comparative Evaluation
**Arc**: Alternatives → Evaluation → Selection
```
Title → [Exec summary] → [Context] → The alternatives (1 slide each) → Evaluation approach/criteria → Comparative results → Why winner wins → Risks → Implementation → [Appendix]
```

### 6. Sequential / Process
**Arc**: Phase 1 → Phase 2 → ... → Phase N
```
Title → [Exec summary] → [Context] → Overview (phases at a glance) → Phase 1 + detail → Phase 2 + detail → ... → Dependencies/risks → Timeline/resources → [Appendix]
```

### Building the Storyline

1. Select playbook matching Q1 choice
2. Fill headline chain using Steps 1-7 content — **the headline chain must form a coherent argument using only words, no numbers required**
3. Include/exclude sections per Q3, Q4, Q6
4. Fit to page count from Q5
5. **Narrative-first test**: Read just the headlines — they should tell the complete story as a logical argument. If any headline only works because of a number (e.g., "The market is $4.2B"), rewrite it to lead with the insight (e.g., "The target market is large enough to sustain our growth thesis")
6. **Number placement pass**: Only after the narrative is locked, decide where a specific number would strengthen a point. Most slides should work without any numbers. Add numbers sparingly as emphasis, not as the backbone.

## CRITICAL: Narrative-First, Not Data-First

**This is a thought leadership piece, not a quantitative research report.** Every slide must make sense without numbers. Numbers emphasize points — they never construct them.

- **Strip test**: Remove all numbers from a slide. If it becomes meaningless, the slide is structured wrong — rewrite around the insight.
- **Emphasis, not backbone**: Good: "Adoption is accelerating — enterprise deployments tripled last year." Bad: "Enterprise AI deployments reached 14,200 in 2024, up from 4,700 in 2023."
- **No data dumps**: If a slide has more than 2-3 numbers, question whether each one is pulling its weight. A slide full of internet-sourced statistics is a literature review, not analysis.

Data integrity rules (freshness, cross-checking, fewer-is-better) are enforced at Step 5 — see `05-analyze.md` Data Quality and Consistency. The Sceptical Review Subagent (Gate 2) will catch anything that slips through.

## Slide Design Principles

**Action Title Rule**: Every title is a complete sentence stating the key insight — lead with the argument, not the number.

| Bad | Good |
|-----|------|
| "Market Analysis" | "The target market is large and growing fast enough to sustain our thesis" |
| "$4.2B TAM at 23% CAGR" | "Market tailwinds create a compelling window for entry — the segment has grown 3x in four years" |
| "Cost Breakdown" | "Rising input costs are compressing margins and require a structural response" |

**Body**: One message per slide. Visual evidence over text. Max 5-6 one-line bullets.

**Source Footer**: Any slide/page with numbers gets a `Source: [citation(s)]` line at the bottom (~8pt, light gray for .pptx; 8-9pt gray for .docx). Multiple sources separated by semicolons. No superscript footnotes. Omit only on pages with no quantitative content.

**Framework-to-Deep-Dive Numbering**: When a framework slide has multiple blocks and subsequent slides detail each, use consistent numbering (Arabic, Roman, or letters) on both overview and detail slides.

**Chart Choice**: Trend → line, Comparison → bar, Part-of-whole → stacked bar/waterfall (avoid pie), Correlation → scatter, Process → diagram, Key number → large callout.

## Executive Summary Guidance (when selected)

Adapts to narrative structure but **never uses framework labels**:
- **Answer-First**: Recommendation → supporting reasons → impact
- **Evidence-First**: Key signals → conclusion they point to
- **SCR**: Context → disruption → path forward (no "Situation"/"Complication"/"Resolution" labels)
- **Transformation**: Today → target → path (no "Current State"/"Future State"/"Bridge")
- **Comparative**: Decision → options → winner → why
- **Sequential**: Phases → timeline → outcome

**Spine test**: Exec summary alone should convey the full argument. Slide titles alone should reconstruct the exec summary.

## Context & Objectives (when selected)

1. Why we're here (triggering event), 2. What was asked (question/scope), 3. How we approached it (1-2 sentences), 4. What success looks like (from Step 1).

## Visual Style Application

**Clean & Minimal**: 40%+ white space, one accent color, minimal gridlines, no decoration.
**Data-Heavy**: Dense charts/tables, multiple visualizations per slide, muted palette.
**Visually Rich**: Framework diagrams, process flows, icons, color-coded categories.
**Corporate/Branded**: Apply user's brand colors, fonts, logo, match existing materials.

**Brand styling profiles** (Q2): Read from `references/styles/`, apply typography, colors, layout, logo per the file. Visual style still governs density — brand file only controls visual identity.

## Word Document Guidance

Same narrative structures adapted for prose. Apply writing style guide throughout. Report structure: Title page → Exec Summary (if Q5) → Context (if Q6) → Content sections → Appendices (if Q8). Source footer goes at the end of each section that quotes numbers (same format as slides).

## Language Quality: Final Editing Pass

Before presenting, run all prose through editing per `references/writing-style.md`: cut filler, active voice, specific language, complete-sentence titles, read exec summary aloud. The goal is prose worthy of a top-tier consulting firm.

## REVIEW Phase: Four Gates

**Gate 0 — Visual Style Confirmation**: Before any building begins, confirm the visual style and brand choices back to the user. Summarize: chosen style, brand (if any), colors/fonts that will be used. Get explicit approval. Do not proceed to storyline or building without this.

**Gate 1 — Storyline**: Present headline sequence and structure before building. Get approval.

**Gate 2 — Sceptical Review**: After storyline is approved but **before building any slides or pages**, launch the Sceptical Review Subagent (defined in SKILL.md). Pass it the approved storyline, the synthesis document (Step 6), and the recommendations brief (Step 7). Present the subagent's full review to the user. Resolve all MUST FIX items before proceeding. SHOULD FIX items are the user's call. Do not skip this gate — it is mandatory for every final deliverable.

**Gate 3 — Final Deliverable**: Present the file. Check exec summary, flow, details, visual style, tone. Offer iteration. Multiple revision rounds are normal.

## Pitfalls

- **Topic titles instead of action titles**: "Q3 Revenue" tells nothing
- **Wrong structure for audience**: Evidence-First for a time-constrained CEO is wrong
- **Building the deck around numbers**: Numbers emphasize points, not construct them. If a slide is meaningless without its numbers, rewrite around the insight
- **Flabby prose**: Apply Strunk & White ruthlessly
- **Exposing framework scaffolding**: Never use literal framework labels as titles/headers
- **Skipping gates**: Visual style (Gate 0), storyline (Gate 1), and sceptical review (Gate 2) must all complete before building starts
