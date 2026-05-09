---
description: Scaffold the Product Discovery pipeline into the user's current project directory. Run when the user invokes /product-discovery:init or asks to "scaffold pipeline", "set up product discovery", "initialize discovery". Copies CLAUDE.md, template/, .claude/skills/, .claude/rules/, and tools/scripts/ from the plugin into the user's working directory, so Claude can run the discovery pipeline on every future session.
---

# Product Discovery — Init

Scaffold the full Product Discovery pipeline into the user's current project directory.

## What this skill does

Copies the plugin's bundled pipeline files into the user's working directory:

```
<user-repo>/
├── CLAUDE.md                       # Master prompt — pipeline lifecycle
├── .claude/
│   ├── skills/                     # 19 specialized skills
│   └── rules/                      # Output formats, evidence typing
├── template/                       # Initiative scaffold
└── tools/scripts/
    ├── status.py                   # Branded session-start dashboard
    ├── new-initiative.sh           # Initiative scaffolder
    └── generate-pptx.py            # Presentation builder
```

Once scaffolded, the user works with the pipeline as a normal local project — Claude reads CLAUDE.md at every session start, runs status.py, and walks them through the discovery flow.

## How to run

Follow these steps in order. **Don't skip the confirmation step** — the user needs to know exactly what's being copied where.

### Step 1: Confirm location

Run:
```bash
pwd
```

Show the absolute path to the user and ask:
> "Scaffold Product Discovery into `<absolute-path>`? (y/n)"

- If user says no, ask: "Which directory should I scaffold into?"
- If user is in `~` (home directory), warn: "This will copy files directly into your home directory. Usually you want a project subdirectory. Continue anyway?"

### Step 2: Check for existing files

Run:
```bash
ls -d CLAUDE.md .claude template tools 2>/dev/null
```

If any of those exist, list them and ask:
> "These files already exist: [list]. Choose: (m) merge — keep existing, only add new / (o) overwrite all / (c) cancel?"

Default to merge. Skip step 3 if user picks cancel.

**Special case for `.claude/settings.json`**: if the user already has `.claude/settings.json`, our SessionStart hook won't be added in merge mode. Tell them: "Your existing `.claude/settings.json` was kept. To get auto-launching of the welcome screen at session start, manually add this hook to your settings.json:"

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "python3 tools/scripts/status.py" } ] }
    ]
  }
}
```

### Step 3: Copy files

The plugin's bundled files live at `${CLAUDE_PLUGIN_ROOT}` — this environment variable is set by Claude Code when the plugin is loaded.

Run this single bash block:

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT not set — plugin install may be broken}"
TARGET="$(pwd)"

# Use -n (no-clobber) for merge, -f for overwrite. Default: merge.
COPY_FLAG="${COPY_FLAG:--n}"

cp -r $COPY_FLAG "$PLUGIN_ROOT/CLAUDE.md" "$TARGET/" 2>/dev/null || cp -r "$PLUGIN_ROOT/CLAUDE.md" "$TARGET/"
cp -r $COPY_FLAG "$PLUGIN_ROOT/.claude" "$TARGET/" 2>/dev/null || true
cp -r $COPY_FLAG "$PLUGIN_ROOT/template" "$TARGET/" 2>/dev/null || true
cp -r $COPY_FLAG "$PLUGIN_ROOT/tools" "$TARGET/" 2>/dev/null || true

# Verify the copy succeeded
ls "$TARGET/CLAUDE.md" "$TARGET/template" "$TARGET/.claude/skills" "$TARGET/tools/scripts" >/dev/null && echo "OK" || echo "MISSING"
```

For overwrite mode, set `COPY_FLAG=-f` before running.

### Step 3.5: Create personal context files (if missing)

These files are personal to the PM and should NOT be overwritten if they already exist. Use the Write tool with `if not exists` semantics — check first via `ls`, only create when absent.

**`.product-corrections.md`** — accumulated rules from PM corrections. Claude reads at every session start.

If `.product-corrections.md` doesn't exist in the target directory, create it with this template:

```markdown
# Product Corrections — [PM Name]

> Personal log of corrections you've given Claude. Claude reads this at every
> session start and applies these rules. Append new entries — don't delete
> (history matters).
>
> Add corrections by:
>   1. Editing this file directly
>   2. Telling Claude: "Add to corrections: ..."
>   3. When you push back during a session, Claude will offer to add it here

## Metrics
<!-- e.g. We measure conversion to purchase, NOT add-to-cart (added 2026-04-15) -->

## Segments
<!-- e.g. "Mobile users" excludes iPad — we count iPad as desktop -->

## Methodology
<!-- e.g. Use SIF (Severity × Impact × Frequency), not RICE -->

## Style
<!-- e.g. PRDs in Russian for VK products, English for international -->
<!-- e.g. Don't use phrase "leverage" — corp-speak -->

## Process
<!-- e.g. Always need VP Product approval before Gates -->
<!-- e.g. Dev estimates require 1-week buffer for QA -->
```

**`pm-profile.md`** — personal profile of the PM (role, company, methodology preferences, recurring stakeholders, domain knowledge). Claude reads at every session start to tailor responses without re-asking.

If `pm-profile.md` doesn't exist in the target directory, create it with this template:

```markdown
# PM Profile

> Your personal profile. Claude reads this at every session start to tailor
> responses. Fields fill in over time as Claude learns from your work.
>
> You can also edit directly. Sections marked [auto] grow automatically;
> sections without the marker are for you to fill (or for Claude to ask
> about during FIRST LAUNCH).

## Role
- **Name**: [filled by init from .pm-local]
- **Title**: [e.g. Product Lead, Senior PM, etc. — Claude asks during FIRST LAUNCH]
- **Company**: [your company]
- **Team**: [your team / area of responsibility]

## Active products [auto]
<!-- Claude appends as you work on initiatives.
     e.g. - VK Видео (social discovery) — 3 active initiatives -->

## Working style [auto]
<!-- Claude appends as it observes recurring patterns.
     e.g. - Methodology: SIF for problems, ICE for solutions
          - PRD style: terse, mixed Russian/English OK
          - Hypothesis format: SIF score + kill-signal + what-to-validate -->

## Recurring stakeholders [auto]
<!-- Claude appends when the same names show up across initiatives.
     e.g. - VP Product (final approver at Gates)
          - Lead Designer Аня (involved from sketch step) -->

## Domain knowledge [auto]
<!-- Claude appends when it observes constants about your product/market.
     e.g. - User base ~80% mobile, 20% web
          - Common segments: новые/возвращающиеся, активные/спящие, платящие -->

## Constraints / context
<!-- e.g. - Working in a regulated market
          - Russian-speaking user base primarily -->
```

### Step 4: Tell the user what to do next

After successful copy, show the user this exact set of next steps. **The cd step is critical** — Claude loads CLAUDE.md from the working directory, so the user MUST be in the scaffolded directory when they restart Claude Code.

```
✓ Product Discovery pipeline scaffolded into <ABSOLUTE_PATH>

NEXT STEPS — run these in your terminal:

  pip3 install rich                          # install dashboard (macOS often only has pip3)
  /exit                                       # exit this Claude Code session
  cd "<ABSOLUTE_PATH>" && claude              # ⚠ MUST cd into the scaffolded dir before launching claude

In the new Claude Code session, send any message —
Claude will show the welcome screen and ask:
  "What product problem are you working on?"
```

Substitute `<ABSOLUTE_PATH>` with the absolute path you scaffolded into. Use double quotes — the path may contain spaces.

**Why cd matters**: Claude Code loads `CLAUDE.md` from the current working directory at session start. If the user runs `claude` from anywhere else (like home), the pipeline's CLAUDE.md won't load and Claude won't know about Product Discovery. This is the #1 user error — emphasize it.

**If `pip3` also fails**: try `python3 -m pip install rich`.

### Step 5: Stop here

Don't run status.py, don't try to start the pipeline. CLAUDE.md only takes effect after Claude Code restarts. Tell the user to restart and end the response.

## Edge cases

- **`CLAUDE_PLUGIN_ROOT` is empty or unset**: tell the user "Plugin install appears broken. Try: `/plugin uninstall product-discovery && /plugin install product-discovery`"
- **No write permission**: surface the OS error verbatim. Don't suggest `sudo` automatically — that's risky for files going into a project directory.
- **Source files missing in plugin install**: if `ls "$PLUGIN_ROOT/CLAUDE.md"` fails, the plugin is corrupted. Tell user to reinstall.
- **User wants to update an already-scaffolded project**: suggest `cd` to a fresh directory or use `COPY_FLAG=-f` to overwrite (warning: overwrites their CLAUDE.md customizations).

## Why this skill exists

Product Discovery is a Claude Code-native pipeline. Its core lives in `CLAUDE.md` (auto-loaded by Claude on every session) and in `.claude/skills/` + `.claude/rules/`. Plugins ship those files, but Claude Code doesn't auto-inject `CLAUDE.md` from a plugin into the user's project — files in `.claude/` plugin directories are loaded into the plugin's own context, not the user's project.

So we use a one-time scaffold step to copy the necessary files into the user's project directory. After that, the project works as a standalone Product Discovery setup — the user can iterate without further plugin involvement, push to their own git repo, customize CLAUDE.md, etc.
