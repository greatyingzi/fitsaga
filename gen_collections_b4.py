#!/usr/bin/env python3
"""gen_collections_b4.py - 合集第三批"""
import sqlite3, pathlib, html

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

B3 = [
  {"slug":"makeup-tutorial","title":"化妆教程精选 · 收藏最高的实战画法","kws":["化妆教程","日常妆容"],"desc":"全站收藏最高的词：从底妆到眼妆的完整实战教程，按收藏排序。"},
  {"slug":"makeup-basics","title":"美妆精选 · 日常妆容速成","kws":["美妆","日常妆容"],"desc":"美妆入门到进阶的收藏榜单——日常妆容的高频画法。"},
  {"slug":"elegant","title":"高级感穿搭精选 · 不费力的精致","kws":["高级感穿搭","穿搭分享"],"desc":"高级感不是堆品牌，是配色、材质与合身度的三重纪律。"},
  {"slug":"american-retro-b","title":"美式复古精选 · 丹宁与摇滚","kws":["美式复古","牛仔"],"desc":"美式复古的硬核单品：牛仔、皮衣、乐队Tee的高收藏示范。"},
  {"slug":"daily-wear","title":"日常穿搭精选 · 每天都有得抄","kws":["日常穿搭","穿搭分享"],"desc":"最高频的穿搭需求：通勤、约会、逛街都有解的收藏清单。"},
  {"slug":"winter-coat","title":"秋冬大衣精选 · 一件定调整身","kws":["秋冬大衣","西装穿搭"],"desc":"大衣的版型与配色决定秋冬气质——高收藏大衣图鉴。"},
  {"slug":"japanese-style","title":"日系穿搭精选 · 松弛的层次","kws":["日系穿搭","森系"],"desc":"日系的叠穿哲学：宽松、自然、低饱和的收藏示范。"},
  {"slug":"blazer","title":"西装穿搭精选 · 中性力量感","kws":["西装穿搭","职场穿搭"],"desc":"西装的当代穿法：垫肩、阔腿裤与混搭的高收藏样本。"},
  {"slug":"skirt-outfit","title":"裙装搭配精选 · 一条裙的365天","kws":["裙装搭配","格裙"],"desc":"从百褶到包臀，裙装的四季搭配与风格切换。"},
  {"slug":"french-style-b","title":"法式穿搭精选 · 慵懒的精致","kws":["法式穿搭","穿搭分享"],"desc":"法式的少即是多：条纹、丝巾与合身剪裁的收藏样本。"},
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