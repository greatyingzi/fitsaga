#!/usr/bin/env python3
import pathlib
s = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py").read_text(encoding="utf-8")
# 找 write_text 行, 在其前插入打印
marker = "(PUB / (sub + "
i = s.find(marker)
dbg_line = '        print("DBG theme in parts:", sum(1 for p_ in parts if "theme" in p_))' + chr(10)
s = s[:i] + dbg_line + s[i:]
pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py").write_text(s, encoding="utf-8")
print("dbg inserted")
