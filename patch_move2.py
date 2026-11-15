#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
D = chr(34)
a1 = "<section class=" + D + "sec" + D + " id=" + D + "ailab" + D
a2 = "<section class=" + D + "sec" + D + " id=" + D + "today" + D
s_start = s.find(a1)
s_end = s.find(a2)
print("ailab at", s_start, "| today at", s_end)
assert 0 < s_start < s_end
ailab_block = s[s_start:s_end]
s = s[:s_start] + s[s_end:]
jm = s.find("}.join(secs)")
assert jm > 0
line_end = s.find(chr(10), jm)
s = s[:line_end+1] + ailab_block + s[line_end+1:]
P.write_text(s, encoding="utf-8")
print("moved")
