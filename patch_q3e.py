#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34)
SCRIPTS = "<script src=" + D + "/lightbox.js" + D + " defer></script><script src=" + D + "/search.js" + D + " defer></script><script src=" + D + "/theme.js" + D + " defer></script>"
n = 0
for i, l in enumerate(lines):
    if l.strip() == D + "</body></html>]" and SCRIPTS not in l:
        lines[i] = l.replace(D + "</body></html>]", SCRIPTS + D + "</body></html>]")
        n += 1
P.write_text(chr(10).join(lines), encoding="utf-8")
print("injected:", n)
