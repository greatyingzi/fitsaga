#!/usr/bin/env python3
"""生成 /zara 官方大片页 — 纯瀑布流展示"""
import sqlite3, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

def main():
    con = sqlite3.connect(DB)
    rows = con.execute("""SELECT si.img_url, s.name FROM suit_imgs si
        JOIN suits s ON s.id=si.suit_id WHERE s.game='ZARA大片' ORDER BY si.id DESC LIMIT 200""").fetchall()
    con.close()
    cards = "\n".join(
        f'<figure class="shot"><img src="{html.escape(u)}" alt="ZARA 女装大片 {i+1}" loading="lazy"><figcaption class="cap"><span>ZARA · 大片 {String(i+1).zfill(2) if False else str(i+1).zfill(2)}</span><em>{html.escape(n)}</em></figcaption></figure>'
        for i, (u, n) in enumerate(rows))
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>ZARA 女装大片图鉴 · FitSaga</title>
<meta name="description" content="ZARA 官方女装新品大片合集：模特穿搭灵感，每周上新。">
<link rel="canonical" href="https://fitsaga.pages.dev/zara.html">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#8ec5ff">ZARA · 女装大片</span></h1>
<p class="sub">{len(rows)} 张官方大片 · 每周上新</p></header>
<main class="sec"><div class="masonry">{cards}</div></main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 品牌大片图鉴</div>
<div class="source">图片版权归 ZARA (Inditex) 所有 · 来源 zara.com 官方新品页 · © 2026 FitSaga</div></footer>
<script src="/lightbox.js" defer></script>
</body></html>'''
    (PUB / "zara.html").write_text(page, encoding="utf-8")
    print("zara.html imgs:", len(rows))

if __name__ == "__main__":
    main()
