#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
out = []
for l in lines:
    if "base = " in l and "en-ex" in l:
        out.append("            base = " + S + "/topics/" + S + " + t[" + D + "slug" + D + "] + " + S + "/" + S)
        continue
    out.append(l)
s = chr(10).join(out)
# 展示升级: 定位4行渲染区间整体替换(用行级扫描)
lines = s.split(chr(10))
start = end = None
for i, l in enumerate(lines):
    st = l.strip()
    if st.startswith("ex_html += ") and "<div style=" in st and "grid" in st:
        start = i
    if start is not None and st.startswith("ex_html += ") and "</div>" in st:
        end = i
        break
print("render block lines:", start, end)
assert start is not None and end is not None
gd_hdr = "            ex_html += '<div style=" + D + "background:#1d4d2b;color:#a8e6a3;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">OK PROMPT</div>'"
bd_hdr = "            ex_html += '<div style=" + D + "background:#4d1d1d;color:#e6a8a8;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700" + D + ">WEAK</div>'"
block = [
    "            ex_html += '<h3>' + html.escape(ex2["title"]) + '</h3>'",
    "            ex_html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'",
    "            ex_html += '<figure style="margin:0">'",
    gd_hdr,
    "            ex_html += '<img src="' + base + s2 + '-good.jpg" loading="lazy" style="width:100%;border-radius:0 0 10px 10px">'",
    "            ex_html += '<figcaption style="font-size:.75rem;color:#a8e6a3;line-height:1.7;margin-top:.35rem">' + html.escape(ex2["good_cap"]) + '</figcaption>'",
    "            ex_html += '</figure>'",
    "            ex_html += '<figure style="margin:0">'",
    bd_hdr,
    "            ex_html += '<img src="' + base + s2 + '-bad.jpg" loading="lazy" style="width:100%;border-radius:0 0 10px 10px;opacity:.85">'",
    "            ex_html += '<figcaption style="font-size:.75rem;color:#cbb8d4;line-height:1.7;margin-top:.35rem">' + html.escape(ex2["bad_cap"]) + '</figcaption>'",
    "            ex_html += '</figure>'",
    "            ex_html += '</div>'",
]
lines[start:end+1] = block
P.write_text(chr(10).join(lines), encoding="utf-8")
print("block replaced")
