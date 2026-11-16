#!/usr/bin/env python3
import pathlib
# 1) 首页导航加b2合集(gen_site.py collections区)
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
if "eye-makeup" not in s:
    old = '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/travel-hanfu">古镇旅拍</a>'
    new = old + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/eye-makeup">眼妆教程</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/skincare">护肤</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/pseudo-nude">伪素颜</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#cbb8d466)" href="/collection/old-money">老钱风</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#e8608a66)" href="/collection/y2k">Y2K 千禧</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/petite">小个子</a>' + chr(10) + '    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/pear-shape">梨形身材</a>'
    s = s.replace(old, new, 1)
    P.write_text(s, encoding="utf-8")
    print("nav b2 added")
# 2) Nikki主题网格img加alt(gen_topics.py 110行figure循环)
P2 = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s2 = P2.read_text(encoding="utf-8")
old_fig = 'themes_html += \'<figure style="margin:0"><img src="\' + u2 + \'" loading="lazy\''
# 用行级替换(找含u2的figure行加alt)
lines = s2.split(chr(10))
for i, l in enumerate(lines):
    if "for u2, nm2 in cards2" in l:
        # 下一行是figure拼接行——给它加alt=nm2
        fig_i = i + 1
        fl = lines[fig_i]
        if "alt=" not in fl:
            # 在img src后插 alt部分: 找 "src="' + u2 + '" 后插 ' alt="' + nm2 + '"'
            fl2 = fl.replace("src="' + u2 + '"", "src="' + u2 + '" alt="' + nm2 + '"")
            if fl2 != fl:
                lines[fig_i] = fl2
                print("alt added to fig line", fig_i+1)
            else:
                print("fig line pattern miss:", fl[:60])
        break
P2.write_text(chr(10).join(lines), encoding="utf-8")
