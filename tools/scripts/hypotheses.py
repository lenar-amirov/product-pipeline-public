#!/usr/bin/env python3
"""
hypotheses.py — hypothesis registry engine (E1, roadmap 0.8).

The registry `output/hypotheses.json` is the single source of truth for
hypothesis STATE: status, evidence type, confidence, sources, history.
Narrative markdown (hypotheses.md, validated-hypotheses.md) stays authored
prose; `render` generates a summary view `output/registry.md` from the JSON.

Zero dependencies by design (stdlib only) — the SessionStart hook must work
on a fresh fork with bare python3.

Usage:
  hypotheses.py validate <initiative_dir>
  hypotheses.py render   <initiative_dir>
  hypotheses.py show     <initiative_dir> [ID]
  hypotheses.py add      <initiative_dir> <ID> --title T [--type X] [--confidence C]
                         [--status S] [--track A|B|cross] [--tag TAG]
                         [--note N] [--source FILE::REF]
  hypotheses.py set      <initiative_dir> <ID> [--status S] [--type X]
                         [--confidence C] [--note N] [--add-source FILE::REF]
                         [--link-solution SID]

Sources are passed as "path/to/file.md::free-form reference".
Every state change made via `set` is appended to the hypothesis history
automatically with today's date.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

EVIDENCE_TYPES = {
    # type: (min_confidence, max_confidence) — see .claude/rules/evidence-typing.md
    "REAL": (0.6, 1.0),
    "SYNTHETIC": (0.2, 0.4),
    "INFERRED": (0.3, 0.5),
    "AMBIGUOUS": (0.1, 0.3),
}

STATUSES = ["draft", "testing", "confirmed", "refuted", "reframed", "parked"]

STATUS_ICONS = {
    "draft": "○",
    "testing": "⚠️",
    "confirmed": "✅",
    "refuted": "❌",
    "reframed": "🎯",
    "parked": "⏸",
}

REGISTRY_REL = Path("output") / "hypotheses.json"
VIEW_REL = Path("output") / "registry.md"


def registry_path(initiative_dir: str) -> Path:
    return Path(initiative_dir) / REGISTRY_REL


def load(initiative_dir: str) -> dict:
    path = registry_path(initiative_dir)
    if not path.exists():
        return {"version": 1, "hypotheses": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(initiative_dir: str, data: dict) -> None:
    data["updated"] = date.today().isoformat()
    path = registry_path(initiative_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find(data: dict, hid: str) -> dict:
    for h in data["hypotheses"]:
        if h["id"] == hid:
            return h
    return None


# ---------------------------------------------------------------- validate

def validate(data: dict) -> tuple:
    """Return (errors, warnings) as lists of strings."""
    errors, warnings = [], []
    seen = set()
    for h in data.get("hypotheses", []):
        hid = h.get("id", "<no id>")
        prefix = f"[{hid}]"
        if hid in seen:
            errors.append(f"{prefix} duplicate id")
        seen.add(hid)
        if not h.get("title"):
            errors.append(f"{prefix} missing title")

        status = h.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix} unknown status '{status}' (allowed: {', '.join(STATUSES)})")

        etype = h.get("evidence_type")
        conf = h.get("confidence")
        if etype not in EVIDENCE_TYPES:
            errors.append(f"{prefix} unknown evidence_type '{etype}'")
        elif conf is not None:
            if not isinstance(conf, (int, float)) or not 0.0 <= conf <= 1.0:
                errors.append(f"{prefix} confidence {conf!r} is not a number in [0, 1]")
            else:
                lo, hi = EVIDENCE_TYPES[etype]
                if not lo <= conf <= hi:
                    warnings.append(
                        f"{prefix} confidence {conf} outside {etype} range "
                        f"[{lo}–{hi}] — retype the evidence or fix the number"
                    )

        if etype == "REAL" and not h.get("sources"):
            errors.append(f"{prefix} evidence_type REAL requires at least one source")

        for s in h.get("sources", []):
            if not s.get("file"):
                warnings.append(f"{prefix} source without file reference")

        if "data_inconsistency" in h.get("flags", []) and (conf or 0) > 0.6:
            warnings.append(
                f"{prefix} flagged data_inconsistency but confidence {conf} > 0.6 — "
                f"downgrade until sources are reconciled"
            )
    return errors, warnings


# ------------------------------------------------------------------ render

def render(data: dict) -> str:
    today = date.today().isoformat()
    lines = [
        "# Hypothesis Registry",
        "",
        f"> Generated {today} by `tools/scripts/hypotheses.py render` from "
        f"`output/hypotheses.json`. Do not edit — change the JSON (or use "
        f"`hypotheses.py set`) and re-render.",
        "",
    ]
    hyps = data.get("hypotheses", [])
    if not hyps:
        lines.append("_Registry is empty. Add hypotheses with `hypotheses.py add`._")
        return "\n".join(lines) + "\n"

    lines += [
        "| ID | Hypothesis | Status | Evidence | Confidence | Sources |",
        "|---|---|---|---|---|---|",
    ]
    for h in hyps:
        icon = STATUS_ICONS.get(h.get("status", ""), "?")
        lines.append(
            f"| {h['id']} | {h.get('title', '')} "
            f"| {icon} {h.get('status', '?')} "
            f"| {h.get('evidence_type', '?')} "
            f"| {h.get('confidence', '—')} "
            f"| {len(h.get('sources', []))} |"
        )
    lines.append("")

    for h in hyps:
        icon = STATUS_ICONS.get(h.get("status", ""), "?")
        lines.append(f"## {h['id']} — {h.get('title', '')}")
        lines.append("")
        meta = (
            f"**{icon} {h.get('status', '?')}** · "
            f"{h.get('evidence_type', '?')} {h.get('confidence', '—')}"
        )
        if h.get("track"):
            meta += f" · track {h['track']}"
        if h.get("tag"):
            meta += f" · [{h['tag']}]"
        if h.get("flags"):
            meta += " · ⚠️ " + ", ".join(h["flags"])
        lines.append(meta)
        if h.get("note"):
            lines.append("")
            lines.append(h["note"])
        if h.get("sources"):
            lines.append("")
            lines.append("Sources:")
            for s in h["sources"]:
                ref = f" — {s['ref']}" if s.get("ref") else ""
                stype = f" ({s['type']})" if s.get("type") else ""
                lines.append(f"- `{s.get('file', '?')}`{ref}{stype}")
        if h.get("solutions"):
            lines.append("")
            lines.append("Solutions: " + ", ".join(h["solutions"]))
        if h.get("history"):
            lines.append("")
            lines.append("History:")
            for e in h["history"]:
                lines.append(f"- {e.get('date', '?')}: {e.get('change', '')}")
        lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------- mutate

def parse_source(spec: str) -> dict:
    if "::" in spec:
        file_part, ref = spec.split("::", 1)
    else:
        file_part, ref = spec, ""
    return {"file": file_part.strip(), "ref": ref.strip(),
            "date": date.today().isoformat()}


def add_history(h: dict, change: str) -> None:
    h.setdefault("history", []).append(
        {"date": date.today().isoformat(), "change": change})


def cmd_add(args) -> int:
    data = load(args.initiative_dir)
    if find(data, args.id):
        print(f"error: {args.id} already exists (use `set` to modify)")
        return 1
    h = {
        "id": args.id,
        "title": args.title,
        "status": args.status,
        "evidence_type": args.type,
        "confidence": args.confidence,
        "sources": [],
        "history": [],
        "solutions": [],
    }
    if args.track:
        h["track"] = args.track
    if args.tag:
        h["tag"] = args.tag
    if args.note:
        h["note"] = args.note
    if args.source:
        src = parse_source(args.source)
        src["type"] = args.type
        h["sources"].append(src)
    add_history(h, f"created: {args.type} {args.confidence}, status {args.status}")
    data["hypotheses"].append(h)
    save(args.initiative_dir, data)
    print(f"added {args.id} ({args.type} {args.confidence}, {args.status})")
    return 0


def cmd_set(args) -> int:
    data = load(args.initiative_dir)
    h = find(data, args.id)
    if not h:
        print(f"error: {args.id} not found")
        return 1
    changes = []
    if args.status and args.status != h.get("status"):
        changes.append(f"status: {h.get('status')} → {args.status}")
        h["status"] = args.status
    if args.type or args.confidence is not None:
        old = f"{h.get('evidence_type')} {h.get('confidence')}"
        if args.type:
            h["evidence_type"] = args.type
        if args.confidence is not None:
            h["confidence"] = args.confidence
        new = f"{h.get('evidence_type')} {h.get('confidence')}"
        if old != new:
            changes.append(f"{old} → {new}")
    if args.add_source:
        src = parse_source(args.add_source)
        src["type"] = h.get("evidence_type")
        h.setdefault("sources", []).append(src)
        changes.append(f"source added: {src['file']}")
    if args.link_solution:
        h.setdefault("solutions", [])
        if args.link_solution not in h["solutions"]:
            h["solutions"].append(args.link_solution)
            changes.append(f"solution linked: {args.link_solution}")
    if args.flag:
        h.setdefault("flags", [])
        if args.flag not in h["flags"]:
            h["flags"].append(args.flag)
            changes.append(f"flag set: {args.flag}")
    if args.unflag and args.unflag in h.get("flags", []):
        h["flags"].remove(args.unflag)
        changes.append(f"flag cleared: {args.unflag}")
    if not changes and not args.note:
        print("nothing to change")
        return 0
    change_str = "; ".join(changes) if changes else "note"
    if args.note:
        h["note"] = args.note
        change_str += f" — {args.note}" if changes else f"note: {args.note}"
    add_history(h, change_str)
    save(args.initiative_dir, data)
    print(f"{args.id}: {change_str}")
    return 0


# -------------------------------------------------------------------- cli

def cmd_validate(args) -> int:
    data = load(args.initiative_dir)
    if not registry_path(args.initiative_dir).exists():
        print("no registry (output/hypotheses.json) — nothing to validate")
        return 0
    errors, warnings = validate(data)
    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"WARNING {w}")
    n = len(data.get("hypotheses", []))
    by_status = {}
    for h in data.get("hypotheses", []):
        by_status[h.get("status", "?")] = by_status.get(h.get("status", "?"), 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(by_status.items()))
    print(f"{n} hypotheses ({summary}); {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def cmd_render(args) -> int:
    data = load(args.initiative_dir)
    out = Path(args.initiative_dir) / VIEW_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    print(f"rendered {out}")
    return 0


def cmd_show(args) -> int:
    data = load(args.initiative_dir)
    if args.id:
        h = find(data, args.id)
        if not h:
            print(f"error: {args.id} not found")
            return 1
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        for h in data.get("hypotheses", []):
            icon = STATUS_ICONS.get(h.get("status", ""), "?")
            print(f"{h['id']:6} {icon} {h.get('status', '?'):10} "
                  f"{h.get('evidence_type', '?'):10} {h.get('confidence', '—')}"
                  f"  {h.get('title', '')}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = p.add_subparsers(dest="command", required=True)

    def base(sp):
        sp.add_argument("initiative_dir", help="initiative folder (contains output/)")

    base(sub.add_parser("validate"))
    base(sub.add_parser("render"))
    sp = sub.add_parser("show")
    base(sp)
    sp.add_argument("id", nargs="?")

    sp = sub.add_parser("add")
    base(sp)
    sp.add_argument("id")
    sp.add_argument("--title", required=True)
    sp.add_argument("--type", default="INFERRED", choices=sorted(EVIDENCE_TYPES))
    sp.add_argument("--confidence", type=float, default=0.3)
    sp.add_argument("--status", default="draft", choices=STATUSES)
    sp.add_argument("--track")
    sp.add_argument("--tag")
    sp.add_argument("--note")
    sp.add_argument("--source", help='FILE::REF')

    sp = sub.add_parser("set")
    base(sp)
    sp.add_argument("id")
    sp.add_argument("--status", choices=STATUSES)
    sp.add_argument("--type", choices=sorted(EVIDENCE_TYPES))
    sp.add_argument("--confidence", type=float)
    sp.add_argument("--note")
    sp.add_argument("--add-source", help='FILE::REF')
    sp.add_argument("--link-solution")
    sp.add_argument("--flag", help='e.g. data_inconsistency')
    sp.add_argument("--unflag")

    args = p.parse_args()
    handler = {
        "validate": cmd_validate,
        "render": cmd_render,
        "show": cmd_show,
        "add": cmd_add,
        "set": cmd_set,
    }[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
