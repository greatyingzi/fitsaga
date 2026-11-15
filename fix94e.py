#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
out = []
done = False
for l in lines:
    if not done and "lightbox.js" in l and l.strip().startswith(S) and "defer" in l:
        out.append("                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ",")
        out.append("                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ",")
        done = True
        continue
    out.append(l)
P.write_text(chr(10).join(out), encoding="utf-8")
print("rewritten:", done)
