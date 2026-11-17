#!/usr/bin/env python3
"""生成全量 sitemap.xml — 必须在生成链最后跑"""
import sqlite3, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"
BASE = "https://fitsaga.pages.dev"

def slugify(name):
    s = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", name.strip())
    return s.strip("-") or "suit"

def main():
    today = datetime.date.today().isoformat()
    entries = [(f"{BASE}/", "1.0")]
    # 风格页
    for k in ["hanfu","qipao","sweet","sexy","jk","street","winter","beauty","korean"]:
        entries.append((f"{BASE}/style/{k}.html", "0.8"))
    # 图鉴索引
    # zh 专题页（自动扫描，排除 en）
    import json as _json
    for f in sorted(pathlib.Path(".").glob("collector/_topic_*.json")):
        if "_en_" in f.name: continue
        t = _json.loads(f.read_text(encoding="utf-8"))
        entries.append((BASE + "/topics/" + t["slug"], "0.8"))
    entries.append((BASE + "/topics.html", "0.8"))
    entries.append((BASE + "/deep-lab.html", "0.9"))
    # EN 专题页
    for f in sorted(pathlib.Path(".").glob("collector/_topic_en_*.json")):
        t = _json.loads(f.read_text(encoding="utf-8"))
        entries.append((BASE + "/en/topics/" + t["slug"], "0.8"))
    entries.append((BASE + "/en/topics.html", "0.8"))
    entries.append((BASE + "/en/nikki-outfits", "0.8"))
    entries.append((BASE + "/downloads.html", "0.7"))
    for f in ["infinity","shining","miracle"]:
        entries.append((f"{BASE}/nikki/{f}.html", "0.8"))
    for p in [2,3,4,5]:
        entries.append((f"{BASE}/nikki/infinity-{p}.html", "0.7"))
    # 合集
    for c in ["starry-night","fairytale-dream","spring-floral","ocean-rain","dark-gothic",
              "jk-uniform","sweet-girl","quiet-luxury","dopamine","millard","american-retro",
              "french-style","new-chinese","commute","knitwear","coat-season","qipao-modern",
              "lolita-picks","hanfu-daily","travel-hanfu","eye-makeup","skincare","pseudo-nude","old-money","minimalist","y2k","petite","pear-shape","hoodie","dress-styles","nail-art","first-love","milk-style","heiress","baddie","office","travel-outfit","korean-style","qipao","mamian","makeup-tutorial","makeup-basics","elegant","american-retro-b","daily-wear","winter-coat","japanese-style","blazer","skirt-outfit","french-style-b"]:
        entries.append((f"{BASE}/collection/{c}", "0.9"))
    # 全部详情页(有图的)
    con = sqlite3.connect(DB)
    for (sid,) in con.execute("SELECT s.id FROM suits s WHERE EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=s.id)"):
        row = con.execute("SELECT name FROM suits WHERE id=?", (sid,)).fetchone()
        if row:
            entries.append((f"{BASE}/nikki/s/{slugify(row[0])}", "0.6"))
    con.close()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    seen = set()
    for u,p in entries:
        if u in seen: continue
        seen.add(u)
        xml.append(f"<url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>")
    xml.append("</urlset>")
    (PUB/"sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
    print("sitemap urls:", len(seen))

if __name__ == "__main__":
    main()