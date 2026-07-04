---
paths:
  - "*/output/**"
---

# Output Artifact Formats

> Hypothesis STATE (status, evidence type, confidence, sources, history)
> lives in `output/hypotheses.json` and is managed via
> `tools/scripts/hypotheses.py`. The markdown formats below are NARRATIVE
> views — their Evidence/confidence lines must mirror the registry, never
> diverge from it.

## Problem hypotheses (`output/hypotheses.md`)

```
## Hypothesis P[N]: [Title]
**CJM step**: [01_step-name]
**Observation**: [fact]
**Problem hypothesis**: [why this is a problem]
**Who's affected**: [segment]
**Impact metric**: [which metric]
**Evidence**: [SYNTHETIC/REAL/INFERRED] confidence: [0.0-1.0]
**SIF Score**: Severity [1-10] x Impact [1-10] x Frequency [1-10] = [total]
**Priority**: High / Medium / Low
```

## Solution hypotheses (`output/solution-hypotheses.md`)

```
## Hypothesis S[N]: [Title]
**Solves problem**: P[N]
**What**: [what we change]
**Mechanism**: [how it works for user]
**Formula**: If [X], then [Y], because [Z], so [M] grows by [N%].
**Metric** / **Counter-metrics** / **Proxy**:
**Win criteria**:
**N% forecast**: [justification]
**Risks** / **Complexity**: High/Medium/Low
**ICE Score**: Impact x Confidence x Ease = [total]
**Business viability**:
  - Unit economics: [estimate]
  - Cannibalization: [risk]
  - Dependencies: [teams/systems]
  - Compliance: [risks]
  - Effort: S/M/L
```

## Tickets (`output/tickets.md`)

```
## EPIC: [Title]
tracker_ref: [URL or ID after push]

### Story: [Title]
As [role] I want [action] So that [value]
**Acceptance criteria**: Given/When/Then
**Priority**: Must Have / Should Have
**Estimate**: [from dev-estimate]
**Component**: [Backend / Frontend / Design / QA]
**Depends on**: [other story titles]
**Sub-tasks**:
- [ ] Design
- [ ] Backend
- [ ] Frontend
- [ ] QA
```

## Decisions log (`output/decisions.md`)

```
## YYYY-MM-DD — Step N: Title / Discussion: topic

**What we did**: ...
**Key decisions**: ...
**Open questions**: ...
**Next step**: ...
```

## PRD sections mapping

PRD is filled incrementally:
- Steps 1 → §1 Context, §2 Target user
- Step 3 → §5 Competitors
- Step 6 → §3 Success metric, §4 Validated problems
- Steps 7-8 → §6 Solution, §7 Scope
- Step 12 → §9 NFR, §10 Dependencies
- Step 13 → §8 User Stories, §11 Open questions

## Anti-generic self-check (every generated artifact)

Before delivering ANY artifact (presentation, PRD, brief, GTM material),
verify against this checklist and fix violations — do not show the draft:

1. **No claim without a source.** Every number and factual statement carries
   `[source: file/slide/page]` or maps to a registry hypothesis id. A claim
   you cannot source is an opinion — label it as such or cut it.
2. **No placeholder advice.** Lines like "ensure compliance", "improve UX",
   "conduct user research", "align with stakeholders" without a concrete
   what/where/how are filler — cut or make specific to THIS initiative.
3. **Proof surfaces are REAL-only.** In presentations, "proof" slides may
   cite only REAL evidence; SYNTHETIC/INFERRED goes to speaker notes as
   context (see evidence-typing.md). In PRDs, §4 Validated problems cites
   only confirmed registry entries.
4. **Frequency honesty.** "Users say X" requires "N of M sources" — one
   synthetic persona is not "users".
5. **Numbers cross-check.** If two numbers in the artifact disagree with
   each other or with the registry — stop and reconcile before delivering.
6. **Prose passes writing-style.md.** Needless words cut, active voice,
   claims lead paragraphs — see `.claude/rules/writing-style.md`.
