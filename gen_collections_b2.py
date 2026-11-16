#!/usr/bin/env python3
"""gen_collections_b2.py - 合集第二批10个(自动生成, 模板同gen_collections的item模式)"""
import sqlite3, pathlib, html

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

B2 = [
  {"slug":"eye-makeup","title":"眼妆教程精选 · 收藏最多的画法","kws":["眼妆教程","美甲"],"desc":"眼妆是妆面的风格开关：氛围感眼睑下至、卧蚕画法与配色实操，全网收藏最高的示范。"},
  {"slug":"skincare","title":"护肤精选 · 底妆之前的功课","kws":["护肤","护肤流程"],"desc":"妆面成败七成在底妆，底妆成败七成在护肤——高收藏的护肤流程与思路。"},
  {"slug":"pseudo-nude","title":"伪素颜妆精选 · 只做一半的艺术","kws":["伪素颜","日常妆容"],"desc":"伪素颜的秘密是三处都只做一半：底妆薄、眉形自然、唇色浅。"},
  {"slug":"old-money","title":"老钱风精选 · 不刻意的贵","kws":["老钱风","高级感穿搭"],"desc":"老钱风的配色纪律与材质对话：驼色、米白、深棕的秩序感合集。"},
  {"slug":"minimalist","title":"极简穿搭精选 · 少即是高级","kws":["极简穿搭","高级感穿搭"],"desc":"极简不是没有设计，是每个设计都必要——性冷淡风的高级样本。"},
  {"slug":"y2k","title":"Y2K 千禧辣妹精选 · 回潮正当时","kws":["Y2K穿搭","美式复古"],"desc":"千禧回潮档案：亮面、低腰、蝴蝶与金属色的高收藏混搭。"},
  {"slug":"petite","title":"小个子穿搭精选 · 显高实战","kws":["小个子穿搭"],"desc":"155 气质穿搭的收藏榜：腰线前置、同色延伸与短外套公式。"},
  {"slug":"pear-shape","title":"梨形身材精选 · 裤装与重心","kws":["梨形身材穿搭","微胖穿搭"],"desc":"梨形身材的裤装选择与重心转移——真实身材博主的高收藏示范。"},
  {"slug":"hoodie","title":"卫衣穿搭精选 · 宽松的分寸","kws":["卫衣穿搭","日常穿搭"],"desc":"卫衣的宽松分寸：oversize 上身时下半身怎么收。"},
  {"slug":"dress-styles","title":"连衣裙精选 · 一件解决全身","kws":["连衣裙","裙装搭配"],"desc":"连衣裙图鉴：从衬衫裙到茶歇裙，一件单品的完整叙事。"},
]

def main():
    con = sqlite3.connect(DB)
    (PUB / "collection").mkdir(parents=True, exist_ok=True)
    for c in B2:
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
            for o in B2 if o["slug"] != c["slug"])
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
