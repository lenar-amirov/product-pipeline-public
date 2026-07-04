---
name: multi-source-signal-synthesiser
description: Synthesises user signals from multiple research sources into a
  unified insight brief, reconciling conflicting feedback. Use when user has data
  from multiple sources, needs to "make sense of all this user data", "what are
  users really telling us", "synthesise our research", or has conflicting feedback
  from different channels.
metadata:
  author: Mohit Aggarwal
  version: 2.0.0
  category: discovery
  tags: [user-research, synthesis, discovery, insights, evidence-typing]
---
# Multi-Source Signal Synthesiser Skill

## Purpose
Reconcile user signals from multiple sources — interviews, support tickets, NPS,
app reviews, analytics, surveys, synthetic research — into a unified, weighted insight brief
that surfaces the underlying need rather than the surface-level request.

## Pipeline Context

**Primary use: Step 6 (/validate-problems)** — when combining:
- Analytics data (from analyst)
- Survey results (from research)
- Interview notes (from PM)
- Synthetic interviews (from step 2)

Also useful at any step where multiple data sources need reconciliation.

## Evidence Typing

Every signal must be tagged with evidence type and confidence score:

| Type | Confidence | Source examples |
|------|-----------|----------------|
| **REAL** | 0.6 - 1.0 | Analytics data, survey results, user interviews, A/B test results |
| **SYNTHETIC** | 0.2 - 0.4 | AI-generated interviews, synthetic personas |
| **INFERRED** | 0.3 - 0.5 | Logical deductions, cross-referencing patterns |
| **AMBIGUOUS** | 0.1 - 0.3 | Contradictory signals, unclear data |

**Conflict resolution**: When REAL contradicts SYNTHETIC, REAL wins. Document the delta — the gap between what synthetic research predicted and what real data showed is itself an insight.

## Source Weighting (default — adapt to your context)
- Direct research (interviews, usability tests): weight 5
- Analytics data (funnels, cohorts, events): weight 5
- Support tickets (unprompted pain signals): weight 4
- Survey results (structured quantitative): weight 4
- NPS verbatims: weight 3
- App store reviews: weight 2
- Sales call summaries (filtered through sales lens): weight 2
- Synthetic research (AI-generated): weight 1
- Anecdote or single report: weight 1

## Process
1. Accept inputs from any combination of source types
2. Tag each signal by source, apply weight, and assign evidence type + confidence
3. **CONVERGENCE**: same underlying need appearing across 3+ sources
   - Calculate combined confidence: highest individual confidence × (1 + 0.1 × number of confirming sources)
   - Cap at 1.0
4. **DIVERGENCE**: contradictory signals suggesting user segmentation
   - Don't average away disagreement — it usually means different user segments
5. **FREQUENCY RANKING**: count how many independent sources mention each insight
   - "N out of M sources mention this" (inspired by frequency-based evidence ranking)
6. Distinguish surface request from underlying need
   (e.g., "faster export" may mean "I don't trust the data will be there when I need it")
7. Produce ranked insights by weighted frequency

## Output Format

### User Signal Synthesis — [Date / Period]
**Sources included:** [list with evidence type for each]
**Total signals processed:** [n]
**Evidence quality**: [% REAL / % SYNTHETIC / % INFERRED]

#### Insight 1: [Underlying need, not feature request]
- **Frequency**: [N/M sources] — [list which sources]
- **Evidence type**: [REAL/SYNTHETIC/INFERRED] combined confidence: [0.0-1.0]
- **Evidence**:
  - Analytics: [specific data point] (REAL, 0.8)
  - Survey: [specific finding] (REAL, 0.85)
  - Interviews: [quote or pattern] (REAL, 0.9)
  - Synthetic: [what AI predicted] (SYNTHETIC, 0.3)
- **Conflicting signals:** [Any contradicting evidence and how to interpret it]
- **REAL vs SYNTHETIC delta**: [Where synthetic research got it wrong/right]
- **Product implication:** [Specific, not generic]

[Repeat for top 3-5 insights, ordered by combined confidence × frequency]

#### Divergent Signals (Possible Segmentation)
[Where user groups appear to have genuinely different needs]
- Segment A says X (evidence: ...) while Segment B says Y (evidence: ...)
- Implication: [consider separate solutions or prioritize one segment]

#### What the Data Does NOT Tell Us
[Gaps that require further research before acting]
- [Gap 1]: would need [research method] to resolve
- [Gap 2]: low confidence because only SYNTHETIC evidence exists

#### Confidence Summary
| Hypothesis | Evidence Sources | Combined Confidence | Recommendation |
|-----------|-----------------|--------------------:|---------------|
| P1: ... | Analytics + Survey + Interviews | 0.93 | Confirmed |
| P2: ... | Synthetic only | 0.35 | Needs validation |
| P3: ... | Analytics + contradicts Survey | 0.55 | Investigate segment split |

## Worked example (one insight)

> **Insight**: users abandon at payment because they distrust the embedded
> form, not because of price.
> **Converges**: survey Q7 (41% "не доверяю оплате", n=380, REAL) +
> 6 of 8 interviews (REAL) + session recordings show form hesitation
> (REAL). **Diverges**: NPS verbatims mention price (12 mentions) — likely
> a different segment (new vs returning); flag for segmentation.
> **Verdict**: H3 confirmed, REAL 0.8, three sources.

## Output to the registry (mandatory)

Every verdict this synthesis produces MUST land in the hypothesis registry —
`hypotheses.py set <id> --status confirmed|refuted|testing --type <T>
--confidence <C> --add-source "research/<file>::<where>"` per hypothesis.
Conflicting sources → `--flag data_inconsistency` instead of silently
averaging. A synthesis that only writes prose is invisible to gates and /next.
