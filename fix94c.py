#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
out = []
done = False
for l in lines:
    if not done and "lightbox.js" in l and "search.js" in l:
        out.append('                 "</article></div>",')
        out.append("                 '<script src="/lightbox.js" defer></script>',")
        out.append("                 '<script src="/search.js" defer></script>',")
        out.append('                 "</body></html>"]')
        done = True
        continue
    # 跳过残行(以<script search开头的悬挂行)
    if done and l.strip().startswith("<script src=") and "body></html>" in l:
        continue
    out.append(l)
P.write_text(chr(10).join(out), encoding="utf-8")
print("rewritten:", done)
