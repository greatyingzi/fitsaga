#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
# 按内容特征找: 该行包含 "</article></div>" 且包含 "lightbox"
idx = None
for i, l in enumerate(lines):
    if "</article></div>" in l and "lightbox" in l:
        idx = i
        break
print("found at:", idx)
if idx is not None:
    # 该行+下一行(悬挂search行)一起替换
    lines[idx] = "                 " + S + "</article></div>" + S + ","
    lines.insert(idx+1, "                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ",")
    lines.insert(idx+2, "                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ",")
    lines.insert(idx+3, "                 " + S + "</body></html>" + S + "]")
    # 删除后续悬挂行(如果有): 以<script search开头且含body的
    for j in range(idx+4, min(idx+8, len(lines))):
        if "<script" in lines[j] and "body></html>" in lines[j]:
            lines[j] = ""
    P.write_text(chr(10).join(lines), encoding="utf-8")
    print("rewritten OK")
