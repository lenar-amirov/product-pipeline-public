#!/usr/bin/env python3
"""
render-ost.py — Opportunity Solution Tree from the hypothesis registry (E13).

Teresa Torres' OST as a generated view: outcome (from CONTEXT.md metric) →
problem hypotheses (colored by status/evidence) → linked solutions.
Emits Mermaid inside markdown: output/ost.md (renders on GitHub and in most
markdown viewers; no dependencies).

Usage:
  render-ost.py <initiative_dir>
"""

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hypotheses as registry  # noqa: E402

STATUS_STYLE = {
    # status -> (emoji, mermaid class)
    "confirmed": ("✅", "confirmed"),
    "reframed": ("🎯", "confirmed"),
    "testing": ("⚠️", "testing"),
    "draft": ("○", "draft"),
    "refuted": ("❌", "refuted"),
    "parked": ("⏸", "draft"),
}

CLASS_DEFS = """\
  classDef outcome fill:#1f6feb,color:#fff,stroke:#1f6feb;
  classDef confirmed fill:#dafbe1,stroke:#1a7f37,color:#1a4d2e;
  classDef testing fill:#fff8c5,stroke:#9a6700,color:#4d3800;
  classDef draft fill:#f6f8fa,stroke:#8b949e,color:#57606a;
  classDef refuted fill:#ffebe9,stroke:#cf222e,color:#82061e;
  classDef solution fill:#ddf4ff,stroke:#0969da,color:#0a3069;"""


def outcome_from_context(init_dir: Path) -> str:
    ctx = init_dir / "CONTEXT.md"
    if not ctx.exists():
        return "Outcome"
    text = ctx.read_text(encoding="utf-8")
    m = re.search(
        r"\*\*(?:Metric we're improving|Метрика, которую улучшаем)\*\*:\s*(.+)",
        text)
    if not m:
        return "Outcome"
    val = " ".join(m.group(1).split())
    return val[:80] if not val.startswith("[") else "Outcome"


def esc(label: str) -> str:
    """Mermaid-safe node label."""
    return label.replace('"', "'").replace("[", "(").replace("]", ")")[:70]


def render(init_dir: Path) -> str:
    data = registry.load(str(init_dir))
    hyps = data.get("hypotheses", [])
    outcome = outcome_from_context(init_dir)
    today = date.today().isoformat()

    lines = [
        "# Opportunity Solution Tree",
        "",
        f"> Generated {today} by `tools/scripts/render-ost.py` from "
        f"`output/hypotheses.json`. Do not edit — change the registry and "
        f"re-render.",
        "",
        "```mermaid",
        "flowchart TD",
        f'  OUT(["🎯 {esc(outcome)}"]):::outcome',
    ]

    tracks = sorted({h.get("track") for h in hyps if h.get("track")})
    for t in tracks:
        lines.append(f'  OUT --> T{t}["Track {t}"]:::draft')

    for h in hyps:
        emoji, cls = STATUS_STYLE.get(h.get("status", "draft"), ("?", "draft"))
        conf = f" {h.get('evidence_type', '')} {h.get('confidence', '')}".rstrip()
        node = f'  {h["id"]}["{emoji} {h["id"]}: {esc(h.get("title", ""))}<br/><i>{conf}</i>"]:::{cls}'
        lines.append(node)
        parent = f"T{h['track']}" if h.get("track") in tracks else "OUT"
        lines.append(f"  {parent} --> {h['id']}")
        for s in h.get("solutions", []):
            sid = re.sub(r"[^A-Za-z0-9_]", "_", s)
            lines.append(f'  {h["id"]} --> SOL_{sid}["💡 {esc(s)}"]:::solution')

    lines.append(CLASS_DEFS)
    lines.append("```")
    lines.append("")
    lines.append("Legend: ✅ confirmed · 🎯 reframed · ⚠️ testing · ○ draft · "
                 "❌ refuted · 💡 solution")
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    init_dir = Path(sys.argv[1])
    out = init_dir / "output" / "ost.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(init_dir), encoding="utf-8")
    print(f"rendered {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
