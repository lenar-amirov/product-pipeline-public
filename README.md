# Product Discovery

**Run a product initiative as a tracked journey — from one-sentence problem to PRD, with persistent state across sessions.**

Not a toolbox of one-shot AI answers. A structured pipeline where every session adds to the same initiative — drill-down questions, evidence-typed hypotheses, a PRD that builds incrementally, and a decision log you can come back to next week.

Built on [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Powered by Double Diamond, Teresa Torres' Continuous Discovery, and Marty Cagan's Product Discovery.

> **Requires** Claude Code desktop app or CLI (not the web version — needs persistent local state).

---

## Why this, and not a PM skill toolbox?

There are great PM skill collections — [pm-skills](https://github.com/phuryn/pm-skills) (60+ skills), [Anthropic's official PM plugin](https://github.com/anthropics/knowledge-work-plugins) (`/write-spec`, `/synthesize-research`, `/competitive-brief`) — that you call ad-hoc. They're excellent for one-shot answers, and stateless by design.

**Product Discovery is different.** It's not a toolbox — it's a journey:

| | PM toolbox (pm-skills, Anthropic PM plugin) | Product Discovery (this) |
|---|---|---|
| **Unit of work** | One question, one answer | One initiative, many sessions |
| **State** | Stateless — Claude forgets next time | Persistent: CONTEXT.md, status.json, decisions.md, PRD.md |
| **PRD** | Generated when you ask | Living document, builds across all 19 steps |
| **Evidence** | Free-form text | Typed (REAL / SYNTHETIC / INFERRED, confidence 0.0–1.0) in a machine-readable registry, validated every session |
| **Continuity** | Each session is a fresh start | Resume exactly where you stopped, with full context |
| **Best for** | Quick answers on any PM task | Working a real product initiative through to launch |

**Use a PM toolbox** when you want quick help with one specific task.
**Use Product Discovery** when you've committed to a real initiative and want a tracked path from problem to launch.

(They complement each other — you can install both.)

---

## Get started in 30 seconds

### 1. Get the tool

```bash
git clone https://github.com/lenar-amirov/product-pipeline-public.git pm-copilot
cd pm-copilot && claude
```

That's it. No questions, no restart, no required dependencies — bare
`python3` is enough (`pip3 install rich` is optional, for a prettier
dashboard).

**No git?** [Download ZIP](https://github.com/lenar-amirov/product-pipeline-public/archive/refs/heads/main.zip), unpack, open the folder in [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

**Where your work lives**: initiatives are created by the tool itself
inside this folder (`{your-name}/{initiative}/`) — gitignored by design,
so they never enter the public repo and never conflict with updates.

**Updates**: `git pull`. Your initiatives are untouched; if you've
customized `CLAUDE.md`, stash your changes first or work in a fork.

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

  Or start with a job right away:
    "read this deck"  ·  "I need an analyst brief"  ·  "break down problem X"
```

Type one sentence. For example:

> Users add items to cart but never complete checkout on mobile

### 3. Value first — the initiative is created after

Claude runs the matching job immediately: for a problem statement you get
3–5 problem hypotheses (typed `INFERRED` until validated) with ONE sharp
challenge question woven in; for "here's a deck from the analyst" it
ingests the deck; for "I need an analyst brief" it writes the brief.

Only then it offers: *"Save this as initiative `<slug>`?"* — say yes and
the folder appears with a hypothesis registry, status and a decision log.
Close Claude, come back next week — the session resumes exactly where you
stopped, with the dashboard showing coverage, overdue dependencies and
evidence issues.

---

## The pipeline

19 steps across 3 phases. Each step produces a concrete artifact and updates the living PRD.

```
   Problem Research              Solution Design + Validate         Launch
┌─────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────┐
│ CJM Analysis            │  │ Design Brief                 │  │ GTM Plan     │
│ Synthetic Research      │  │ Dev Estimate                 │  │ GTM Materials│
│ Competitor Research     │  │ Finalize PRD                 │  │ Support Brief│
│ Research Briefs         │  │ AB Test Design               │  └──────────────┘
│ Validate Problems       │  │ Solution Research Report ▶   │
│ Solution Hypotheses     │  │ AB Test Analysis             │
│ Sketch Solution         │  │  → Ship / Extend / Iterate   │
│ Design Review           │  └──────────────────────────────┘
│                         │
│   Problem Research      │
│       Report ▶          │
└─────────────────────────┘
```

### What you accumulate over the journey

| Artifact | What it is |
|----------|-----------|
| **CONTEXT.md** | The initiative's frame: metric, segment, baseline, constraints, OKR — never re-explained |
| **status.json** | Current step, pending tasks, pipeline config — Claude resumes from here |
| **decisions.md** | Log of every meaningful decision and discussion across sessions |
| **hypotheses.json** | Machine-readable hypothesis registry: status, evidence type, confidence, sources, full history of every transition. Validated on each session start; `registry.md` is the generated view |
| **hypotheses.md** | Narrative hypothesis analysis (the registry holds the state) |
| **.initiatives-digest.md** | Auto-generated cross-initiative summary — Claude spots overlaps between your new problem and past initiatives |
| **PRD.md** | Living document — sections fill as you progress, not at the end |
| **Problem Research Report** | Presentation: validated problem + solution sketch (after step 10) |
| **Solution Research Report** | Presentation: designed solution + AB test plan (after step 15) |
| **tickets.md** | Dev tickets — pushed to Jira/Linear/GitHub via MCP if connected |

---

## What's bundled

| Component | Role |
|-----------|------|
| `CLAUDE.md` | Master prompt — session lifecycle, FIRST LAUNCH flow, intent matching |
| `.claude/settings.json` | `SessionStart` hooks: dashboard, initiatives digest, evidence audit |
| `.claude/skills/` | 23 specialized skills — problem structuring, ingestion, validation, scoring, gates rehearsal, PRD, post-launch review, etc. |
| `.claude/rules/` | Path-scoped rules: output formats, evidence typing |
| `template/` | Initiative scaffold copied for each new initiative |
| `tools/scripts/status.py` | Branded terminal dashboard with first-launch onboarding |
| `tools/scripts/scan-initiatives.py` | Regenerates `.initiatives-digest.md` — cross-initiative awareness at every session start |
| `tools/scripts/hypotheses.py` | Hypothesis registry engine: add / set / validate / render (state + full history) |
| `tools/scripts/validate-evidence.py` | Session-start evidence audit: confidence ranges, missing sources, unreconciled data |
| `tools/scripts/new-initiative.sh` | Initiative scaffolder |
| `tools/scripts/generate-pptx.py` | Markdown → PowerPoint conversion |
| `tools/web/` | Optional local web dashboard (Flask) + `static_export.py` — dependency-free single-file HTML export of an initiative |

### Your initiative folder

```
you/my-initiative/
├── CONTEXT.md              ← metric, segment, baseline, constraints
├── CJM/                    ← user journey screenshots
├── research/               ← analytics briefs, survey design, competitive analysis
└── output/                 ← hypotheses, PRD, presentations, decision log
```

### Configurable pipeline

Pick a template or compose your own. Mandatory steps stay locked.

| Template | Steps | Best for |
|----------|-------|----------|
| **Quick Discovery** | ~6 core steps | PM with existing data, tight timeline |
| **Full Discovery** | All steps | New problem space, full research |
| **Problem Only** | 5 steps | Just understand the problem |
| **Solution Only** | 7 steps | Problem known, design solution |
| **Custom** | Your choice | You know what's needed |

---

## Tracker integration

After Solution Research Report, push tickets to your tracker via MCP. Set the tracker in `CONTEXT.md` → `## Tracker` section.

### Jira + Confluence

MCP config lives in `.mcp.json` at the repo root — **gitignored**, because it holds your real API token. Never put credentials in `.claude/settings.json` (tracked by git).

1. Copy `.mcp.json.example` → `.mcp.json`
2. Fill in your Jira/Confluence URL and API token
   (Atlassian Cloud: https://id.atlassian.com/manage-profile/security/api-tokens)
3. If your company runs a different Jira/Confluence MCP server package, put its `command`/`args` in — the example uses a placeholder package name
4. Restart Claude Code and approve the servers when prompted

### Linear

Add a `linear` entry to the same `.mcp.json` with the MCP server your team uses (API key: Linear → Settings → API → Personal API keys).

### GitHub Issues

No extra MCP — Claude Code uses `gh` CLI natively. Run `gh auth status` to verify you're logged in.

### No tracker

Skip MCP. `/create-tickets` writes `output/tickets.md` for manual copy-paste.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — CLI, desktop app, or IDE extension (not web)
- Python 3.9+ (macOS system Python works; no packages required for the core)
- `pip3 install rich` — optional, prettier terminal dashboard (plain-text fallback works without it)

Optional, install on demand:
- `pip3 install python-pptx` — when you reach `/create-presentation` (step 10) or `/create-gate2-presentation` (step 15)
- `pip3 install flask markdown` — only if you want the optional Flask web dashboard at `tools/web/app.py`

---

## Optional: Flask web dashboard

`tools/web/app.py` provides a visual dashboard:

```bash
pip3 install flask markdown
PM_USERS=$(cat .pm-local) python3 tools/web/app.py
# open http://127.0.0.1:5000/{your-name}/
```

It binds to `127.0.0.1` and is a **local viewer** — it has no real authentication. Set `PIPELINE_HOST=0.0.0.0` only on a network you trust.

No Flask? `python3 tools/web/static_export.py <you>/<initiative>` emits a self-contained HTML dashboard for one initiative (no dependencies).

Most users don't need either — `tools/scripts/status.py` (auto-run at session start) shows the same info in the terminal.

---

## FAQ

**How do I continue working?**
Open Claude Code in the project directory. The SessionStart hook runs `status.py` which loads your last state. Type "continue" and Claude picks up where you stopped.

**How do I change the pipeline configuration?**
Tell Claude: "reconfigure pipeline" or "switch to quick template" or "enable competitor research". The config lives in `output/status.json` → `pipeline_config`.

**Can I work on multiple initiatives in parallel?**
Yes. Each initiative is a separate folder with its own `CONTEXT.md`, `status.json`, `decisions.md`. Claude shows all initiatives at session start; you select one.

**What are Problem Research Report and Solution Research Report?**
Two presentations for stakeholders:
- **Problem Research Report** (after step 10) — validated problem + solution sketch
- **Solution Research Report** (after step 15) — designed solution + AB test plan

**What's the difference between step types?**
- **Core** — pipeline breaks without it
- **Recommended** — strongly suggested; skipping reduces confidence
- **Optional** — useful in specific contexts only

**Where are my personal preferences stored?**
- `pm-profile.md` — your role, company, working style (gitignored, personal)
- `.product-corrections.md` — accumulated corrections you've taught Claude (gitignored)
- `.initiatives-digest.md` — auto-generated overview of all your initiatives

---

## Get in touch

Product Discovery ships continuously — see [CHANGELOG](./CHANGELOG.md) for what's new and [docs/](./docs/) for the design decisions behind the tool. Real PM feedback shapes the next iterations.

- 🐛 **Bug?** → [open an issue](https://github.com/lenar-amirov/product-pipeline-public/issues/new?template=bug.yml)
- 💬 **Tried it? Share how it went** → [feedback issue](https://github.com/lenar-amirov/product-pipeline-public/issues/new?template=feedback.yml)
- 💭 **Questions, ideas, just want to chat** → [Discussions](https://github.com/lenar-amirov/product-pipeline-public/discussions)
- 🎉 **Show off your initiative** → [Discussions / Show & Tell](https://github.com/lenar-amirov/product-pipeline-public/discussions/categories/show-and-tell)

---

## Privacy

Product Discovery is local-first — there is no server, no telemetry, no analytics. Everything lives on your machine. Claude Code processes your conversation through Anthropic; integrations you connect (Jira / Linear MCP) see the ticket data you push.

Extra guard for contributors: `tools/scripts/install-hooks.sh` installs a
pre-push hook that blocks pushes containing initiative folders, credential
files, token-like values, or your personal markers from a gitignored
`.leak-patterns` file.

See [PRIVACY.md](./PRIVACY.md) for full details.

---

## License

MIT
