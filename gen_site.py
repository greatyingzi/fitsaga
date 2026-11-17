#!/usr/bin/env python3
"""FitSaga site generator: SQLite -> public/ 静态站
生成: index.html, /style/<key>.html(xN), sitemap.xml, robots.txt
"""
import sqlite3, json, pathlib, html, datetime
from style_content import STYLE_CONTENT
import html as htmlMod

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
BASE = "https://fitsaga.pages.dev"

STYLES = [
  {"key":"hanfu","zh":"古风 · 汉服","kws":["汉服"],"accent":"#b5548c",
   "desc":"广袖流仙裙，一梦入华夏。从齐胸襦裙到马面裙，收集最打动人的国风搭配。",
   "intro":"汉服穿搭的灵感库。这里的每一张图都来自真实同袍的日常与旅拍：形制、配色、场合搭配各有讲究。点开任意一张可以跳回原始分享页，向原作者致意。"},
  {"key":"qipao","zh":"旗袍 · 优雅","kws":["旗袍"],"accent":"#c23a52",
   "desc":"东方美的极致剪裁。",
   "intro":"旗袍的现代穿法集合。改良剪裁、日常化搭配、新娘敬酒服——优雅从来不只一种样子。"},
  {"key":"sweet","zh":"甜美 · 少女","kws":["甜美穿搭"],"accent":"#e0609e",
   "desc":"马卡龙色的心动日常。",
   "intro":"甜妹风格图鉴：奶系配色、初恋感单品、约会look。适合想要柔软氛围感的你。"},
  {"key":"sexy","zh":"辣妹 · 性感","kws":["御姐风穿搭"],"accent":"#e0475f",
   "desc":"自信张扬，锋芒万丈。",
   "intro":"御姐与辣妹风的边界示范：气场拉满但不擦边。吊带、包臀、纯欲氛围感的正确打开方式。"},
  {"key":"jk","zh":"JK · 制服","kws":["JK制服"],"accent":"#3f6fd8",
   "desc":"青春感拉满的学院风。",
   "intro":"JK制服图鉴：格裙、水手服、西式制服与秋冬叠穿。青春是最好的滤镜。"},
  {"key":"street","zh":"街头 · 潮流","kws":["街拍"],"accent":"#0ea5a5",
   "desc":"都市酷感，随性出街。",
   "intro":"真实街拍流：城市里被镜头捕捉的普通人穿搭，比杂志更接近明天你能穿上的样子。"},
  {"key":"winter","zh":"秋冬 · 叠穿","kws":["秋冬穿搭"],"accent":"#8a6d3b",
   "desc":"降温天的高级感解法。",
   "intro":"秋冬叠穿专题：大衣、围巾、层次感配色。保暖与风度在这页和平共处。"},
  {"key":"beauty","zh":"美妆 · 变美","kws":["美妆"],"accent":"#a855f7",
   "desc":"妆容灵感与技巧参考。",
   "intro":"美妆灵感墙：日常妆、纯欲妆、氛围感眼妆。每一张都来自真实博主的化妆台。"},
  {"key":"korean","zh":"韩系 · 街拍","kws":[],"musinsa":True,"accent":"#3b82f6",
   "desc":"首尔街头的心动瞬间。",
   "intro":"来自 Musinsa 스냅 的韩国真实街拍：年轻、利落、氛围感十足。图片来源与作者信息逐张标注。"},
]

def esc(s): return html.escape(str(s or ""))

def fetch_items(kws=None, musinsa=False, limit=60):
    con = sqlite3.connect(DB)
    if musinsa:
        rows = con.execute("SELECT img_url,origin_url,author,license,w,h,raw FROM items WHERE source='musinsa' ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        items = []
        for img,origin,author,lic,w,h,raw in rows:
            # musinsa CDN 支持缩放参数; user字段是数字ID, 展示用通用署名
            u = img + "?w=700" if "image.msscdn.net" in img else img
            items.append({"img":u,"origin":origin,"author":"스냅创作者","src":"Musinsa","w":w,"h":h})
        return items
    q = ",".join("?"*len(kws))
    # 质量分层: 分辨率过滤(竖图≥400x600) + 按收藏数排序 + 时间近者优先
    rows = con.execute(f"""SELECT img_url,origin_url,author,license,w,h,tags,source FROM items
        WHERE source IN ('duitang','lofter') AND json_extract(tags,'$.kw') IN ({q})
          AND (COALESCE(w,600)>=400 AND COALESCE(h,800)>=500 OR source='lofter')
        ORDER BY (COALESCE(json_extract(raw,'$.favorite_count'),0) + CASE WHEN source='lofter' THEN 150 ELSE 0 END) DESC, id DESC
        LIMIT ?""", (*kws, limit * 3)).fetchall()
    items = []
    from collections import defaultdict
    per_kw = defaultdict(int)
    cap = max(6, limit // max(1, len(kws)))
    for img,origin,author,lic,w,h,tags,source_col in rows:
        kw = json.loads(tags).get("kw") if tags else ""
        if per_kw[kw] >= cap: continue
        per_kw[kw] += 1
        sid = json.loads(tags).get("sender_id") if tags else None
        items.append({"img":img,"origin":origin,"author":author or (f"创作者{sid}" if sid else None),"src":("Lofter" if source_col=="lofter" else "堆糖"),"w":w,"h":h,"kw":kw})
    con.close()
    return items

def card(it, i, style):
    alt = f"{style}搭配灵感图{i+1} · 来自{it.get('src','')}"
    dims = f'width="{it["w"]}" height="{it["h"]}"' if it.get("w") else ""
    author = esc(it.get("author") or "佚名创作者")
    src_link = f'<a class="src-link" href="{esc(it["origin"])}" target="_blank" rel="nofollow noopener">来源↗</a>' if it.get("origin") else ""
    return f'''<figure class="shot">
  <img src="{esc(it["img"])}" alt="{esc(alt)}" {dims} loading="lazy">
  {src_link}
  <figcaption class="cap"><span>{esc(style)}</span><em>© {author} · {esc(it.get("src",""))}</em></figcaption>
</figure>'''

CSS = open(ROOT/"site.css", encoding="utf-8").read() if (ROOT/"site.css").exists() else ""

GSC_META = ""  # 主人在 GSC 选「HTML 标记」法后, 把整段 meta 贴到这里, 形如: <meta name="google-site-verification" content="token">
OG_TAGS = '<meta property="og:title" content="FitSaga · 每一种美，都值得一场时装冒险"><meta property="og:description" content="古风汉服、旗袍、甜美、辣妹、JK、街拍——真实搭配灵感与AI画法专题"><meta property="og:type" content="website"><meta property="og:url" content="https://fitsaga.pages.dev/"><meta name="twitter:card" content="summary"'

def page(title, desc, body, accent, path="/"):
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
{OG_TAGS}{GSC_META}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{esc(path)}">
<style>{CSS}</style>
</head>
<body>
{body}
<script src="/lightbox.js" defer></script>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body>
</html>'''

def nav_html(active):
    chips = "".join(
        f'<a class="chip{" on" if s["key"]==active else ""}" style="background:linear-gradient(135deg,#2a1832,{s["accent"]}66)" href="/style/{s["key"]}.html">{s["zh"]}</a>'
        for s in STYLES)
    return f'<nav class="stylechips">{chips}</nav>'

def style_page(s):
    items = fetch_items(s.get("kws"), s.get("musinsa"))
    cards = "\n".join(card(it,i,s["zh"].split(" · ")[0]) for i,it in enumerate(items))
    sc = STYLE_CONTENT.get(s["key"], {})
    deep_html = f'<p class="intro">{esc(sc["deep"])}</p>' if sc.get("deep") else f'<p class="intro">{esc(s["intro"])}</p>'
    ld = ""
    if items:
        ld = f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"ItemList","name":s["zh"],"itemListElement":[{"@type":"ImageObject","contentUrl":it["img"],"name":f"{s[chr(122)+chr(104)]}搭配灵感{i+1}","url":it["origin"]} for i,it in enumerate(items[:20])]}, ensure_ascii=False)}</script>'
    faq_html = ""
    if sc.get("faq"):
        faq_items = "".join(
            f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in sc["faq"])
        faq_html = f'<div class="sec-head" style="color:{s["accent"]}"><h2>常见问题</h2></div><div class="faq">{faq_items}</div>'
    body = f'''
<header class="hero small" style="background:radial-gradient(900px 400px at 70% 10%,{s["accent"]}33,transparent 60%),#141018">
  <h1><span style="color:{s["accent"]}">{s["zh"]}</span></h1>
  <p class="sub">{esc(s["desc"])}</p>
</header>
<main class="sec">
  {deep_html}
  {ld}'
  {nav_html(s["key"])}
  <div class="masonry">{cards}</div>
  {faq_html}
  <p style="margin-top:1.5rem"><a style="color:#c793ff" href="/topics/hanfu-prompt-guide">🎨 想用 AI 生成这种风格？看画法研究所的 prompt 方案 →</a></p>
</main>
<footer>
  <div><b style="color:#f5c76e">FitSaga</b> · 每一套时装，都是一个故事</div>
  <div class="source">图片版权归原创作者所有，点击图片可访问原始分享页 · 侵权请联系删除 · © 2026 FitSaga</div>
</footer>'''
    return page(f"{s['zh']}搭配图鉴 · FitSaga", f"{s['zh']}穿搭灵感图鉴：{s['desc']}海量真实搭配图片，逐张标注来源与作者。", body, s["accent"], f"/style/{s['key']}.html")

def today_cards_html(limit=14):
    con = sqlite3.connect(DB)
    rows = con.execute("""SELECT img_url,origin_url,author,license,w,h,tags FROM items
        WHERE source='duitang' AND (COALESCE(w,600)>=400 AND COALESCE(h,800)>=500 OR source='lofter')
        ORDER BY COALESCE(json_extract(raw,'$.favorite_count'),0) DESC, id DESC LIMIT ?""", (limit,)).fetchall()
    con.close()
    cards = []
    for i, (img, origin, author, lic, w, h, tags) in enumerate(rows):
        kw = json.loads(tags).get("kw", "") if tags else ""
        cards.append(f'<figure class="shot"><img src="{htmlMod.escape(img)}" alt="{kw or "精选"}搭配灵感{i+1} · FitSaga今日精选" loading="lazy"><figcaption class="cap"><span>{htmlMod.escape(kw or "精选")}</span><em>查看 ↗</em></figcaption></figure>')
    return "\n".join(cards)

def topic_cards_html():
    import json as _json
    cards = []
    for f in sorted((ROOT / "collector").glob("_topic_*.json")):
        t = _json.loads(f.read_text(encoding="utf-8"))
        if t.get("lang") == "en": continue
        sub = "en/topics" if t.get("lang") == "en" else "topics"
        emoji = "🔥" if t.get("type") == "hot" else ("🧠" if t.get("type") == "deep" else "📚")
        cards.append("<a class='scard' style='padding:1rem;display:block' href=/" + sub + "/" + t["slug"] + "'><div class='sname'>" + emoji + " " + htmlMod.escape(t["title"]) + "</div><div class='smeta' style='margin-top:.4rem;line-height:1.7'>" + htmlMod.escape(t["lede"][:60]) + "…</div></a>")
    cards.sort(key=lambda c: 0 if "🔥" in c else (1 if "🧠" in c else 2))
    return chr(10).join(cards)

def home():
    topic_cards = topic_cards_html()
    today_cards = today_cards_html()
    style_rows = []
    for s in STYLES:
        items = fetch_items(s.get("kws"), s.get("musinsa"), limit=4)
        mini_parts = []
        for it in items:
            mini_parts.append('<a class="mini" href="/style/' + s["key"] + '.html"><img src="' + esc(it["img"]) + '" loading="lazy"></a>')
        mini = chr(10).join(mini_parts)
        style_rows.append(
            '<div class="srow">' +
            '<div class="srow-h" style="color:' + s["accent"] + '"><b>' + esc(s["zh"]) + '</b><a href="/style/' + s["key"] + '.html" class="more">全部 →</a></div>' +
            '<div class="minirow">' + mini + '</div></div>')
    chips = ''.join('<a class="chip" style="background:linear-gradient(135deg,#2a1832,' + s["accent"] + '66)" href="/style/' + s["key"] + '.html">' + s["zh"] + '</a>' for s in STYLES)
    body = f'''
<section class="hero hero2">
  <h1>真实穿搭图鉴 <span style="color:#c793ff">×</span> AI 画法研究所</h1>
  <p class="sub">每一种美，都值得一场时装冒险 —— 图鉴用来找灵感，画法用来做创作</p>
  <nav class="stylechips">
    <a class="chip chip-hero" style="background:linear-gradient(135deg,#3a2a44,#c793ff)" href="/topics.html">🎨 AI 画法研究所</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/guide.html">📖 穿搭研究所</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/ai.html">✦ AI 灵感图鉴</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/zara.html">ZARA 大片</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/downloads.html">⬇ 参考图包</a>
  </nav>
</section>
<section class="sec" id="ailab" style="padding-top:1.5rem">
  <div class="sec-head" style="color:#c793ff">
    <h2>🎨 AI 画法研究所</h2>
    <p style="color:#d8c9de">把游戏、影视、流行文化的美学翻译成可直接复制的 prompt —— 热点追更 + 常青风格库</p>
  </div>
  <div class="tgrid">{topic_cards}</div>
</section>
<section class="sec" id="today" style="padding-top:1rem">
  <div class="sec-head" style="color:#ffd9a8">
    <h2>今日精选 🔥</h2>
    <p style="color:#d8c9de">全网收藏最多的搭配灵感，每天更新 ——</p>
  </div>
  <div class="masonry">{today_cards}</div>
</section>
<section class="sec" id="styles-quick">
  <div class="sec-head" style="color:#ff7eb3">
    <h2>风格图鉴速览</h2>
    <p style="color:#d8c9de">九种风格 · 每种都有完整图鉴页 ——</p>
  </div>
  " + chr(10).join(style_rows) + "
</section>
<section class="sec" id="collections">
  <div class="sec-head" style="color:#ff7eb3">
    <h2>策展合集</h2>
    <p style="color:#d8c9de">有人替你选好、排好、讲好的主题特辑 ——</p>
  </div>
  <nav class="stylechips" style="margin-top:.5rem;justify-content:flex-start">
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#e8608a66)" href="/collection/starry-night">星夜漫游</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#3f6fd866)" href="/collection/jk-uniform">JK 制服</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#cbb8d466)" href="/collection/quiet-luxury">静奢风</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#e0475f66)" href="/collection/dopamine">多巴胺</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#0ea5a566)" href="/collection/new-chinese">新中式</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#b5548c66)" href="/collection/hanfu-daily">汉服日常</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/travel-hanfu">古镇旅拍</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/eye-makeup">眼妆教程</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/skincare">护肤</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/pseudo-nude">伪素颜</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#cbb8d466)" href="/collection/old-money">老钱风</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#e8608a66)" href="/collection/y2k">Y2K 千禧</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/petite">小个子</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/pear-shape">梨形身材</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/nail-art">美甲</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/first-love">初恋感</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ff7eb366)" href="/collection/heiress">千金风</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#e8608a66)" href="/collection/baddie">御姐风</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/office">职场通勤</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#cbb8d466)" href="/collection/qipao">旗袍</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/mamian">马面裙</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ff7eb366)" href="/collection/makeup-tutorial">化妆教程</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#8ec5ff66)" href="/collection/daily-wear">日常穿搭</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#ffd9a866)" href="/collection/winter-coat">秋冬大衣</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#cbb8d466)" href="/collection/blazer">西装穿搭</a>
    <a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/japanese-style">日系穿搭</a>
  </nav>
</section>
<footer>
  <div><b style="color:#f5c76e">FitSaga</b> · 每一套时装，都是一个故事</div>
  <div class="links"><a href="/style/hanfu.html">风格图鉴</a><a href="/guide.html">穿搭研究所</a><a href="/topics.html">画法研究所</a><a href="/ai.html">AI 灵感</a><a href="/zara.html">ZARA</a></div>
  <div class="source">图片版权归原创作者所有，点击图片访问原始分享页 · © 2026 FitSaga</div>
</footer>'''
    return page("FitSaga · 真实穿搭图鉴 × AI 画法研究所", "FitSaga：真实穿搭灵感图鉴与 AI 画法专题——把每一种美变成可复制的灵感与 prompt。", body, "#e8608a")

def sitemap():
    today = datetime.date.today().isoformat()
    urls = [(f"{BASE}/", "1.0")]
    for s in STYLES:
        urls.append((f"{BASE}/style/{s['key']}.html", "0.8"))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u,p in urls:
        xml.append(f"<url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>")
    xml.append("</urlset>")
    return "\n".join(xml)

def main():
    (PUB/"style").mkdir(parents=True, exist_ok=True)
    (PUB/"index.html").write_text(home(), encoding="utf-8")
    for s in STYLES:
        (PUB/f"style/{s['key']}.html").write_text(style_page(s), encoding="utf-8")
    (PUB/"sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (PUB/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://fitsaga.pages.dev/sitemap.xml\n", encoding="utf-8")
    print("generated:", [p.name for p in PUB.rglob("*.html")], "+ sitemap.xml robots.txt")

if __name__ == "__main__":
    main()