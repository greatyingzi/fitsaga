#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
# 找 hero 内第二行导航(穿搭研究所/AI灵感/画法研究所/ZARA), 把画法研究所提到第一行最前
for i, l in enumerate(lines):
    if "穿搭研究所" in l and "hero" not in l and "chip" in l:
        # 该行是nav块开始, 找画法研究所行
        for j in range(i, min(i+6, len(lines))):
            if "画法研究所" in lines[j]:
                line = lines[j].strip()
                # 插入到风格chips nav前(找 <nav class="stylechips">{chips}</nav> 行)
                for k, m in enumerate(lines):
                    if m.strip() == "<nav class=" + D + "stylechips" + D + ">{chips}</nav>":
                        # 在其前插入画法chip为第一行nav
                        lines[k] = "  <nav class=\"stylechips\">\n    " + line + "\n    {chips}\n  </nav>"
                        print("hero first-line chip inserted")
                        break
                break
        break
P.write_text(chr(10).join(lines), encoding="utf-8")
