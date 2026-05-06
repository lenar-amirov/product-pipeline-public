# Product Discovery

Your AI copilot for product discovery. From a product problem to a validated solution — research, hypotheses, presentations, PRD — all structured and evidence-based.

Product Discovery removes the drudgery — writing briefs, structuring hypotheses, building presentations — so you focus on strategy, design, and talking to users.

Built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Powered by Double Diamond, Teresa Torres' Continuous Discovery, and Marty Cagan's Product Discovery.

---

## Get started in 30 seconds

### 1. Install the plugin

In Claude Code:

```
/plugin marketplace add lenar-amirov/product-pipeline-public
/plugin install product-discovery
```

Then in any project where you want to start a discovery:

```
/product-discovery:init
```

The plugin scaffolds `CLAUDE.md`, `template/`, and `.claude/` into your repo. After scaffolding:

```bash
pip install rich        # for the status dashboard
```

Restart Claude Code so the new `CLAUDE.md` loads.

### Alternative: clone the repo

If you don't want the plugin, clone directly:

```bash
git clone https://github.com/lenar-amirov/product-pipeline-public.git my-discovery
cd my-discovery && pip install rich
```

Open in [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

### 2. Describe your problem

You'll see:

```
╭────────────────────────────────────────╮
│                                        │
│  ◆ Product Discovery                   │
│  PM Copilot                            │
│                                        │
╰────────────────────────────────────────╯

  What product problem are you working on?
```

Type one sentence. For example:

> Users add items to cart but never complete checkout on mobile

### 3. Get instant results

Product Discovery immediately creates:

- **Initiative folder** with all the scaffolding
- **3-5 problem hypotheses** tied to your product
- **Research plan** — what data to collect, who to interview
- **Next steps** — add CJM screenshots for deeper analysis or continue the pipeline

That's it. You're in the pipeline. Say `continue` and Product Discovery guides you through every step.

---

## What happens next

The pipeline walks you through structured discovery — step by step:

```
   Problem Research                    Solution Design              Launch
┌─────────────────────────┐  ┌──────────────────────────┐  ┌──────────────┐
│ CJM Analysis            │  │ Design Brief             │  │ Support Brief│
│ Synthetic Research      │  │ Dev Estimate             │  │ AB Test Post │
│ Competitor Research     │  │ Finalize PRD             │  │ Release Post │
│ Research Briefs         │  │ AB Test Design           │  └──────────────┘
│ Validate Problems       │  │                          │
│ Solution Hypotheses     │  │   Solution Research      │
│ Sketch Solution         │  │       Report ▶           │
│ Design Review           │  └──────────────────────────┘
│                         │
│   Problem Research      │
│       Report ▶          │
└─────────────────────────┘
```

Every step produces a concrete artifact — hypotheses, briefs, presentations, PRD — and tracks decisions along the way.

### What you get at the end

| Artifact | Description |
|----------|-------------|
| **Problem Research Report** | Presentation: validated problem + solution sketch |
| **Solution Research Report** | Presentation: designed solution + AB test plan |
| **PRD** | Living document built incrementally across all steps |
| **Research artifacts** | Hypotheses, competitive analysis, survey design, interview synthesis |
| **AB test design** | Baseline, MDE, sample size, guardrails, decision criteria |

---

## How it works

Product Discovery is a set of prompts and skills that run inside Claude Code. No server, no SaaS — everything stays in your local repo.

| Component | What it does |
|-----------|-------------|
| `CLAUDE.md` | Master prompt — pipeline logic, session lifecycle, formats |
| `template/` | Initiative scaffold — copied for each new initiative |
| `.claude/skills/` | 19 specialized skills (discovery, personas, funnels, PRD, design critique, pipeline-steps, etc.) |
| `tools/scripts/status.py` | Terminal dashboard — shows progress at session start |
| `tools/scripts/generate-pptx.py` | Converts presentation markdown to .pptx |

### Your initiative folder

```
you/my-initiative/
├── CONTEXT.md              ← metric, segment, baseline, constraints
├── CJM/                    ← user journey screenshots
├── research/               ← analytics briefs, survey design, competitive analysis
└── output/                 ← hypotheses, PRD, presentations, decision log
```

### Pipeline is configurable

Choose a template or pick individual steps:

| Template | Steps | Best for |
|----------|-------|----------|
| **Quick Discovery** | ~6 core steps | Have data, need structure |
| **Full Discovery** | All steps | New problem, full research |
| **Problem Only** | 5 steps | Just understand the problem |
| **Solution Only** | 7 steps | Problem known, design solution |
| **Custom** | Your choice | You know what's needed |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — CLI, desktop app, or IDE extension
- Python 3.10+
- `pip install rich` — for the terminal dashboard

Optional (for presentations and web dashboard):
```bash
pip install -r requirements.txt   # rich, flask, markdown, python-pptx
```

---

## License

MIT
