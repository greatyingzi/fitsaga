#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
old = 'base = "/topics/gta6/"  # images shared across languages'
new = 'base = ("/topics/en-ex/" if t.get("slug") in ("hanfu-prompt-guide",) and t.get("lang")=="en" else "/topics/gta6/") if t.get("examples") else "/topics/gta6/"'
# 简化: 按slug判断
new = 'base = "/topics/en-ex/" if (t.get("lang") == "en" and t.get("slug") == "hanfu-prompt-guide") else "/topics/gta6/"'
assert old in s
s = s.replace(old, new, 1)
P.write_text(s, encoding="utf-8")
print("en-ex path ok")
