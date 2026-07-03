---
name: system-design-doc
description: Captures the system context a PM needs for feasibility — affected components, dependencies on teams/systems, constraining NFRs, integration risks — feeding PRD §9-10 and the dev estimate. Use with the dev lead at estimation time, or when the user says "system design", "architecture constraints", "what does this touch", "технические зависимости", "системный дизайн". NOT a full engineering design doc.
---

# System Design (PM view)

Boundary: **this skill = what the system looks like and what constrains the
initiative** (feasibility input, PRD §9–10). What will be built for this
initiative belongs to `technical-spec-document`.

This is a conversation WITH the dev lead, not a document Claude invents.
Claude structures; the dev lead supplies facts. Anything Claude infers
without the dev lead is INFERRED — mark it and list it as an open question.

## What to capture (in priority order)

1. **System context** — which existing components/services does the
   solution touch? One list: component → what changes.
2. **Dependencies** — teams, internal platforms, external vendors the
   initiative needs. For each: owner + what exactly + lead time. These
   become `dependencies[]` in status.json (owner, deadline, blocks) —
   offer to create them immediately.
3. **Constraining NFRs** — load, latency, privacy/compliance, platform
   parity. Only the ones that could change the solution shape or the
   estimate; skip textbook lists.
4. **Risks and unknowns** — the "we won't know until we open it" list;
   each unknown widens the estimate — ask the dev lead to size the
   widening.
5. **Integration points for tracking** — where the analytics events (from
   `tracking-and-funnels`) will be emitted; flag anything the solution
   makes unmeasurable.

## Output

`output/dev-estimate.md` §Architecture (or PRD §9–10 directly): context
list, dependency table, constraining NFRs, risk register with estimate
impact.

## Anti-patterns

- Infrastructure detail (servers, databases, configs) the PM neither needs
  nor can verify.
- Presenting Claude-guessed architecture as fact — without the dev lead
  everything here is INFERRED.
- NFR laundry lists — only constraints that change decisions.
