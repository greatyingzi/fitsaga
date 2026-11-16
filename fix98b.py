#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
S = chr(39); D = chr(34)
# 定位98行('</article></div>'行), 重写98-103(6行: article闭合+3script+body闭合+空行保留结构)
start = None
for i, l in enumerate(lines):
    if "</article></div>" in l and "lightbox" not in l:
        start = i
        break
print("article line:", start)
assert start is not None
block = [
    "                 " + S + "</article></div>" + S + ",",
    "                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ",",
    "                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ",",
    "                 " + S + "<script src=" + D + "/theme.js" + D + " defer></script>" + S + ",",
    "                 " + S + "</body></html>" + S + "]",
]
lines[start:start+6] = block
P.write_text(chr(10).join(lines), encoding="utf-8")
print("98-103 rewritten")
