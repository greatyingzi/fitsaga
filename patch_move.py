#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
# ailab section 当前在 today 前; 把它移到 secs 之后第一个位置(风格板块之前)
# 现结构: {"".join(secs)} <section ailab> <section today> <section collections>
# 改为: <section ailab> {"".join(secs)} <section today> <section collections>
ailab_start = s.find("<section class="sec" id="ailab"")
ailab_end = s.find("<section class="sec" id="today"")
assert ailab_start > 0 and ailab_end > ailab_start, (ailab_start, ailab_end)
# 提取ailab块(到today前)
ailab_block = s[ailab_start:ailab_end]
s = s[:ailab_start] + s[ailab_end:]
# 插入到 {"".join(secs)} 之后
join_marker = "{chr(34)}.join(secs)".replace("chr(34)", chr(34))
# 实际源码里是 {"".join(secs)} — 用字符串查找
jm = s.find("}.join(secs)")
assert jm > 0
line_end = s.find(chr(10), jm)
s = s[:line_end+1] + ailab_block + s[line_end+1:]
P.write_text(s, encoding="utf-8")
print("ailab moved to first content block")
