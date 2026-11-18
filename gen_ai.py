#!/usr/bin/env python3
"""生成 /ai.html — AI灵感图鉴(civitai, 按tag分组)"""
import sqlite3, pathlib, html, json

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

TAGS = [("fashion","时尚人像"),("hanfu","汉服国风"),("qipao","旗袍东方"),("kimono","和服和风"),
        ("dress","裙装"),("gown","礼服"),("wedding dress","婚纱"),("portrait","人像写真")]

def main():
    con = sqlite3.connect(DB)
    sections = []
    total = 0
    for tag, zh in TAGS:
        rows = con.execute("""SELECT img_url,origin_url,author,w,h FROM items
            WHERE source='civitai' AND json_extract(tags,'$.tag')=? ORDER BY w DESC LIMIT 12""", (tag,)).fetchall()
        if not rows: continue
        total += len(rows)
        cards = "\n".join(
            f'''<figure class="shot">
  <img src="{html.escape(u)}" alt="AI灵感图 · {html.escape(zh)} {i+1}" loading="lazy">
  <figcaption class="cap"><span>AI · {html.escape(zh)}</span><a href="{html.escape(origin)}" target="_blank" rel="nofollow noopener"><em>来源↗</em></a></figcaption>
</figure>''' for i,(u,origin,author,w,h) in enumerate(rows))
        sections.append(f'''
<section class="sec" id="ai-{tag.replace(" ","-")}">
  <div class="sec-head" style="color:#a855f7">
    <h2>{html.escape(zh)} <span class="en" style="font-size:.75rem;opacity:.6">AI·{len(rows)}</span></h2>
    <p style="color:#cbb8d4">AI 生成的{html.escape(zh)}灵感，高分辨率，可作为搭配参考与AI创作底图。</p>
  </div>
  <div class="masonry">{cards}</div>
</section>''')
    con.close()
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>AI 灵感图鉴 · FitSaga</title>
<meta property="og:title" content="FitSaga · 穿搭图鉴与AI画法研究所">
<meta name="description" content="AI 生成的女性穿搭灵感图鉴：汉服、旗袍、婚纱、礼服等人像大片，来自 Civitai 社区，高分辨率可商用参考。">
<link rel="canonical" href="https://fitsaga.pages.dev/ai.html">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#a855f7">AI 灵感图鉴</span></h1>
<p class="sub">{total} 张 · 生成式时尚视觉 · 持续扩充</p></header>
{"".join(sections)}
<footer><div><b style="color:#f5c76e">FitSaga</b> · AI 视觉实验室</div>
  <script src="/search.js" defer></script>
  <script src="/theme.js" defer></script>
<div class="source">图片由社区模型生成，版权归各模型作者所有 · 来源 Civitai · © 2026 FitSaga</div></footer>
<script src="/lightbox.js" defer></script>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''
    (PUB / "ai.html").write_text(page, encoding="utf-8")
    print("ai.html:", total, "imgs")

if __name__ == "__main__":
    main()
