#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
out = []
D = chr(34); S = chr(39)
in_home = False
done_hero = done_cards = False
for i, l in enumerate(lines):
    # hero 副标改双定位
    if not done_hero and "美妆 · 变美 · 每日灵感" in l:
        out.append('  <p class="sub">穿搭图鉴 × AI 画法 — 每一种美，都值得一场冒险</p>')
        done_hero = True
        continue
    # 在9风格sections输出后、今日精选前插入画法研究所板块
    if not done_cards and "{chr(39)}".join([]) == "never" and False:
        pass
    out.append(l)
# 靠字符串替换处理板块插入(比行级稳)
s = chr(10).join(out)
anchor = "<section class="sec" id="today" style="padding-top:1rem">"
topic_block = (
    '<section class="sec" id="ailab" style="padding-top:2.5rem">' + chr(10)
    + '  <div class="sec-head" style="color:#c793ff">' + chr(10)
    + '    <h2>🎨 AI 画法研究所</h2>' + chr(10)
    + '    <p style="color:#d8c9de">把游戏、影视、流行文化的美学翻译成可直接复制的 prompt —— 热点追更 + 常青风格库</p>' + chr(10)
    + "  </div>" + chr(10)
    + '  <div class="sgrid" style="grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr))">{topic_cards}</div>' + chr(10)
    + '  <p style="margin-top:1rem"><a style="color:#c793ff" href="/topics.html">进入研究所查看全部专题 →</a></p>' + chr(10)
    + "</section>" + chr(10)
    + anchor
)
assert anchor in s
s = s.replace(anchor, topic_block, 1)
# hero双口号
s = s.replace("古风 · 优雅 · 甜美 · 性感 · 青春 · 潮流<br>美妆 · 变美 · 每日灵感",
              "穿搭图鉴 × AI 画法<br>古风 · 汉服 · 辣妹 · 婚纱 · 游戏时装 · prompt 灵感")
P.write_text(s, encoding="utf-8")
print("hero + topic block inserted")
