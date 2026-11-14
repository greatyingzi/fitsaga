#!/usr/bin/env python3
"""生成 /nikki/s/<slug> 套装详情页 + 扩充sitemap"""
import sqlite3, pathlib, html, re

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

def slugify(name):
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", name.strip())
    return s.strip("-") or "suit"

def main(cap=300):
    con = sqlite3.connect(DB)
    (PUB / "nikki" / "s").mkdir(parents=True, exist_ok=True)
    rows = con.execute("""
        SELECT s.id,s.name,s.game,COUNT(si.id) FROM suits s
        JOIN suit_imgs si ON si.suit_id=s.id
        GROUP BY s.id HAVING COUNT(si.id)>0 ORDER BY s.id LIMIT ?""", (cap,)).fetchall()
    urls = []
    made = 0
    for sid, name, game, n in rows:
        slug = slugify(name)
        imgs = con.execute("SELECT img_url,kind FROM suit_imgs WHERE suit_id=? ORDER BY id", (sid,)).fetchall()
        cards = "\n".join(
            f'<figure class="shot"><img src="{html.escape(u)}" alt="{html.escape(game+name+kind)}" loading="lazy"><figcaption class="cap">{html.escape(kind)}</figcaption></figure>'
            for u, kind in imgs)
        # 同风格相关: 同游戏其他套装随机4个
        rel = con.execute("SELECT id,name FROM suits WHERE game=? AND id<>? AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) ORDER BY RANDOM() LIMIT 4", (game, sid)).fetchall()
        rel_html = "\n".join(
            f'<a class="chip" href="/nikki/s/{slugify(rn)}">{html.escape(rn)}</a>' for _, rn in rel)
        page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(name)} · {html.escape(game)}套装图鉴 · FitSaga</title>
<meta name="description" content="{html.escape(name)}({html.escape(game)})套装图鉴：{n}张展示图/部件图/海报，来源BWIKI，点击查看。">
<link rel="canonical" href="https://fitsaga.pages.dev/nikki/s/{slug}">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#f5c76e">{html.escape(name)}</span></h1>
<p class="sub">{html.escape(game)} · {n} 张图 · 数据来自 BWIKI</p></header>
<main class="sec">
<div class="masonry">{cards}</div>
<p style="margin-top:1.5rem;color:#9d8fa8;font-size:.85rem">相关套装：</p>
<nav class="stylechips" style="margin-top:.4rem">{rel_html}</nav>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 游戏时装图鉴</div>
<div class="source">游戏素材版权归 {("叠纸网络" if "暖暖" in game else "官方")} 所有 · 数据整理自 BWIKI(biligame) · <a style="color:#9d8fa8" href="/nikki/infinity">返回图鉴索引</a> · © 2026 FitSaga</div></footer>
</body></html>'''
        (PUB / f"nikki/s/{slug}.html").write_text(page, encoding="utf-8")
        urls.append(f"/nikki/s/{slug}")
        made += 1
    # sitemap 扩容
    today = __import__("datetime").date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          f"<url><loc>https://fitsaga.pages.dev/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>"]
    for k in ["hanfu","qipao","sweet","sexy","jk","street","winter","beauty","korean"]:
        sm.append(f"<url><loc>https://fitsaga.pages.dev/style/{k}.html</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>")
    for f in ["infinity","shining","miracle"]:
        sm.append(f"<url><loc>https://fitsaga.pages.dev/nikki/{f}.html</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>")
    for u in urls:
        sm.append(f"<url><loc>https://fitsaga.pages.dev{u}</loc><lastmod>{today}</lastmod><priority>0.6</priority></url>")
    sm.append("</urlset>")
    (PUB / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    print(f"detail pages: {made}, sitemap urls: {len(sm)-2}")

if __name__ == "__main__":
    main()
