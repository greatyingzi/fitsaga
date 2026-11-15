#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
# 找 "</article></div>" 行, 其后三行整体重写
for i, l in enumerate(lines):
    if "</article></div>" in l and "lightbox" in l:
        lines[i] = "                 " + S + "</article></div>" + S + ","
        lines[i+1] = "                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ","
        lines[i+2] = "                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ","
        lines[i+3] = "                 " + S + "<script src=" + D + "/theme.js" + D + " defer></script>" + S + ",",
        lines[i+3] = lines[i+3].rstrip(",")
        lines[i+4] = "                 " + S + "</body></html>" + S + "]"
        print("rewrote 4 lines at", i+1)
        break
P.write_text(chr(10).join(lines), encoding="utf-8")
