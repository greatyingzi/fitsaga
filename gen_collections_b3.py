#!/usr/bin/env python3
"""gen_collections_b3.py - 合集第三批"""
import sqlite3, pathlib, html

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

B3 = [
  {"slug":"nail-art","title":"美甲精选 · 指尖的风格宣言","kws":["美甲"],"desc":"美甲是穿搭的最后一环——高收藏的款式与配色示范。"},
  {"slug":"first-love","title":"初恋感精选 · 清透的少年气","kws":["初恋感","甜妹穿搭"],"desc":"初恋感的配方：清透底妆、柔和配色、不刻意的松弛。"},
  {"slug":"milk-style","title":"奶系穿搭精选 · 软糯的温柔","kws":["奶系穿搭"],"desc":"奶系的色彩公式：燕麦、奶油、雾蓝的低饱和温柔。"},
  {"slug":"heiress","title":"千金风精选 · 甜而不腻的贵气","kws":["千金风"],"desc":"千金风的边界感：小香风、珍珠与蝴蝶结的分寸。"},
  {"slug":"baddie","title":"御姐风精选 · 大女主气场","kws":["御姐风穿搭","辣妹穿搭"],"desc":"御姐风的剪裁语言：垫肩、深V与高跟的权力感。"},
  {"slug":"office","title":"职场穿搭精选 · 通勤进阶","kws":["职场穿搭","韩系通勤"],"desc":"职场穿搭的层次课：西装、衬衫与半裙的轮换。"},
  {"slug":"travel-outfit","title":"出游穿搭精选 · 上镜的松弛","kws":["出游穿搭","古镇旅拍"],"desc":"出游穿搭配色随场景走：古镇、海边与草原的实拍示范。"},
  {"slug":"korean-style","title":"韩系穿搭精选 · 首尔街拍感","kws":["韩系穿搭"],"desc":"韩系的层次感：短上衣、阔腿裤与低跟短靴。"},
  {"slug":"qipao","title":"旗袍精选 · 一件写尽东方","kws":["旗袍","新中式"],"desc":"旗袍的当代演绎：改良剪裁与新材质的高收藏示范。"},
  {"slug":"mamian","title":"马面裙精选 · 明制日常化","kws":["马面裙","汉服日常"],"desc":"马面裙穿搭的日常解法：织金、混搭与通勤化。"},
]

def main():
    con = sqlite3.connect(DB)
    (PUB / "collection").mkdir(parents=True, exist_ok=True)
    for c in B3:
        q = ",".join("?" * len(c["kws"]))
        rows = con.execute(f"""SELECT img_url, origin_url,
            COALESCE(fav_count, json_extract(raw,'$.favorite_count'),0), author FROM items
            WHERE source IN ('duitang','lofter') AND json_extract(tags,'$.kw') IN ({q})
            AND (COALESCE(w,600)>=400 AND COALESCE(h,800)>=500 OR source='lofter')
            ORDER BY 3 DESC LIMIT 18""", c["kws"]).fetchall()
        if not rows:
            print(f"[{c['slug']}] no imgs"); continue
        cards = []
        for i, (u, o, f, a) in enumerate(rows):
            cards.append(
                '<figure class="shot"><img src="' + html.escape(u) + '" alt="' +
                html.escape(c["title"]) + " " + str(i+1) + '" loading="lazy">' +
                '<figcaption class="cap"><span>' + html.escape(c["kws"][0]) + " · 收藏" + str(f) +
                '</span><a href="' + html.escape(o) + '" target="_blank" rel="nofollow noopener"><em>来源↗</em></a></figcaption></figure>')
        others = "".join(
            '<a class="chip" style="background:linear-gradient(135deg,#2a1832,#ff7eb355)" href="/collection/' +
            o["slug"] + '">' + html.escape(o["title"].split(" ·")[0]) + "</a>"
            for o in B3 if o["slug"] != c["slug"])
        page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(c["title"])} · FitSaga</title>
<meta name="description" content="{html.escape(c["desc"])}">
<link rel="canonical" href="https://fitsaga.pages.dev/collection/{c["slug"]}">
  <meta property="og:title" content="{html.escape(c["title"])} · FitSaga">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#ff7eb3">{html.escape(c["title"])}</span></h1>
<p class="sub">{len(rows)} 套 · 按收藏热度排序 · 每日更新</p></header>
<main class="sec">
<p class="intro">{html.escape(c["desc"])}</p>
<nav class="stylechips" style="margin-bottom:1.5rem">{others}</nav>
<div class="masonry">{"".join(cards)}</div>
<p style="margin-top:1.5rem"><a style="color:#c793ff" href="/topics.html">🎨 想用 AI 生成这种风格？进画法研究所 →</a></p>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 策展合集</div>
<div class="source">图片版权归原创作者所有 · 点击来源↗访问原帖 · © 2026 FitSaga</div></footer>
<script src="/lightbox.js" defer></script>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''
        (PUB / f"collection/{c['slug']}.html").write_text(page, encoding="utf-8")
        print(f"[{c['slug']}] {len(rows)} imgs")
    con.close()

if __name__ == "__main__":
    main()
