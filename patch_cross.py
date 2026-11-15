#!/usr/bin/env python3
import pathlib
# 1) gen_nikki_detail.py: 详情页尾部加"AI画法推荐"块
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_nikki_detail.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39)
old = '<p style="margin-top:1.5rem;color:#9d8fa8;font-size:.85rem">相关套装：</p>'
new = (
    '<div style="margin-top:2rem;background:linear-gradient(135deg,#2a1832,#4a1f45);border-radius:14px;padding:1rem 1.1rem;border-left:3px solid #c793ff">'
    '<b style="color:#c793ff">🎨 AI 画法推荐</b>'
    '<p style="margin:.4rem 0 0;font-size:.85rem;color:#d8c9de;line-height:1.8">想用 AI 画这种风格？看<a style="color:#ff9ec7" href="/topics/hanfu-prompt-guide">汉服形制 prompt 指南</a>与<a style="color:#ff9ec7" href="/topics/nikki-art-reference">游戏时装借色方法论</a>。</p>'
    "</div>" + chr(10)
    + old
)
if old in s and "AI 画法推荐" not in s:
    s = s.replace(old, new, 1)
    P.write_text(s, encoding="utf-8")
    print("detail cross-link added")
else:
    print("detail skip")
# 2) gen_collections.py: 合集尾部加专题入口
P2 = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_collections.py")
s2 = P2.read_text(encoding="utf-8")
old2 = '<div class="source">图片版权归原创作者所有 · 点击来源↗访问原帖 · © 2026 FitSaga</div>'
old2b = '<div class="source">游戏素材版权归叠纸网络所有 · 数据整理自 BWIKI · <a style="color:#9d8fa8" href="/nikki/infinity">全部套装图鉴</a> · © 2026 FitSaga</div>'
crossblock = '<p style="margin-top:1.5rem"><a style="color:#c793ff" href="/topics.html">🎨 想用 AI 生成这种风格？进画法研究所看 prompt 方案 →</a></p>'
if old2 in s2 and "画法研究所" not in s2:
    s2 = s2.replace(old2, crossblock + chr(10) + old2, 1)
    P2.write_text(s2, encoding="utf-8")
    print("collections cross-link added")
else:
    print("collections skip:", old2 in s2, "画法研究所" in s2)
