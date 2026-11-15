#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34)
a1 = "<section class=" + D + "sec" + D + " id=" + D + "ailab" + D
a2 = "<section class=" + D + "sec" + D + " id=" + D + "today" + D
# 行级定位
i_start = i_end = None
for i, l in enumerate(lines):
    if a1 in l and i_start is None: i_start = i
    if a2 in l and i_end is None and i_start is not None: i_end = i
print("lines:", i_start, i_end)
assert i_start is not None and i_end is not None and i_end > i_start
ailab_lines = lines[i_start:i_end]
rest = lines[:i_start] + lines[i_end:]
# 在 201行 {"".join(secs)} (重算: 删除后位置变化, 按内容找)
for i, l in enumerate(rest):
    if "join(secs)" in l:
        rest[i+1:i+1] = ailab_lines
        print("inserted after line", i+1)
        break
P.write_text(chr(10).join(rest), encoding="utf-8")
