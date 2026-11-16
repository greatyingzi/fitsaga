#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
out = []
for l in lines:
    # 1) base路径通用化
    if "base = " in l and "en-ex" in l:
        out.append('            base = "/topics/" + t["slug"] + "/"')
        continue
    # 2) 展示升级: ex_html渲染块(73-76行区域)——找到div grid那行开始整体替换4行
    out.append(l)
s = chr(10).join(out)
# 展示升级: 替换 4 行渲染为带标签条+灯箱hover的版本
old_block_start = s.find('ex_html += ' + S + '<div style=')
old_block_end = s.find("ex_html += '</div>'", old_block_start)
assert old_block_start > 0 and old_block_end > old_block_start
new_block = (
    "ex_html += '<h3 style="display:flex;align-items:center;gap:.5rem">' + html.escape(ex2["title"]) + '</h3>'" + chr(10)
    + "            ex_html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'" + chr(10)
    + "            ex_html += ('<figure style="margin:0"><div style="background:#1d4d2b;color:#a8e6a3;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700">✓ " + D + "GOOD PROMPT" + D + "</div><img src="' + base + s2 + '-good.jpg" loading="lazy" style="width:100%;border-radius:0 0 10px 10px;cursor:zoom-in"><figcaption style="font-size:.75rem;color:#a8e6a3;line-height:1.7;margin-top:.35rem">' + html.escape(ex2["good_cap"]) + '</figcaption></figure>')" + chr(10)
    + "            ex_html += ('<figure style="margin:0"><div style="background:#4d1d1d;color:#e6a8a8;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700">✗ " + D + "WEAK" + D + "</div><img src="' + base + s2 + '-bad.jpg" loading="lazy" style="width:100%;border-radius:0 0 10px 10px;opacity:.85;cursor:zoom-in"><figcaption style="font-size:.75rem;color:#cbb8d4;line-height:1.7;margin-top:.35rem">' + html.escape(ex2["bad_cap"]) + '</figcaption></figure>')" + chr(10)
    + "            ex_html += '</div>'"
)
s = s[:old_block_start] + new_block + s[old_block_end + len("ex_html += '</div>'"):]
P.write_text(s, encoding="utf-8")
print("ex render upgraded")
