---
name: ab-test-announcement-wizard
description: Generates internal announcements for AB tests and releases.
  Use when user needs to announce an AB test launch, release rollout,
  or says "announce the test", "write AB test announcement", "announce release",
  "write release post for the team channel".
metadata:
  version: 1.0.0
  category: communication
  tags: [ab-test, release, announcement, communication]
---
# AB Test & Release Announcement Wizard

## Purpose
Generate clear, structured internal announcements for AB test launches and
full releases. These posts go to a team/company channel so everyone knows
what's changing, why, and how to report issues.

## When to Use
- **Step 18** (`/create-gtm-materials`): structural patterns for in-app
  notifications, email announcements, blog posts, and other GTM materials
  generated when the validated solution is rolled out to existing users.
- Anywhere else the PM asks to draft an internal announcement (AB test
  launch, full rollout, milestone communication).

## AB Test Announcement Template (Step 17)

### Required Inputs
- `output/PRD.md` — what the feature does
- `output/ab-test-design.md` — experiment parameters

### Structure (8 sections)

```markdown
# [Greeting emoji] AB Test Launch: [Feature Name]

## 1. What's Happening
[One sentence: what we're testing and why]

## 2. What Changes for Users
- **Test group** ([N%] of [segment]): [What they see differently]
- **Control group**: [No changes]
- [Screenshot or link to mockup if available]

## 3. Hypothesis
> If [change], then [metric] will [improve/increase by N%],
> because [reasoning].

## 4. Context
- Problem: [1-2 sentences from validated hypotheses]
- Evidence: [Key data points that led to this solution]
- What we tried before: [If applicable]

## 5. What We Expect
- **Primary metric**: [metric name] from [baseline] to [target]
- **Guardrail metrics**: [metrics that must NOT degrade]
- **Duration**: [N weeks]

## 6. Rollout Details
- **Platforms**: [web / iOS / Android]
- **Segments**: [who's in the test]
- **Start date**: [date]
- **Expected end date**: [date]

## 7. Experiment IDs
- [Platform]: `experiment_id_here`
- [Platform]: `experiment_id_here`

## 8. Contact
- **PM**: [name] — for questions about the feature
- **Analyst**: [name] — for questions about the experiment
- **Report bugs**: [channel or link]
```

### Tone
- Informative, not promotional
- Assume the reader has 30 seconds
- Lead with what changed, not why it's brilliant
- Include experiment IDs so anyone can look it up

## Release Announcement Template (Step 18)

Adapt the AB test template for full rollout:

### Key Differences from AB Test Announcement

| Section | AB Test | Release |
|---------|---------|---------|
| **1. What's Happening** | "We're testing..." | "We're rolling out to 100%..." |
| **3. Hypothesis** | Future tense hypothesis | **Results**: what the AB test showed |
| **5. Expectations** | What we hope to see | **Measured impact**: actual numbers from AB |
| **6. Rollout** | Test group % | Full rollout plan (phased or immediate) |
| **7. IDs** | Experiment IDs | Feature flag / release version |

### Additional Section: What's Next
```markdown
## What's Next
- [Iteration 1]: [planned improvement based on AB learnings]
- [Iteration 2]: [future plan]
- [Monitoring]: We'll watch [metrics] for [N weeks] post-rollout
```

### When AB Test Results Are Not Available
If releasing without AB test (e.g., step 14 was disabled):
- Replace "Results" with "Expected impact" based on research data
- Note: "Releasing based on [research type] validation, no AB test conducted"
- Add monitoring plan: what metrics to watch post-release

## Placeholders

If data is missing, use `[placeholder]` and add a "Needs clarification" section at the end:
```markdown
## Needs Clarification
- [ ] Experiment IDs not yet assigned
- [ ] Exact rollout date TBD
- [ ] Analyst contact not specified
```

## Output

When invoked from step 18 `/create-gtm-materials`, contributes the announcement-style sections to `output/materials/email-announcement.md`, `output/materials/blog-post.md`, etc. (drives the structure / tone, not the file path).

When invoked ad-hoc, write to whatever file the PM asks for. PM reviews, then publishes.
