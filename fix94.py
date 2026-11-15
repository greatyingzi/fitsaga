#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
# 找94行(0-based 93)替换为两行
for i, l in enumerate(lines):
    if "lightbox.js" in l and "search.js" in l and l.strip().endswith('"'):
        lines[i] = '                 "</article></div>",'
        lines.insert(i+1, "                 " + chr(39) + "<script src=" + chr(34) + "/lightbox.js" + chr(34) + " defer></script>" + chr(39) + ",")
        lines.insert(i+2, "                 " + chr(39) + "<script src=" + chr(34) + "/search.js" + chr(34) + " defer></script>" + chr(39) + ",")
        lines.insert(i+3, '                 "</body></html>"]')
        print("fixed at", i+1)
        break
# 删除原95行残留(含"</body></html>]"的旧行)
for i, l in enumerate(lines):
    if "search.js" in l and "body></html>" in l and i > 95:
        lines[i] = ""
        break
P.write_text(chr(10).join(lines), encoding="utf-8")
print("done")
