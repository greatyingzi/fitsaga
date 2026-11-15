#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39); B = chr(92)
# 0-based: 97=98行, 98=99行, 99=100行
lines[97] = "                 " + S + "</article></div>" + S + ","
lines[98] = "                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ","
lines[99] = "                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ","
# 在99后插theme行(把100行的悬挂内容整个替换)
lines[99+1] = "                 " + S + "<script src=" + D + "/theme.js" + D + " defer></script>" + S + ","
lines[99+2] = "                 " + S + "</body></html>" + S + "]"
P.write_text(chr(10).join(lines), encoding="utf-8")
print("lines 98-101 rewritten")
