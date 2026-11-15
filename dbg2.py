#!/usr/bin/env python3
import pathlib
s = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py").read_text(encoding="utf-8")
old = '        print(("en:" if is_en else "zh:") + t["slug"])'
new = '        print(("en:" if is_en else "zh:") + t["slug"], "| zh_cards:", len(zh_cards))'
assert old in s
s = s.replace(old, new, 1)
pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py").write_text(s, encoding="utf-8")
print("dbg ok")
