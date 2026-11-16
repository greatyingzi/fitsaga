#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
# hero第二行4入口chips 加下载中心
old = '<a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/zara.html">ZARA 大片</a>'
if "downloads.html" not in s:
    s = s.replace(old, old + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/downloads.html">⬇ 参考图包</a>', 1)
    P.write_text(s, encoding="utf-8")
    print("nav added")
