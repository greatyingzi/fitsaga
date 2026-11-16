#!/usr/bin/env python3
"""gen_downloads_page.py - 参考图包下载中心页"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

DL_CSS = """
.dwrap{max-width:900px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
.dgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(260px,100%),1fr));gap:14px}
.dcard{background:#241b2c;border-radius:14px;padding:1.1rem;box-shadow:0 4px 14px rgba(0,0,0,.4);display:flex;flex-direction:column;gap:.5rem}
.dcard b{color:#ffd9a8;font-size:.98rem}
.dcard .dmeta{font-size:.78rem;color:#9d8fa8}
.dcard a.dl{display:inline-block;text-align:center;padding:.6rem;border-radius:10px;background:linear-gradient(135deg,#ff7eb3,#a855f7);color:#fff;font-weight:700;text-decoration:none;margin-top:.3rem}
.dcard a.dl:hover{filter:brightness(1.1)}
"""

def main():
    manifest = json.loads((PUB / "downloads" / "manifest.json").read_text(encoding="utf-8"))
    cards = []
    for m in manifest:
        cards.append(f'''<div class="dcard">
  <b>🔥 {html.escape(m["title"])}</b>
  <div class="dmeta">{m["count"]} 张对照参考图 · {m["size_kb"]} KB · zip</div>
  <a class="dl" href="{m["zip"]}" download>⬇ 下载参考图包</a>
</div>''')
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>参考图包下载 · FitSaga AI 画法研究所</title>
<meta name="description" content="全部专题的正反例对照参考图免费打包下载：GTA6、汉服、光线、面料、婚纱等 AI 生成参考集。">
<style>{CSS}</style><style>{DL_CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#c793ff">参考图包下载</span></h1>
<p class="sub">{len(manifest)} 个专题 · {sum(m["count"] for m in manifest)} 张对照图 · 全部免费</p></header>
<main class="dwrap"><div class="dgrid">{"".join(cards)}</div></main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · AI 画法研究所</div>
<div class="source">参考图为 AI 生成，可自由用于 prompt 学习与创作参考 · © 2026 FitSaga</div></footer>
<script src="/search.js" defer></script>
<script src="/theme.js" defer></script>
</body></html>'''
    (PUB / "downloads.html").write_text(page, encoding="utf-8")
    print("downloads.html:", len(manifest), "packs")

if __name__ == "__main__":
    main()
