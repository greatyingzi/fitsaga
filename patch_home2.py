#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
D = chr(34)
Q = chr(39)
anchor = "<section class=" + D + "sec" + D + " id=" + D + "today" + D
print("anchor at:", s.find(anchor))
if s.find(anchor) > 0:
    topic_block = (
        "<section class=" + D + "sec" + D + " id=" + D + "ailab" + D + " style=" + D + "padding-top:2.5rem" + D + ">" + chr(10)
        + "  <div class=" + D + "sec-head" + D + " style=" + D + "color:#c793ff" + D + ">" + chr(10)
        + "    <h2>🎨 AI 画法研究所</h2>" + chr(10)
        + "    <p style=" + D + "color:#d8c9de" + D + ">把游戏、影视、流行文化的美学翻译成可直接复制的 prompt —— 热点追更 + 常青风格库</p>" + chr(10)
        + "  </div>" + chr(10)
        + "  <div class=" + D + "sgrid" + D + " style=" + D + "grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr))" + D + ">{topic_cards}</div>" + chr(10)
        + "  <p style=" + D + "margin-top:1rem" + D + "><a style=" + D + "color:#c793ff" + D + " href=" + D + "/topics.html" + D + ">进入研究所查看全部专题 →</a></p>" + chr(10)
        + "</section>" + chr(10)
        + anchor
    )
    # 换回字面anchor(带引号的原始串)
    raw_anchor = "<section class=" + D + "sec" + D + " id=" + D + "today" + D
    s = s.replace(raw_anchor + " style=" + D + "padding-top:1rem" + D, topic_block + " style=" + D + "padding-top:1rem" + D, 1)
    # hero双口号
    s = s.replace("古风 · 优雅 · 甜美 · 性感 · 青春 · 潮流<br>美妆 · 变美 · 每日灵感",
                  "穿搭图鉴 × AI 画法<br>古风 · 汉服 · 辣妹 · 婚纱 · 游戏时装 · prompt 灵感")
    P.write_text(s, encoding="utf-8")
    print("patched OK")
