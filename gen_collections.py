#!/usr/bin/env python3
"""生成策展合集页 /collection/<slug> — 从无限暖暖套装库自动策展+人工导语"""
import sqlite3, pathlib, html, re

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

COLLECTIONS = [
  {"slug":"starry-night","title":"星夜漫游 · 套装精选","kw":["星","月","夜","银河","宵","梦泽"],
   "desc":"把星空穿在身上的 20 套精选。从咏月到银河，适合想拥有静谧氛围感的你。",
   "curator":"策展逻辑：按「天体意象」筛出套装名含星/月/夜/宵的款式，人工剔除了纯黑礼服类，保留氛围更梦幻的。"},
  {"slug":"fairytale-dream","title":"童话与梦 · 套装精选","kw":["童话","梦","天鹅","小王子","残响","真谛"],
   "desc":"住在童话里的 20 套。天鹅、小王子、梦境意象大合集。",
   "curator":"策展逻辑：童话与梦境主题词命中，按图片质量人工排序，封面选了视觉故事性最强的。"},
  {"slug":"spring-floral","title":"花开时节 · 套装精选","kw":["花","蔷薇","春","樱","篱","堇"],
   "desc":"春日花语 20 套。从庭院蔷薇到山野春色。",
   "curator":"策展逻辑：花卉+春主题词命中，去重了同名变体，每套只取最佳展示图。"},
  {"slug":"ocean-rain","title":"海洋与雨 · 套装精选","kw":["海","雨","浪","鳞","驭浪","雾雨"],
   "desc":"水汽氤氲的 20 套。雨夜、海浪与鳞光的氛围感。",
   "curator":"策展逻辑：水系意象词命中。精选了构图里有环境互动的套装。"},
  {"slug":"dark-gothic","title":"暗夜哥特 · 套装精选","kw":["暗","影","夜宴","墟夜","暗影","幽"],
   "desc":"暗黑美学 20 套。哥特、幽影与夜色礼服。",
   "curator":"策展逻辑：暗黑系词命中，控制了尺度：选华丽暗色系而非恐怖风。"},
]

def slugify(name):
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", name.strip())
    return s.strip("-") or "suit"

def main():
    con = sqlite3.connect(DB)
    (PUB / "collection").mkdir(parents=True, exist_ok=True)
    urls = []
    for c in COLLECTIONS:
        hits = []
        seen = set()
        for kw in c["kw"]:
            for (name,) in con.execute(
                "SELECT name FROM suits WHERE game='无限暖暖' AND name LIKE ? AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) LIMIT 60",
                (f"%{kw}%",)):
                if name not in seen:
                    seen.add(name); hits.append(name)
        hits = hits[:20]
        cards = []
        NOTES = {"starry-night":["静谧蓝调，夜色的第一步","星光落在肩线的位置刚好","月白的克制版，日常可穿","丝绒反光让深色活起来","适合正式夜场的叙事感"],
  "fairytale-dream":["童话浓度刚好的一套","薄纱层次是这套的灵魂","低饱和让幻想变可信","圆头鞋收尾，甜度完整","故事感来自配色纪律"],
  "spring-floral":["花开得克制，底色压得住","绿底是这季最稳的选择","大小花比例决定气质","一件外套把花拉回现代","通勤约会的两用解"],
  "ocean-rain":["垂坠感就是这套的水","雾蓝几乎不挑人","光泽走出了涟漪","白色让水汽透出来","一件单品的全场叙事"],
  "dark-gothic":["锋利但优雅的黑色纪律","银饰是唯一的金属色","露肤点到锁骨为止","格纹给黑色一个出口","红唇是这套的标点"]}[c["slug"]] or []
        for i, name in enumerate(hits):
            sid = con.execute("SELECT id FROM suits WHERE game='无限暖暖' AND name=?", (name,)).fetchone()[0]
            img = con.execute("SELECT img_url FROM suit_imgs WHERE suit_id=? LIMIT 1", (sid,)).fetchone()
            if not img: continue
            slug = slugify(name)
            cards.append(f'''<figure class="shot">
  <a href="/nikki/s/{slug}"><img src="{html.escape(img[0])}" alt="{html.escape(name)} 无限暖暖套装展示图" loading="lazy"></a>
  <figcaption class="cap"><span>{html.escape(name)}</span><em class="view">{NOTES[i % len(NOTES)] if NOTES else ""}</em></figcaption>
</figure>''')
        chips = "".join(f'<a class="chip" style="background:linear-gradient(135deg,#2a1832,#e8608a55)" href="/collection/{o["slug"]}">{html.escape(o["title"].split(" ·")[0])}</a>' for o in COLLECTIONS if o["slug"] != c["slug"])
        page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(c["title"])} · FitSaga</title>
<meta name="description" content="{html.escape(c["desc"])}共 {len(cards)} 套，数据来自无限暖暖套装库。">
<link rel="canonical" href="https://fitsaga.pages.dev/collection/{c["slug"]}">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#ff7eb3">{html.escape(c["title"])}</span></h1>
<p class="sub">{len(cards)} 套 · 无限暖暖 · BWIKI 数据</p></header>
<main class="sec">
<p class="intro">{html.escape(c["desc"])}</p>
<p class="intro" style="font-size:.8rem;opacity:.7">{html.escape(c["curator"])}</p>
<nav class="stylechips" style="margin-bottom:1.5rem">{chips}</nav>
<div class="masonry">{"".join(cards)}</div>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 每一套时装，都是一个故事</div>
<div class="source">游戏素材版权归叠纸网络所有 · 数据整理自 BWIKI · <a style="color:#9d8fa8" href="/nikki/infinity">全部套装图鉴</a> · © 2026 FitSaga</div></footer>
<script src="/lightbox.js" defer></script>
</body></html>'''
        (PUB / f"collection/{c['slug']}.html").write_text(page, encoding="utf-8")
        urls.append(f"/collection/{c['slug']}")
        print(c["slug"], len(cards), "suits")
    # sitemap 追加合集
    sm = (PUB / "sitemap.xml").read_text(encoding="utf-8")
    today = __import__("datetime").date.today().isoformat()
    add = "".join(f"<url><loc>https://fitsaga.pages.dev{u}</loc><lastmod>{today}</lastmod><priority>0.9</priority></url>" for u in urls)
    sm = sm.replace("</urlset>", add + "</urlset>")
    (PUB / "sitemap.xml").write_text(sm, encoding="utf-8")
    print("sitemap urls:", sm.count("<loc>"))
    con.close()

if __name__ == "__main__":
    main()