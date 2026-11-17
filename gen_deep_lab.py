#!/usr/bin/env python3
"""gen_deep_lab.py - 深度方法论专区 /deep-lab.html"""
import json, pathlib, html
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PUB = ROOT / "public"
CSS = open(ROOT / "site.css", encoding="utf-8").read()
GROUPS = [
  ("诊断与调试", ["ai-fashion-failure-atlas", "prompt-debug-checklist", "why-ai-fashion-looks-plastic", "prompt-anti-patterns"]),
  ("语法与结构", ["fashion-ai-prompt-grammar", "the-anatomy-of-a-viral-fashion-prompt", "the-readability-paradox", "building-a-visual-vocabulary"]),
  ("设计语言", ["nikki-design-language", "chinese-garment-taxonomy-en", "hanfu-color-meanings", "commerce-of-fictional-places"]),
  ("观察与洞察", ["why-mamian-went-global", "the-economy-of-ai-reference-images", "visual-trends-half-life", "why-saving-more-is-worse"]),
  ("创作工具", ["style-deconstruction-workflow", "reference-hygiene", "the-prompt-lab-method", "ai-fashion-copyright-map"]),
  ("数据与实证", ["the-68-experiments", "what-4547-images-say", "why-1587-suits", "negative-results-matter", "content-as-structure"]),
]
def main():
    idx = {}
    for f in (ROOT/"collector").glob("_topic_*.json"):
        t = json.loads(f.read_text(encoding="utf-8"))
        if t.get("type") != "deep": continue
        idx[t["slug"]] = t
    sections = []
    for gname, slugs in GROUPS:
        cards = []
        for s in slugs:
            t = idx.get(s)
            if not t: continue
            sub = "en/topics" if t.get("lang") == "en" else "topics"
            cards.append(f'<a class="scard" style="padding:1rem;display:block" href="/{sub}/{s}"><div class="sname">{html.escape(t["title"])}</div><div class="smeta" style="margin-top:.4rem;line-height:1.7">{html.escape(t["lede"][:70])}…</div></a>')
        sections.append(f'<h2 style="color:#c793ff;margin-top:2rem">{gname}</h2><div class="tgrid">{chr(10).join(cards)}</div>')
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 画法方法论实验室 · FitSaga</title>
<meta name="description" content="20 篇基于独家数据的原创方法论：从失败模式图鉴、prompt 语法学，到跨文化观察与创作工具。FitSaga AI 画法研究所。">
<style>{CSS}</style></head><body>
<header class="hero small"><h1><span style="color:#c793ff">🧠 AI 画法方法论实验室</span></h1>
<p class="sub">20 篇原创框架 · 60 组对照实验 · 4,700 张图库 · 2,000+ 套装数据</p></header>
<main class="sec">
<p style="color:#d8c9de;line-height:1.9;max-width:760px">这里不是 prompt 技巧合集——每一篇都是基于本站自有数据归纳出的原创框架。数据别人没有，框架不可速成，这是我们唯一的护城河。</p>
{chr(10).join(sections)}
<p style="margin-top:2.5rem"><a href="/topics.html" style="color:#ff9ec7">← 全部专题（教程与热点）</a></p>
</main>
<footer><div><b style="color:#f5c76e">FitSaga</b> · AI 画法研究所</div>
<div class="source">方法论基于站内对照实验与图库数据 · © 2026 FitSaga</div></footer>
<script src="/search.js" defer></script><script src="/theme.js" defer></script>
</body></html>'''
    (PUB/"deep-lab.html").write_text(page, encoding="utf-8")
    print("deep-lab.html:", len(sections), "groups")
if __name__ == "__main__": main()
