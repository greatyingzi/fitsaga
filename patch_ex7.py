#!/usr/bin/env python3
import pathlib, re
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
src = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39); NL = chr(10)
pat_str = "ex_html " + chr(43) + "= .*grid.*" + NL + "(.*" + NL + ")*?" + "ex_html " + chr(43) + "= " + S + "</div>" + S
pat = re.compile(pat_str, re.S)
m = pat.search(src)
print("matched:", bool(m))
if m:
    L = []
    def add(x): L.append(x)
    add("            ex_html += " + S + "<h3>" + S + " + html.escape(ex2[" + D + "title" + D + "]) + " + S + "</h3>" + S)
    add("            ex_html += " + S + "<div style=" + D + "display:grid;grid-template-columns:1fr 1fr;gap:10px" + D + ">" + S)
    add("            ex_html += " + S + "<figure style=" + D + "margin:0" + D + ">" + S)
    add("            ex_html += " + S + "<div style=" + D + "background:#1d4d2b;color:#a8e6a3;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">OK PROMPT</div>" + S)
    add("            ex_html += " + S + "<img src=" + D + " + base + s2 + " + S + "-good.jpg" + S + " loading=" + D + "lazy" + D + " style=" + D + "width:100%;border-radius:0 0 10px 10px" + D + ">" + S)
    add("            ex_html += " + S + "<figcaption style=" + D + "font-size:.75rem;color:#a8e6a3;line-height:1.7;margin-top:.35rem" + D + ">" + S + " + html.escape(ex2[" + D + "good_cap" + D + "]) + " + S + "</figcaption>" + S)
    add("            ex_html += " + S + "</figure>" + S)
    add("            ex_html += " + S + "<figure style=" + D + "margin:0" + D + ">" + S)
    add("            ex_html += " + S + "<div style=" + D + "background:#4d1d1d;color:#e6a8a8;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">WEAK</div>" + S)
    add("            ex_html += " + S + "<img src=" + D + " + base + s2 + " + S + "-bad.jpg" + S + " loading=" + D + "lazy" + D + " style=" + D + "width:100%;border-radius:0 0 10px 10px;opacity:.85" + D + ">" + S)
    add("            ex_html += " + S + "<figcaption style=" + D + "font-size:.75rem;color:#cbb8d4;line-height:1.7;margin-top:.35rem" + D + ">" + S + " + html.escape(ex2[" + D + "bad_cap" + D + "]) + " + S + "</figcaption>" + S)
    add("            ex_html += " + S + "</figure>" + S)
    add("            ex_html += " + S + "</div>" + S)
    src = src[:m.start()] + NL.join(L) + src[m.end():]
    P.write_text(src, encoding="utf-8")
    print("replaced")
