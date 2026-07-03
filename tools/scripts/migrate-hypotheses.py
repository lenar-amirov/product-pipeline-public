#!/usr/bin/env python3
"""
migrate-hypotheses.py — best-effort conversion of legacy markdown hypothesis
registries into output/hypotheses.json (E1, roadmap 0.8).

Reads (if present):
  output/hypotheses.md            — draft registry (### P1. [tag] Title)
  output/validated-hypotheses.md  — verdicts (### P8 [tag] ✅ ... REAL 0.75);
                                    overrides draft entries by id

Usage:
  migrate-hypotheses.py <initiative_dir> [--force]

Writes output/hypotheses.json (refuses to overwrite without --force).
Migration is intentionally conservative: whatever can't be parsed keeps
defaults (INFERRED 0.4, draft) and is listed in the summary for manual review.
After migration run:
  hypotheses.py validate <dir>   — the validator flags real defects
  hypotheses.py render <dir>     — generate output/registry.md
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

TYPE_CONF_RE = re.compile(
    r"(REAL|SYNTHETIC|INFERRED|AMBIGUOUS)\s*([01]?\.\d+)?")
DRAFT_HEADER_RE = re.compile(
    r"^###\s+(P\d+[a-z]?)\.?\s+\[([^\]]+)\]\s*(.*)$")
VALIDATED_HEADER_RE = re.compile(
    r"^###\s+(P\d+[a-z]?)\.?\s*\[([^\]]+)\]\s*(.*)$")
TRACK_RE = re.compile(r"^##\s+Трек\s+([AB])", re.IGNORECASE)

STATUS_BY_EMOJI = [
    ("❌", "refuted"),
    ("🎯", "reframed"),
    ("✅", "confirmed"),
    ("⚠️", "testing"),
]


def parse_draft(path: Path) -> dict:
    """id -> partial hypothesis from the draft registry."""
    result = {}
    if not path.exists():
        return result
    track = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = TRACK_RE.match(line)
        if m:
            track = m.group(1).upper()
            continue
        m = DRAFT_HEADER_RE.match(line)
        if not m:
            continue
        hid, tag, rest = m.groups()
        # Title = remainder up to first bold marker / emoji clutter
        title = re.split(r"\s*\*\*", rest)[0].replace("🆕", "").strip()
        result[hid] = {
            "id": hid,
            "title": title or tag,
            "tag": tag.strip(),
            "track": track,
            "status": "draft",
            "evidence_type": "INFERRED",
            "confidence": 0.4,
        }
    return result


def parse_validated(path: Path) -> dict:
    """id -> verdict overlay from validated-hypotheses.md."""
    result = {}
    if not path.exists():
        return result
    track = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = TRACK_RE.match(line)
        if m:
            track = m.group(1).upper()
            continue
        m = VALIDATED_HEADER_RE.match(line)
        if not m:
            continue
        hid, tag, rest = m.groups()
        status = None
        for emoji, st in STATUS_BY_EMOJI:
            if emoji in rest:
                status = st
                break
        # Last "TYPE conf" mention in the header = final state
        etype, conf = None, None
        for tm in TYPE_CONF_RE.finditer(rest):
            etype = tm.group(1)
            if tm.group(2):
                conf = float(tm.group(2))
        entry = {
            "id": hid,
            "tag": tag.strip(),
            "track": track,
            "verdict_line": rest.strip(),
        }
        if status:
            entry["status"] = status
        if etype:
            entry["evidence_type"] = etype
        if conf is not None:
            entry["confidence"] = conf
        result[hid] = entry
    return result


def migrate(initiative_dir: Path) -> dict:
    draft = parse_draft(initiative_dir / "output" / "hypotheses.md")
    validated = parse_validated(
        initiative_dir / "output" / "validated-hypotheses.md")
    today = date.today().isoformat()

    merged = {}
    for hid, h in draft.items():
        merged[hid] = h
    for hid, v in validated.items():
        base = merged.get(hid, {
            "id": hid,
            "title": v["tag"],
            "tag": v["tag"],
            "track": v.get("track"),
            "status": "draft",
            "evidence_type": "INFERRED",
            "confidence": 0.4,
        })
        note = v.pop("verdict_line", "")
        history_change = (
            f"migrated verdict from validated-hypotheses.md: {note}"
            if note else "migrated from validated-hypotheses.md")
        base.update({k: val for k, val in v.items() if val is not None})
        base["note"] = note
        base.setdefault("history", []).append(
            {"date": today, "change": history_change})
        merged[hid] = base

    hyps = []
    for hid in sorted(merged, key=lambda x: (x[1:].zfill(4), x)):
        h = merged[hid]
        h.setdefault("history", []).append(
            {"date": today, "change": "migrated from legacy markdown registry"})
        h.setdefault("sources", [])
        h.setdefault("solutions", [])
        if h.get("evidence_type") == "REAL" and not h["sources"]:
            h["sources"].append({
                "file": "output/validated-hypotheses.md",
                "ref": f"карточка {hid} (миграция — уточните первоисточник)",
                "type": "REAL",
                "date": today,
            })
        if h.get("track") is None:
            h.pop("track", None)
        hyps.append(h)

    return {"version": 1, "hypotheses": hyps}


def main() -> int:
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    if len(args) != 1:
        print(__doc__)
        return 2
    initiative_dir = Path(args[0])
    out = initiative_dir / "output" / "hypotheses.json"
    if out.exists() and not force:
        print(f"error: {out} already exists — use --force to overwrite")
        return 1

    data = migrate(initiative_dir)
    if not data["hypotheses"]:
        print("nothing to migrate: no parsable headers found in "
              "output/hypotheses.md / output/validated-hypotheses.md")
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"migrated {len(data['hypotheses'])} hypotheses → {out}")
    for h in data["hypotheses"]:
        print(f"  {h['id']:6} {h.get('status', '?'):10} "
              f"{h.get('evidence_type', '?'):10} {h.get('confidence', '—')}"
              f"  {h.get('title', '')[:60]}")
    print("review sources for REAL hypotheses (migration points at the "
          "narrative file, not the original evidence), then run "
          "`hypotheses.py validate` and `hypotheses.py render`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
