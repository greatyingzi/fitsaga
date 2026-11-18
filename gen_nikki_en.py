#!/usr/bin/env python3
"""gen_nikki_en.py - /en/nikki-outfits 英文套装总览(807套按主题EN聚类, 分页12主题)"""
import sqlite3, pathlib, html

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PUB = ROOT / "public" / "en"
PUB.mkdir(parents=True, exist_ok=True)
CSS = open(ROOT / "site.css", encoding="utf-8").read()

THEMES = [
  ("Dreamy & Night", ["梦", "夜"], "dreamy-night"),
  ("Floral & Garden", ["花"], "floral"),
  ("Star & Moon", ["星", "月"], "star-moon"),
  ("Snow & Winter", ["雪", "冬"], "snow"),
  ("Ocean & Water", ["海", "水"], "ocean"),
  ("Spring & Fresh", ["春", "樱"], "spring"),
  ("Royal & Elegant", ["王", "冠", "贵"], "royal"),
  ("Sweet & Cute", ["甜", "糖", "果"], "sweet"),
  ("Fantasy & Magic", ["幻", "魔", "精灵"], "fantasy"),
  ("Classic & Retro", ["复", "古"], "retro"),
  ("Wedding & Bridal", ["婚", "嫁", "誓"], "wedding"),
  ("Gothic & Dark", ["暗", "黑", "魅"], "gothic"),
  ("Fire & Passion", ["火", "炎", "焰"], "fire"),
  ("Moonlight & Silver", ["银", "月"], "moonlight"),
  ("Gold & Glory", ["金", "辉"], "gold"),
  ("Butterfly & Wings", ["蝶", "翼", "羽"], "butterfly"),
  ("Music & Stage", ["歌", "舞", "乐", "演"], "music"),
  ("Ancient & Hanfu", ["汉", "唐", "宋", "古装"], "hanfu"),
  ("Punk & Rebel", ["朋克", "叛逆", "摇滚"], "punk"),
  ("Fairy & Elf", ["仙", "精灵", "妖"], "fairy"),
]

def main():
    con = sqlite3.connect(ROOT / "data" / "fitsaga.db")
    cards_all = []
    total = 0
    for tname, kws, slug2 in THEMES:
        q = " OR ".join(["name LIKE ?"] * len(kws))
        rows = con.execute(f"""SELECT s.id, s.name, (SELECT img_url FROM suit_imgs WHERE suit_id=s.id LIMIT 1)
            FROM suits s WHERE s.game='无限暖暖' AND ({q})
            AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=s.id) LIMIT 16""", tuple("%"+k+"%" for k in kws)).fetchall()
        if not rows: continue
        total += len(rows)
        figs = "".join(
            '<figure style="margin:0"><img src="' + html.escape(img) + '" alt="' + html.escape(nm) +
            ' Infinity Nikki outfit" loading="lazy" style="width:100%;border-radius:8px">' +
            '<figcaption style="font-size:.72rem;color:#9d8fa8;margin-top:.25rem">' + html.escape(nm) + '</figcaption></figure>'
            for sid, nm, img in rows if img)
        cards_all.append('<h2 style="color:#c793ff;font-size:1.05rem;margin-top:1.6rem">' + tname +
                         ' <span style="color:#9d8fa8;font-size:.8rem">(' + str(len(rows)) + ' shown)</span></h2>' +
                         '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">' + figs + '</div>')
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>Infinity Nikki Outfits: {total} Suits by Theme · FitSaga</title>
<meta name="description" content="Browse {total}+ Infinity Nikki outfits grouped by theme — dreamy, floral, starlit, snowy, oceanic. Real in-game suit references for AI palette borrowing and fan design.">
<link rel="canonical" href="https://fitsaga.pages.dev/en/nikki-outfits">
<meta property="og:title" content="Infinity Nikki Outfits by Theme · FitSaga">
<meta property="og:description" content="{total} real in-game suits as AI reference — palette-first workflow included.">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#c793ff">Infinity Nikki Outfits</span></h1>
<p class="sub">{total} suits shown · 10 themes · from our 800+ suit database</p></header>
<main class="sec">
<p style="color:#d8c9de;line-height:1.8">Every theme below pulls <b>real in-game suits</b> with images. The workflow: pick a suit → extract its palette → rebuild it as a prompt (see <a style="color:#8ec5ff" href="/en/topics/infinity-nikki-outfit-ideas">the ideas guide</a> and <a style="color:#8ec5ff" href="/en/topics/game-costume-design-ai">the copyright ladder</a>).</p>
{"".join(cards_all)}
<p style="margin-top:1.5rem;color:#c793ff"><b>Other suit galleries:</b> <a href="/nikki/miracle.html">Miracle Nikki</a> · <a href="/nikki/shining.html">Shining Nikki</a> · <a href="/nikki/miraclehd.html">Miracle HD</a> · <a href="/nikki/zara.html">ZARA editorial</a></p>
<p style="margin-top:2rem"><a style="color:#ff7eb3" href="/en/topics.html">← All AI reference topics</a></p>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · AI Reference</div>
<div class="source">Game assets © Papergames, shown as design reference · © 2026 FitSaga</div></footer>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''
    (PUB / "nikki-outfits.html").write_text(page, encoding="utf-8")
    print("en/nikki-outfits:", total, "suits across", len(cards_all), "themes")
    con.close()

if __name__ == "__main__":
    main()
