#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
lines[93] = '                 "</article></div>",'
lines[94] = "                 '<script src="/lightbox.js" defer></script>', '<script src="/search.js" defer></script>', "</body></html>"]"
P.write_text(chr(10).join(lines), encoding="utf-8")
print("94-95 rewritten")
