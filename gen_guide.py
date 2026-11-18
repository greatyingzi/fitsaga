#!/usr/bin/env python3
"""gen_guide.py — 文章系统: articles表→/guide/<slug>.html + /guide.html索引"""
import sqlite3, pathlib, html, re, json, datetime

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

ARTICLE_CSS = """
.gwrap{max-width:680px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
.gwrap h1{font-size:clamp(1.6rem,4vw,2.2rem);line-height:1.4;font-weight:800;color:#fff}
.gwrap .meta{color:#9d8fa8;font-size:.85rem;margin:.8rem 0 1.8rem}
.gwrap .lede{font-size:1.05rem;line-height:2;color:#f0e8f3;border-left:3px solid #ff7eb3;padding-left:1rem;margin-bottom:1.8rem}
.gwrap h2{font-size:1.25rem;color:#ffd9a8;margin:2rem 0 .8rem;font-weight:800}
.gwrap p{line-height:2;color:#e8dff0;margin:.7rem 0;font-size:.98rem}
.gwrap .formula{background:#241b2c;border-radius:14px;padding:1rem 1.1rem;margin:.9rem 0;border:1px solid #3a2a44}
.gwrap .formula b{color:#ff9ec7}
.gwrap .formula p{margin:0;font-size:.92rem;line-height:1.8}
.gwrap .faq{margin:1.5rem 0}
.gwrap details{background:#241b2c;border-radius:12px;margin:.6rem 0;padding:.9rem 1rem;border:1px solid #3a2a44}
.gwrap summary{cursor:pointer;font-weight:700;color:#ffd9a8;font-size:.95rem}
.gwrap details p{margin:.6rem 0 0;font-size:.92rem}
.gpair{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:1.5rem 0}
.gpair figure{margin:0}.gpair img{width:100%;border-radius:10px}.gpair figcaption{font-size:.75rem;margin-top:.3rem;line-height:1.7}
.gwrap .looks{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(150px,100%),1fr));gap:12px;margin:1.2rem 0}
.gwrap .looks img{width:100%;border-radius:10px;aspect-ratio:3/4;object-fit:cover;display:block}
.gwrap .looks figure{margin:0;position:relative}
.gwrap .looks figcaption{font-size:.72rem;color:#9d8fa8;margin-top:.3rem}
.gwrap .tip{background:linear-gradient(135deg,#2a1832,#3a1f45);border-radius:14px;padding:1rem 1.1rem;margin:1.2rem 0}
.gwrap .tip b{color:#c793ff}
.gwrap a{color:#ff9ec7}
"""

def md2html(md):
    """轻量md: ##/###/**/lists/段落"""
    out = []
    for line in md.split("\n"):
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3 style='color:#f5c76e;font-size:1.05rem;margin:1.2rem 0 .5rem'>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            t = html.escape(line[2:])
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
            out.append(f"<p style='padding-left:1.2rem'>· {t}</p>")
        elif line.strip() == "":
            continue
        else:
            t = html.escape(line)
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
            out.append(f"<p>{t}</p>")
    return "\n".join(out)

def article_html(a, body_html, looks_html, related_html=""):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html.escape(a["title"])} · FitSaga 穿搭研究所</title>
<meta name="description" content="{html.escape(a["lede"][:80])}">
<link rel="canonical" href="https://fitsaga.pages.dev/guide/{a["slug"]}">
<style>{CSS}</style><style>{ARTICLE_CSS}</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["lede"][:150],"datePublished":a.get("published_at","")[:10],"author":{"@type":"Organization","name":"FitSaga"},"publisher":{"@type":"Organization","name":"FitSaga"},"mainEntityOfPage":f"https://fitsaga.pages.dev/guide/{a['slug']}"}, ensure_ascii=False)}</script>
</head><body>
<div class="gwrap">
<article>
<h1>{html.escape(a["title"])}</h1>
<div class="meta">{a["published_at"][:10] if a.get("published_at") else ""} · 穿搭研究所 · 数据来源：站内图片库与搜索词分析</div>
<div class="lede">{html.escape(a["lede"])}</div>
{body_html}
{looks_html}
</article>
{related_html}
<p style="margin-top:2.5rem"><a href="/guide.html">← 返回穿搭研究所</a> · <a href="/deep-lab.html">🧠 方法论实验室</a> · <a href="/">首页</a></p>
</div>
<script src="/lightbox.js" defer></script>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''

def main():
    (PUB / "guide").mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    # articles 表 (若空则写样板文)
    con.executescript("""CREATE TABLE IF NOT EXISTS articles (
      id INTEGER PRIMARY KEY AUTOINCREMENT, topic_id INTEGER, slug TEXT UNIQUE,
      title TEXT NOT NULL, status TEXT DEFAULT 'draft', md_path TEXT, lede TEXT,
      published_at TEXT, created_at TEXT DEFAULT (datetime('now')))""")
    n = con.execute("SELECT COUNT(*) FROM articles WHERE status='published'").fetchone()[0]
    # 扫描全部 _article_*.json 自动入库(幂等)
    for f in sorted((ROOT/"collector").glob("_article_*.json")):
        a = json.loads(f.read_text(encoding="utf-8"))
        cur = con.execute("INSERT OR IGNORE INTO articles (slug,title,status,lede,published_at) VALUES (?,?,'published',?,?)",
                          (a["slug"], a["title"], a.get("lede",""), datetime.datetime.now().isoformat()))
        if cur.rowcount:
            print("article registered:", a["slug"])
    con.commit()
    rows = con.execute("SELECT id,slug,title,lede,published_at FROM articles WHERE status='published'").fetchall()
    urls = []
    for aid, slug, title, lede, pub in rows:
        data = json.loads(open(ROOT/"collector"/f"_article_{slug}.json", encoding="utf-8").read())
        body_html = md2html(data["body"])
        examples_html = ""
        for ex in data.get("examples", []):
            examples_html += "<h2>" + html.escape(ex.get("title", "对照")) + "</h2>"
            examples_html += '<div class="gpair">'
            examples_html += '<figure><img src="/guide-img/' + ex["slug"] + '-good.jpg" loading="lazy"><figcaption style="color:#a8e6a3">OK ' + html.escape(ex.get("good_cap", "")) + '</figcaption></figure>'
            examples_html += '<figure><img src="/guide-img/' + ex["slug"] + '-bad.jpg" loading="lazy"><figcaption style="color:#cbb8d4">X ' + html.escape(ex.get("bad_cap", "")) + '</figcaption></figure>'
            examples_html += "</div>"
        # 相关专题推荐(命中率提升: 决策文→专题)
        RELATED = {
            "laoqianfeng-ruwen": ["quiet-luxury", "dopamine", "old-money", "minimalist"],
            "lolita-xuanpai": ["jk-lolita-ai-guide", "lolita-picks", "jk-uniform"],
            "mamiqun-shangyi": ["hanfu-prompt-guide", "mamian", "hanfu-daily"],
            "xiaogez-xiangao": ["petite", "pear-shape", "commute"],
            "jingshefeng-zenmechuan": ["quiet-luxury", "elegant", "old-money", "minimalist"],
            "zhenzhishan-xuankuan": ["knitwear", "coat-season", "winter-coat"],
            "duobapei-secaigongshi": ["dopamine", "color-psychology", "seasonal-color-engine"],
            "jkzhifu-ruquan": ["jk-uniform", "jk-lolita-ai-guide", "first-love"],
            "tianmei-bianjie": ["sweet-girl", "first-love", "milk-style"],
            "y2k-huichao": ["y2k", "american-retro-b", "street"],
        }
        related_slugs = RELATED.get(slug, [])
        related_html = ""
        if related_slugs:
            chips = "".join(
                f'<a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href="/collection/{rs}">相关合集</a>'
                if not rs.endswith("-guide") and not rs.endswith("-engine") and not rs.endswith("-psychology")
                else f'<a class="chip" style="background:linear-gradient(135deg,#2a1832,#c793ff)" href="/topics/{rs}">相关专题</a>'
                for rs in related_slugs)
            related_html = '<div style="margin-top:2rem;padding:1rem;background:#241b2c;border-radius:12px"><b style="color:#c793ff">延伸阅读 · 从文章到图库</b><nav class="stylechips" style="margin-top:.6rem;justify-content:flex-start">' + chips + '</nav></div>'
        looks = "\n".join(
            f'<figure><img src="{html.escape(u)}" alt="{html.escape(alt)}" loading="lazy"><figcaption>{html.escape(cap)}</figcaption></figure>'
            for u, alt, cap in data["looks"])
        page = article_html({"slug":slug,"title":title,"lede":lede,"published_at":pub}, body_html, examples_html + f'<div class="looks">{looks}</div>', related_html)
        (PUB / f"guide/{slug}.html").write_text(page, encoding="utf-8")
        urls.append((slug, title, lede))
    # guide索引页
    cards = "\n".join(
        f'''<a class="scard" href="/guide/{slug}" style="padding:1rem;display:block">
  <div class="sname">{html.escape(title)}</div>
  <div class="smeta" style="margin-top:.4rem;line-height:1.7">{html.escape((lede or "")[:60])}…</div>
</a>''' for slug, title, lede in urls)
    idx = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>穿搭研究所 · FitSaga</title>
<meta name="description" content="穿搭决策指南：风格怎么穿、派别怎么选、一周方案怎么排——每个建议都来自真实搭配图与搜索词证据。">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#ffd9a8">穿搭研究所</span></h1>
<p class="sub">怎么穿 · 怎么选 · 怎么排 — 把灵感变成决策</p></header>
<main class="sec"><div class="sgrid">{cards}</div></main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 穿搭研究所</div>
  <script src="/search.js" defer></script>
  <script src="/theme.js" defer></script>
<div class="source">文章基于站内图片库与搜索词证据生成 · © 2026 FitSaga</div></footer>
</body></html>'''
    (PUB / "guide.html").write_text(idx, encoding="utf-8")
    print("guide articles:", len(urls))
    con.close()

if __name__ == "__main__":
    main()