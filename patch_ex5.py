#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
start = end = None
for i, l in enumerate(lines):
    st = l.strip()
    if st.startswith("ex_html += ") and "grid" in st:
        start = i
    if start is not None and st.startswith("ex_html += ") and "</div>" in st:
        end = i
        break
print("block:", start, end)
assert start is not None and end is not None
def q(s): return S + s + S
block = [
    "            ex_html += " + q("<h3>") + " + html.escape(ex2[" + D + "title" + D + "]) + " + q("</h3>"),
    "            ex_html += " + q("<div style=" + D + "display:grid;grid-template-columns:1fr 1fr;gap:10px" + D + ">"),
    "            ex_html += " + q("<figure style=" + D + "margin:0" + D + ">"),
    "            ex_html += " + q("<div style=" + D + "background:#1d4d2b;color:#a8e6a3;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">OK PROMPT</div>"),
    "            ex_html += " + q("<img src=" + D) + " + base + s2 + " + q("-good.jpg") + " + q(" + D + " loading=" + D + "lazy" + D + " style=" + D + "width:100%;border-radius:0 0 10px 10px" + D + ">"),
    "            ex_html += " + q("<figcaption style=" + D + "font-size:.75rem;color:#a8e6a3;line-height:1.7;margin-top:.35rem" + D + ">") + " + html.escape(ex2[" + D + "good_cap" + D + "]) + " + q("</figcaption>"),
    "            ex_html += " + q("</figure>"),
    "            ex_html += " + q("<figure style=" + D + "margin:0" + D + ">"),
    "            ex_html += " + q("<div style=" + D + "background:#4d1d1d;color:#e6a8a8;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">WEAK</div>"),
    "            ex_html += " + q("<img src=" + D) + " + base + s2 + " + q("-bad.jpg") + " + q(" + D + " loading=" + D + "lazy" + D + " style=" + D + "width:100%;border-radius:0 0 10px 10px;opacity:.85" + D + ">"),
    "            ex_html += " + q("<figcaption style=" + D + "font-size:.75rem;color:#cbb8d4;line-height:1.7;margin-top:.35rem" + D + ">") + " + html.escape(ex2[" + D + "bad_cap" + D + "]) + " + q("</figcaption>"),
    "            ex_html += " + q("</figure>"),
    "            ex_html += " + q("</div>"),
]
lines[start:end+1] = block
P.write_text(chr(10).join(lines), encoding="utf-8")
print("done")
