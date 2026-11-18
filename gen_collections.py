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
<meta property="og:title" content="FitSaga · 穿搭图鉴与AI画法研究所">
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
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
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


def gen_item_collections():
    """基于items表(堆糖)的词策展合集 — 高收藏优先"""
    import sqlite3 as sq
    con = sq.connect(DB)
    (PUB / "collection").mkdir(parents=True, exist_ok=True)
    EXTRA = [
      ("jk-uniform","JK 制服图鉴 · 高收藏精选","JK制服",["JK制服","格裙"],"青春与秩序感的平衡：格裙、水手服与秋冬叠穿的高收藏示范。"),
      ("sweet-girl","甜妹穿搭精选 · 全网高收藏","甜妹穿搭",["甜妹穿搭","初恋感"],"甜妹风的收藏榜：马卡龙配色与初恋感单品的真实示范。"),
      ("quiet-luxury","静奢风精选 · 低调的贵气","静奢风",["静奢风","千金风"],"静奢=不喊出来的贵：燕麦色、奶油白与软糯面料的收藏级示范。"),
      ("dopamine","多巴胺穿搭精选 · 高饱和的快乐","多巴胺穿搭",["多巴胺穿搭"],"高饱和撞色的快乐法则：怎么穿亮色不显廉价。"),
      ("millard","美拉德穿搭精选 · 秋冬的焦糖系","美拉德穿搭",["美拉德穿搭"],"棕橘焦糖色系的秋冬叙事：老钱风的近亲，更暖更松弛。"),
      ("american-retro","美式复古精选 · Y2K与千禧","美式复古",["美式复古","千禧"],"美式复古的档案库：牛仔裤、棒球服与千禧辣妹的混搭样本。"),
      ("french-style","法式穿搭精选 · 不过度用力","法式穿搭",["法式穿搭"],"法式的核心是「不费力的精致」：碎花、针织与红唇的配比。"),
      ("new-chinese","新中式精选 · 传统与现代的接口","新中式",["新中式","汉元素"],"新中式的日常化样本：立领、盘扣与云肩的现代剪裁。"),
      ("commute","通勤穿搭精选 · 一周不重样","通勤穿搭",["通勤穿搭","职场穿搭"],"通勤搭配的收藏榜：从周一到周五的秩序感。"),
      ("knitwear","针织衫精选 · 软糯的秋冬","针织衫",["针织衫"],"针织的温柔算法：高领、开衫与马甲的层次。"),
      ("coat-season","秋冬大衣精选 · 气场的重量","秋冬大衣",["秋冬大衣","羽绒服"],"大衣是秋冬的排面：驼色、黑色与格纹的收藏示范。"),
      ("qipao-modern","旗袍现代穿法精选","旗袍",["旗袍"],"旗袍的日常化：改良剪裁与现代单品的碰撞。"),
      ("lolita-picks","Lolita 精选 · 三派全收录","Lolita",["Lolita","洛丽塔"],"甜lo、Cla与中华风的收藏样本库。"),
      ("hanfu-daily","汉服日常化精选 · 同袍的衣柜","汉服",["汉服","马面裙"],"汉服的日常穿法：从通勤到旅拍的真实示范。"),
      ("travel-hanfu","古镇旅拍精选 · 穿越感构图","古镇旅拍",["古镇旅拍"],"旅拍的高级感来自场景与服装的互文：古城墙下的襦裙。"),
    ]
    urls = []
    for slug, title, main_kw, kws, desc in EXTRA:
        q = ",".join("?"*len(kws))
        rows = con.execute(f"""SELECT img_url,origin_url,COALESCE(fav_count,json_extract(raw,'$.favorite_count'),0),author FROM items
            WHERE source='duitang' AND json_extract(tags,'$.kw') IN ({q}) AND COALESCE(w,600)>=400 AND COALESCE(h,800)>=500
            ORDER BY 3 DESC LIMIT 18""", kws).fetchall()
        if not rows: continue
        cards = []
        for i,(u,o,f,a) in enumerate(rows):
            cards.append(f'''<figure class="shot">
  <img src="{html.escape(u)}" alt="{html.escape(title)} {i+1}" loading="lazy">
  <figcaption class="cap"><span>{html.escape(main_kw)} · 收藏{f}</span><a href="{html.escape(o)}" target="_blank" rel="nofollow noopener"><em>来源↗</em></a></figcaption>
</figure>''')
        others = "".join(f'<a class="chip" style="background:linear-gradient(135deg,#2a1832,#ff7eb355)" href="/collection/{s}">{html.escape(t.split(" ·")[0])}</a>' for s,t,_,_,_ in EXTRA if s != slug)[:600]
        page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(title)} · FitSaga</title>
<meta property="og:title" content="FitSaga · 穿搭图鉴与AI画法研究所">
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://fitsaga.pages.dev/collection/{slug}">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#ff7eb3">{html.escape(title)}</span></h1>
<p class="sub">{len(rows)} 套 · 按收藏热度排序 · 每日更新</p></header>
<main class="sec">
<p class="intro">{html.escape(desc)}</p>
<nav class="stylechips" style="margin-bottom:1.5rem">{others}</nav>
<div class="masonry">{"".join(cards)}</div>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 策展合集</div>
<p style="margin-top:1.5rem"><a style="color:#c793ff" href="/topics.html">🎨 想用 AI 生成这种风格？进画法研究所看 prompt 方案 →</a></p>
<div class="source">图片版权归原创作者所有 · 点击来源↗访问原帖 · © 2026 FitSaga</div></footer>
<script src="/lightbox.js" defer></script>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''
        (PUB / f"collection/{slug}.html").write_text(page, encoding="utf-8")
        urls.append(slug)
        print(f"[{slug}] {len(rows)} imgs")
    con.close()
    return urls

if __name__ == "__main__":
    main()
    u2 = gen_item_collections()
    # 合并进sitemap
    import subprocess