#!/usr/bin/env python3
"""Static, dependency-free dashboard exporter for a single initiative.

Fallback for environments where the Flask app (tools/web/app.py) can't run
(no flask/markdown, no network). Reads status.json + the initiative's markdown
docs and emits a self-contained HTML file (inline CSS, no external assets).

Usage: python3 tools/web/static_export.py <pm>/<initiative> [out.html]
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from pipeline_constants import PIPELINE_STEPS, DEFAULT_TOTAL  # noqa: E402

STEPS = [(num, cmd) for num, cmd, _phase, _label in PIPELINE_STEPS]

DOCS = [
    ("Hypotheses", "output/hypotheses.md"),
    ("Analytics data (REAL)", "research/analytics-data.md"),
    ("Competitive analysis", "research/competitive-analysis.md"),
    ("Analytics brief", "research/analytics-brief.md"),
    ("Survey questions", "research/survey-questions.md"),
    ("Synthetic interviews", "research/synthetic-interviews.md"),
    ("PRD", "output/PRD.md"),
    ("Decision log", "output/decisions.md"),
]

STATUS_COLORS = {
    "done": "#1a7f37", "in_progress": "#1f6feb", "paused": "#9a6700",
    "pending": "#8b949e", "skipped": "#6e7781",
}


def md_to_html(md: str) -> str:
    """Tiny markdown renderer: headings, bold, code, tables, lists, links, blockquotes."""
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t

    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        # code fence
        if ln.startswith("```"):
            buf = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre class='code'>" + "\n".join(buf) + "</pre>")
            continue
        # table
        if "|" in ln and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|", lines[i + 1]):
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            t += "</tbody></table>"
            out.append(t)
            continue
        # heading
        m = re.match(r"^(#{1,6})\s+(.*)", ln)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        # blockquote
        if ln.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(inline(lines[i].lstrip(">").strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(buf) + "</blockquote>")
            continue
        # hr
        if re.match(r"^---+$", ln.strip()):
            out.append("<hr>")
            i += 1
            continue
        # list
        if re.match(r"^\s*[-*]\s+", ln):
            buf = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                buf.append("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            buf = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                buf.append("<li>" + inline(re.sub(r"^\s*\d+\.\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("<ol>" + "".join(buf) + "</ol>")
            continue
        # paragraph
        out.append("<p>" + inline(ln) + "</p>")
        i += 1
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("usage: static_export.py <pm>/<initiative> [out.html]")
        sys.exit(1)
    root = Path(__file__).resolve().parents[2]
    init = root / sys.argv[1]
    status = json.loads((init / "output" / "status.json").read_text())
    steps = status.get("steps", {})
    cfg = status.get("pipeline_config", {})
    done = sum(1 for s in steps.values() if s.get("status") == "done")
    total = DEFAULT_TOTAL

    rows = []
    for num, name in STEPS:
        st = steps.get(str(num) if num == int(num) else str(num), {})
        status_v = st.get("status", "pending")
        color = STATUS_COLORS.get(status_v, "#8b949e")
        summ = html.escape(st.get("summary") or "")
        date = st.get("date") or ""
        rows.append(
            f"<tr><td class='num'>{num}</td><td>{html.escape(name)}</td>"
            f"<td><span class='badge' style='background:{color}'>{status_v}</span></td>"
            f"<td class='date'>{date}</td><td class='summ'>{summ}</td></tr>"
        )

    pending = status.get("pending", {})
    pend_rows = "".join(
        f"<li><b>{html.escape(k)}</b>: {html.escape(str(v))}</li>"
        for k, v in pending.items() if v
    ) or "<li>—</li>"

    doc_sections = []
    for title, rel in DOCS:
        p = init / rel
        if not p.exists():
            continue
        body = md_to_html(p.read_text())
        doc_sections.append(
            f"<details><summary>{html.escape(title)} "
            f"<span class='path'>{html.escape(rel)}</span></summary>"
            f"<div class='doc'>{body}</div></details>"
        )

    pm = status.get("pm", "")
    name = status.get("initiative", "")
    tpl = cfg.get("template", "")
    pct = int(done / total * 100)

    htmlout = f"""<!doctype html><html lang=ru><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>{html.escape(name)} — Product Discovery</title>
<style>
:root{{--bg:#f6f8fa;--card:#ffffff;--bd:#d8dee4;--fg:#1f2328;--mut:#636c76;--acc:#0969da}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:1100px;margin:0 auto;padding:28px 20px 80px}}
h1{{font-size:26px;margin:0 0 4px}} .sub{{color:var(--mut);margin-bottom:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}}
.kpi{{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:14px;box-shadow:0 1px 3px rgba(31,35,40,.06)}}
.kpi .v{{font-size:22px;font-weight:700}} .kpi .l{{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
.bar{{height:10px;background:#eaeef2;border-radius:6px;overflow:hidden;margin:6px 0 0}}
.bar>i{{display:block;height:100%;background:linear-gradient(90deg,#0969da,#1a7f37);width:{pct}%}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:18px;margin:18px 0;box-shadow:0 1px 3px rgba(31,35,40,.06)}}
h2{{font-size:18px;margin:0 0 12px;border-bottom:1px solid var(--bd);padding-bottom:8px}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid var(--bd);padding:6px 9px;text-align:left;vertical-align:top}}
th{{background:#f0f3f6;color:var(--mut);font-weight:600}}
.num{{color:var(--mut);width:34px}} .date{{color:var(--mut);white-space:nowrap;font-size:12px}}
.summ{{color:#42484f;font-size:12.5px}} .badge{{color:#fff;border-radius:20px;padding:2px 9px;font-size:11px;font-weight:600}}
.funnel{{display:flex;flex-direction:column;gap:4px;max-width:560px}}
.fr{{display:flex;align-items:center;gap:10px}} .fbar{{background:var(--acc);height:30px;border-radius:5px;min-width:4px}}
.fr .lab{{width:170px;flex:none;color:var(--mut);font-size:12px;text-align:right}}
.fr .val{{font-size:12px;font-weight:700;color:var(--fg);white-space:nowrap}}
.drop{{color:#cf222e;font-size:12px;font-weight:700;white-space:nowrap}}
details{{background:var(--card);border:1px solid var(--bd);border-radius:10px;margin:10px 0;box-shadow:0 1px 3px rgba(31,35,40,.06)}}
summary{{cursor:pointer;padding:12px 16px;font-weight:600;user-select:none}}
.path{{color:var(--mut);font-weight:400;font-size:12px;font-family:ui-monospace,monospace}}
.doc{{padding:0 18px 16px;border-top:1px solid var(--bd);font-size:13.5px;overflow-x:auto}}
.doc h1{{font-size:19px}} .doc h2{{font-size:16px}} .doc h3{{font-size:14px;border:0}}
.doc code{{background:#eff1f3;padding:1px 5px;border-radius:4px;font-size:12px}}
.doc pre.code{{background:#f6f8fa;border:1px solid var(--bd);border-radius:8px;padding:12px;overflow-x:auto;font-size:12px}}
.doc table{{font-size:12px;margin:10px 0}} .doc blockquote{{border-left:3px solid var(--acc);margin:10px 0;padding:4px 12px;color:var(--mut)}}
.doc a{{color:var(--acc)}} a{{color:var(--acc)}}
.flag{{background:#fff8e6;border:1px solid #d4a72c;border-radius:8px;padding:10px 14px;margin:8px 0;font-size:13px}}
</style></head><body><div class=wrap>
<h1>{html.escape(name)}</h1>
<div class=sub>PM: {html.escape(pm)} · template: <b>{html.escape(tpl)}</b> · north-star «видели→заказ» = <b>1.4%</b></div>

<div class=grid>
  <div class=kpi><div class=l>Прогресс</div><div class=v>{done}/{total}</div><div class=bar><i></i></div></div>
  <div class=kpi><div class=l>Обрыв A · видят→клик</div><div class=v>24.9%</div><div class=l>потеря ~41M</div></div>
  <div class=kpi><div class=l>Обрыв B · клик→заказ</div><div class=v>7.3%</div><div class=l>потеря ~12.6M</div></div>
  <div class=kpi><div class=l>Заказов/день (REAL)</div><div class=v>52.6K</div><div class=l>27% Озон</div></div>
</div>

<div class=card><h2>Воронка зрелости</h2><div class=funnel>
  <div class=fr><div class=lab>Видели 1+ шопс</div><div class=fbar style='width:100%'></div><span class=val>71.77M</span></div>
  <div class=fr><div class=lab>Видели 5+</div><div class=fbar style='width:76.4%'></div><span class=val>54.83M</span><span class=drop>76.4%</span></div>
  <div class=fr><div class=lab>Клик 1+ (обрыв A)</div><div class=fbar style='width:19.0%'></div><span class=val>13.64M</span><span class=drop>24.9%</span></div>
  <div class=fr><div class=lab>Заказ (обрыв B)</div><div class=fbar style='width:1.4%'></div><span class=val>1.0M</span><span class=drop>7.3%</span></div>
</div><div class=sub style='margin:10px 0 0;font-size:11.5px'>Ширина бара — доля от «видели 1+»; <span style='color:#cf222e;font-weight:700'>%</span> — конверсия шага к предыдущему.</div></div>

<div class=card><h2>🔑 Ключевые REAL-находки (дек «Опыт покупателя v7»)</h2>
  <div class=flag><b>P4a опровергнута:</b> сквозная конверсия из карточки — Озон <b>3.5%</b> 🥇 &gt; нативный чекаут 1% &gt; чаты/мессенджер 0.34–0.35%. Хендофф на Озон — НЕ leak, а сильнейший путь.</div>
  <div class=flag><b>P4b рычаг:</b> оплата подключена лишь в 5% заказов; подключённая оплата = <b>+491% CR</b> в сделку.</div>
  <div class=flag><b>P4c:</b> мессенджер — крупнейший канал (25K сделок/день), но вне механизмов e-com; 53% не отправляют сообщение.</div>
  <div class=flag><b>P8 подтверждена:</b> CTR в CTA по surface — Лента шопсов <b>21%</b> ≫ Клипы 13% ≫ Посты 4%. Контекст решает.</div>
</div>

<div class=card><h2>Pipeline ({done}/{total})</h2>
<table><thead><tr><th>#</th><th>Шаг</th><th>Статус</th><th>Дата</th><th>Итог</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<div class=card><h2>Pending</h2><ul>{pend_rows}</ul></div>

<div class=card><h2>Документы</h2>{''.join(doc_sections)}</div>

</div></body></html>"""

    out = Path(sys.argv[2]) if len(sys.argv) > 2 else init / "output" / "html" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(htmlout)
    print(out)


if __name__ == "__main__":
    main()
