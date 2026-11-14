
# ---------- Nikki 套装页生成 (gen_nikki.py) ----------
import sqlite3, pathlib
import html as html_mod

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
CSS = open(ROOT / "site.css", encoding="utf-8").read() if (ROOT / "site.css").exists() else ""

SLUG_RE = None

def slugify(name: str) -> str:
    # 中文名slug: 保留中文, 替换非法字符
    import re
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", name.strip())
    return s.strip("-") or "suit"

def gen_nikki_pages(limit_games=("无限暖暖", "闪耀暖暖", "奇迹暖暖"), per_game_cap=300):
    out = []
    con = sqlite3.connect(DB)
    (PUB / "nikki").mkdir(parents=True, exist_ok=True)
    sitemap_urls = []
    for game in limit_games:
        rows = con.execute("SELECT id,name FROM suits WHERE game=? ORDER BY id LIMIT ?",
                           (game, per_game_cap)).fetchall()
        # 索引页
        idx_cards = []
        for sid, name in rows:
            slug = slugify(name)
            first = con.execute("SELECT img_url FROM suit_imgs WHERE suit_id=? LIMIT 1", (sid,)).fetchone()
            cover = first[0] if first else ""
            n_imgs = con.execute("SELECT COUNT(*) FROM suit_imgs WHERE suit_id=?", (sid,)).fetchone()[0]
            if n_imgs == 0: continue
            idx_cards.append(f'''<a class="scard" href="/nikki/{slug}">
  <img src="{html_mod.escape(cover)}" alt="{html_mod.escape(game+name)}套装展示图" loading="lazy">
  <div class="sname">{html_mod.escape(name)}</div>
  <div class="smeta">{n_imgs} 张图 · {html_mod.escape(game)}</div>
</a>''')
        idx_html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{html_mod.escape(game)}套装图鉴 · FitSaga</title>
<meta name="description" content="{html_mod.escape(game)}全部套装图鉴：展示图、部件图、海报，逐张标注来源。">
<style>{CSS}</style><style>
.sgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px}}
.scard{{background:#241b2c;border-radius:14px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.4)}}
.scard img{{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}}
.sname{{padding:.6rem .7rem .1rem;font-weight:700;font-size:.9rem}}
.smeta{{padding:0 .7rem .7rem;font-size:.72rem;color:#9d8fa8}}
</style></head><body>
<header class="hero small"><h1><span style="color:#f5c76e">{html_mod.escape(game)}</span> 套装图鉴</h1>
<p class="sub">{len(idx_cards)} 套 · 数据来自 {("BWIKI")}</p></header>
<main class="sec"><div class="sgrid">{"".join(idx_cards)}</div></main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · 游戏时装图鉴</div>
<div class="source">游戏素材版权归叠纸网络/官方所有 · 数据整理自 BWIKI(biligame) · © 2026 FitSaga</div></footer>
</body></html>'''
        fname = {"无限暖暖":"infinity","闪耀暖暖":"shining","奇迹暖暖":"miracle"}[game]
        (PUB / f"nikki/{fname}.html").write_text(idx_html, encoding="utf-8")
        sitemap_urls.append(f"/nikki/{fname}.html")
        out.append(f"{game} index: {len(idx_cards)} suits")
    con.close()
    return out, sitemap_urls

if __name__ == "__main__":
    import json
    res, urls = gen_nikki_pages()
    print(json.dumps(res, ensure_ascii=False))