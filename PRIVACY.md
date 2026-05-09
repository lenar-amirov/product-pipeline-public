# Privacy Policy — Product Discovery

**Last updated**: 2026-05-09

## TL;DR

Product Discovery is a **local-first** Claude Code plugin. It runs entirely on your machine. There is no server, no cloud backend, no analytics endpoint, no telemetry. We — the plugin maintainers — do not collect, store, or transmit your data. Anywhere.

The rest of this document explains what that means in practice and what third parties (Anthropic, GitHub, optional MCP servers you choose to connect) do receive when you use the plugin.

---

## What stays on your machine

Everything you produce while using the plugin lives in your local working directory:

- `.pm-local` — your name
- `pm-profile.md` — your role, company, working style
- `.product-corrections.md` — corrections you've taught Claude
- `.initiatives-digest.md` — auto-generated overview of your initiatives
- `{pm}/{initiative}/` — every initiative folder, including `CONTEXT.md`, `status.json`, `decisions.md`, hypotheses, PRD, presentations, GTM materials
- All research notes, CJM screenshots, dev estimates, AB test results

These files never leave your machine through the plugin itself. They sit on your local filesystem (typically gitignored). If you choose to commit them to a private git repo, that's your decision and goes to your git provider — not us.

---

## What goes to Anthropic

When you use Claude Code (which the plugin runs inside), the conversation between you and Claude is processed by **Anthropic**. This includes:

- Your messages to Claude
- Claude's responses
- File contents Claude reads or writes (`CLAUDE.md`, `CONTEXT.md`, your initiative artifacts) when they enter the conversation context
- Tool calls Claude makes (Bash, Read, Write, WebSearch, etc.)

This is governed by **your contract with Anthropic**, not by this plugin. See:
- [Anthropic Privacy Policy](https://www.anthropic.com/privacy)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

The plugin does not modify what Claude Code sends to Anthropic.

---

## What goes to GitHub

You interact with GitHub through:

- **Plugin install** — `/plugin marketplace add` clones this repository to your local Claude Code plugin cache. GitHub sees the clone request; it's the same as anyone cloning a public repo.
- **Plugin updates** — same as above, GitHub sees the fetch request.
- **Public Issues / Discussions** — anything you post publicly here (bug reports, feedback, questions) is public. Don't paste confidential strategy, internal metrics, customer names, or anything you wouldn't want indexed by search engines.

Use of GitHub is governed by **your contract with GitHub**: [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

---

## Optional integrations you choose to connect

The plugin supports — but does not require — these integrations:

| Integration | When it's used | What it sees |
|-------------|----------------|--------------|
| **Jira MCP** (`@anthropic/mcp-atlassian`) | If you set Tracker → Jira and run `/create-tickets` | Ticket data you push (titles, descriptions, acceptance criteria, priority, estimates) |
| **Linear MCP** (`@anthropic/mcp-linear`) | If you set Tracker → Linear | Same as above, in Linear format |
| **GitHub Issues** (via `gh` CLI) | If you set Tracker → GitHub Issues | Same as above, sent to your specified repo |
| **Figma MCP** | If you connect it (used at step 8 sketch / wireframes) | The Figma file URLs you reference |
| **Anthropic web search** | When Claude runs WebSearch (e.g., during competitor research) | The search query — handled by Anthropic |

You install these MCP servers separately and you control their credentials. The plugin only invokes them when relevant pipeline steps run, with data you've already authored locally. We do not proxy any of this through our own servers — there are no servers.

---

## What we (maintainers) collect

**Nothing automatically.** There is no telemetry, no usage ping, no install counter on our end.

Through GitHub's standard repository owner dashboard, we passively see:

- Aggregate **stars / forks / clones** for the repo (no per-user identifiers beyond what GitHub publicly exposes)
- **Public issue / discussion content** that contributors post
- **Traffic graphs** GitHub provides to repo owners (referrer URLs, popular files — aggregate only)

This is the same passive data any GitHub repo owner sees. We don't combine it with anything else, we don't sell it, we don't run it through analytics tools.

If Anthropic publishes the plugin in their marketplace, they may report install counts to us via their dashboard. The plugin code does not transmit this — Anthropic's marketplace does, and only because you installed it through their service.

---

## Public contributions

When you open an Issue, Discussion, or pull request on this repository:

- The content is **publicly visible** and indexed by search engines
- Your GitHub username and any data you include is public
- We may quote your feedback (anonymized or with your username, depending on context) in release notes, blog posts, or social media

If you want to share private feedback, use the optional contact field in the Feedback issue template, or reach out via the channels listed in the README.

---

## Children

Product Discovery is a tool for product managers. It is not directed at children under 16 and we don't knowingly accept contributions or feedback from children.

---

## Changes to this policy

If we change anything material, we'll:
1. Update the **Last updated** date at the top
2. Note the change in [`CHANGELOG.md`](./CHANGELOG.md)
3. For significant changes (e.g., introducing telemetry — which we don't plan), post a pinned Discussion announcement at least 30 days before the change takes effect

History of this file is available in [git log](https://github.com/lenar-amirov/product-pipeline-public/commits/main/PRIVACY.md).

---

## Contact

Privacy questions, concerns, or "wait, but what about X?":

- Open a Discussion (preferred — public answer helps others)
- File an Issue with the `feedback` template if it's specific
- For private inquiries, drop a contact in the Feedback template's optional contact field

Maintainer: Lenar Amirov ([@lenar-amirov](https://github.com/lenar-amirov))

---

**Plain summary in one paragraph**: this plugin runs locally and does not collect data. Anthropic processes the conversation you have with Claude Code. GitHub sees that you cloned a public repo. Anything else in your filesystem stays in your filesystem. Public Issues and Discussions are public.
