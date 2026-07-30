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
| **Unit of work** | One question, one answer | Point-entry jobs that accumulate into one tracked initiative |
| **State** | Stateless — Claude forgets next time | Persistent: hypothesis registry, decision log, living PRD, coverage map |
| **PRD** | Generated when you ask | Living document, sections fill as evidence arrives |
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

## How it works — jobs, not steps

You don't march through a checklist. You come with a moment — "read this
deck", "which hypotheses hold?", "tomorrow's the gate" — and call the
matching **job**. Each job works standalone and quietly records what it
learned into the initiative's state.

| Job | When you reach for it |
|---|---|
| `/hypotheses` | break a problem into testable hypotheses (MECE) |
| `/ingest` | you were handed a deck / export / wiki page — pull the numbers in |
| `/brief` | you need a brief for an analyst or designer |
| `/validate` | data arrived — confirm, refute or flag hypotheses against it |
| `/solutions` | turn confirmed problems into scored solution bets |
| `/sketch` | draw the screens for a solution |
| `/challenge` | rehearse a gate — three hostile stakeholders attack your deck |
| `/tickets` | break the solution into Jira/Linear/GitHub tickets |
| `/next` | "what's the most valuable thing to do now?" |
| `/deep-think` | a strategy question that isn't an initiative yet |

Legacy step commands (`/analyze-cjm`, `/validate-problems`, …) still work as
aliases — the numbered pipeline (steps 0–19) is the internal structure the
jobs draw on, not something you navigate by hand.

### Progress is evidence coverage, not "step N of 20"

The dashboard shows a **coverage map** of seven phases, computed from your
actual state — the registry, the artifacts, the gate checks — not from how
many commands you've run:

```
Frame 2/4 · Evidence 3/3 · Solution 0/2 · Bet 0/1 · Build 0/2 · Launch 0/3 · Learn 0/1
focus → Solution: no solutions linked to confirmed hypotheses yet
```

Gates (Problem Research Report, Solution Research Report) have **machine
preconditions**: you can't assemble the deck until ≥2 hypotheses are
confirmed REAL, the registry has no unreconciled contradictions, and the
frame (metric / target / kill criteria) is set. After launch, the **Learn**
phase closes the loop — actual vs target, production verdicts on each
hypothesis, and reusable facts banked for your next initiative.

### What you accumulate over the journey

| Artifact | What it is |
|----------|-----------|
| **CONTEXT.md** | The initiative's frame: metric, segment, baseline, constraints, OKR — never re-explained |
| **hypotheses.json** | Machine-readable hypothesis registry: status, evidence type, confidence, sources, full history of every transition. Validated on each session start; `registry.md` and `ost.md` (Opportunity Solution Tree) are generated views |
| **status.json** | Machine state: step statuses, `dependencies[]` (external work with owner + deadline, flagged OVERDUE on the dashboard), pipeline config — Claude resumes from here |
| **decisions.md** | Log of every meaningful decision and discussion across sessions |
| **hypotheses.md** | Narrative hypothesis analysis (the registry holds the machine state) |
| **.initiatives-digest.md** | Auto-generated cross-initiative summary + banked knowledge facts — Claude spots overlaps with past initiatives |
| **PRD.md** | Living document — sections fill as evidence arrives, not at the end |
| **Problem Research Report** | Gate deck: validated problem + solution sketch (gate-checked before assembly) |
| **Solution Research Report** | Gate deck: designed solution + AB test plan (gate-checked before assembly) |
| **tickets.md** | Dev tickets — pushed to Jira/Linear/GitHub via MCP if connected |

---

## What's bundled

| Component | Role |
|-----------|------|
| `CLAUDE.md` | Master prompt — session lifecycle, FIRST LAUNCH value-first flow, JOBS CATALOG |
| `.claude/settings.json` | `SessionStart` hooks: dashboard, initiatives digest, evidence audit |
| `.claude/skills/` | 23 specialized skills — problem structuring, ingestion, validation, scoring, gate rehearsal, PRD, post-launch review, etc. |
| `.claude/rules/` | Path-scoped rules: output formats, evidence typing, writing style |
| `template/` | Initiative scaffold copied for each new initiative |
| `tools/scripts/status.py` | Terminal dashboard: coverage map, OVERDUE dependencies, `/next` hint |
| `tools/scripts/hypotheses.py` | Hypothesis registry engine: add / set / validate / render (state + full history) |
| `tools/scripts/validate-evidence.py` | Evidence audit + `--gate` preconditions that block deck assembly |
| `tools/scripts/coverage.py` | The coverage map: 7 phases with exit criteria computed from actual state |
| `tools/scripts/scan-initiatives.py` | Regenerates `.initiatives-digest.md` — cross-initiative awareness at every session start |
| `tools/scripts/render-ost.py` · `render-pdf.py` · `generate-pptx.py` | Opportunity Solution Tree, PDF→PNG for `/ingest`, gate decks → .pptx |
| `tools/scripts/check-leaks.py` + `install-hooks.sh` | Pre-push guard against committing personal data (see Privacy) |
| `tools/web/` | Optional read-only web dashboard (Flask) + `static_export.py` — dependency-free single-file HTML export |

(Full inventory with the "why" of every file: [docs/REPO-MAP.md](./docs/REPO-MAP.md).)

### Your initiative folder

```
you/my-initiative/
├── CONTEXT.md              ← metric, segment, baseline, constraints
├── CJM/                    ← user journey screenshots
├── research/               ← analytics briefs, survey design, competitive analysis
└── output/                 ← hypotheses, PRD, presentations, decision log
```

### No templates to choose — you run the jobs you need

There's no "pick a workflow" step. A new initiative starts with everything
available; you call the jobs your situation calls for, and the coverage map
shows what evidence is still missing. Got rich data already? Go straight to
`/ingest` and `/validate`. Fuzzy problem? Start with `/hypotheses`. Only a
strategy question? `/deep-think`. Each step carries a Core / Recommended /
Optional weight so `/next` knows what's safe to skip — but the choice of
what to do is always the job in front of you, never a template up front.

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

**Do I have to run every step?**
No. Run the jobs your situation needs; the coverage map shows what evidence is still missing, and `/next` recommends the most valuable action from your actual state. If you want to switch a specific step off, tell Claude "disable competitor research" — the per-step config lives in `output/status.json` → `pipeline_config`. (There are no workflow templates to pick — that model was retired.)

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
