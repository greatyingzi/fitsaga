#!/usr/bin/env python3
"""gen_topics.py - topic pages generator, bilingual (zh + en)"""
import sqlite3, pathlib, html, re, json, datetime

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
CSS = open(ROOT / "site.css", encoding="utf-8").read()

TOPIC_CSS = """.twrap{max-width:760px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
.twrap h1{font-size:clamp(1.5rem,4vw,2.1rem);font-weight:800;line-height:1.4;color:#fff}
.twrap .badge{display:inline-block;padding:.3rem .8rem;border-radius:999px;background:linear-gradient(135deg,#ff7eb3,#a855f7);color:#fff;font-size:.78rem;font-weight:700;margin-bottom:1rem}
.twrap .lede{font-size:1.02rem;line-height:2;color:#f0e8f3;border-left:3px solid #a855f7;padding-left:1rem;margin:1.4rem 0}
.twrap h2{font-size:1.25rem;color:#ffd9a8;margin:2rem 0 .7rem;font-weight:800}
.twrap h3{font-size:1.02rem;color:#c793ff;margin:1.4rem 0 .5rem}
.twrap p{line-height:2;color:#e8dff0;margin:.7rem 0;font-size:.95rem}
.twrap p b{color:#ff9ec7}
.twrap pre{background:#0f0c13;border:1px solid #3a2a44;border-radius:12px;padding:1rem 1.1rem;overflow-x:auto;margin:1rem 0}
.twrap pre code{color:#8ec5ff;font-size:.82rem;line-height:1.9;font-family:ui-monospace,Menlo,monospace}
.twrap details{background:#1a1420;border-radius:12px;margin:.6rem 0;padding:.9rem 1rem;border:1px solid #3a2a44}
.twrap summary{cursor:pointer;font-weight:700;color:#ffd9a8}
.twrap details p{margin:.5rem 0 0;font-size:.92rem}
.twrap .chase{background:linear-gradient(135deg,#2a1832,#4a1f45);border-radius:14px;padding:1rem 1.1rem;margin:1.5rem 0;border-left:3px solid #ff7eb3}
.twrap .chase b{color:#ff7eb3}
.twrap .meta{color:#9d8fa8;font-size:.85rem;margin:.6rem 0}"""

FENCE = chr(96) * 3
NL = chr(10)

def md2html(md):
    out, in_code, buf = [], False, []
    for line in md.split(NL):
        if line.strip().startswith(FENCE):
            if in_code:
                out.append("<pre><code>" + html.escape(NL.join(buf)) + "</code></pre>")
                buf, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            buf.append(line)
            continue
        if line.startswith("## "):
            out.append("<h2>" + html.escape(line[3:]) + "</h2>")
        elif line.startswith("### "):
            out.append("<h3>" + html.escape(line[4:]) + "</h3>")
        elif line.startswith("- "):
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(line[2:]))
            out.append("<p style='padding-left:1.2rem'>· " + t + "</p>")
        elif line.strip():
            t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(line))
            out.append("<p>" + t + "</p>")
    return NL.join(out)

def main():
    topics = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "collector").glob("_topic_*.json"))]
    zh_cards, en_cards = [], []
    today = datetime.date.today().isoformat()
    for t in topics:
        is_en = t.get("lang") == "en"
        sub = "en/topics" if is_en else "topics"
        (PUB / sub).mkdir(parents=True, exist_ok=True)
        body = md2html(t["body_md"])
        faq = ""
        if t.get("faq"):
            faq = "<h2>" + ("FAQ" if is_en else "常见问题") + "</h2><div>" + "".join(
                "<details><summary>" + html.escape(q) + "</summary><p>" + html.escape(a) + "</p></details>"
                for q, a in t["faq"]) + "</div>"
        ex_html = ""
        for ex2 in t.get("examples", []):
            s2 = ex2["slug"]
            base = "/topics/" + t["slug"] + "/"
            ex_html += "<h3>" + html.escape(ex2["title"]) + "</h3>"
            ex_html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
            ex_html += '<figure style="margin:0"><div style="background:#1d4d2b;color:#a8e6a3;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700">OK PROMPT</div><img src="' + base + s2 + '-good.jpg" loading="lazy" style="width:100%;border-radius:10px"><figcaption style="font-size:.75rem;color:#8ec5ff;line-height:1.7">OK ' + html.escape(ex2["good_cap"]) + '</figcaption></figure>'
            ex_html += '<figure style="margin:0"><div style="background:#4d1d1d;color:#e6a8a8;font-size:.72rem;padding:.3rem .6rem;border-radius:8px 8px 0 0;font-weight:700">WEAK</div><img src="' + base + s2 + '-bad.jpg" loading="lazy" style="width:100%;border-radius:10px;opacity:.85"><figcaption style="font-size:.75rem;color:#cbb8d4;line-height:1.7">X ' + html.escape(ex2["bad_cap"]) + '</figcaption></figure>'
            ex_html += '</div>'
        dl_btn = ""
        try:
            _mf = json.loads((PUB / "downloads/manifest.json").read_text(encoding="utf-8"))
            for _m in _mf:
                if _m["slug"] == t["slug"]:
                    dl_btn = '<p style="margin-top:1rem"><a style="background:linear-gradient(135deg,#ff7eb3,#a855f7);color:#fff;padding:.7rem 1.2rem;border-radius:10px;text-decoration:none;font-weight:700" href="' + _m["zip"] + '" download>⬇ 下载本专题参考图包（' + str(_m["count"]) + ' 张）</a></p>'
                    break
        except Exception:
            pass

        _rel_lab = "Related topics" if is_en else "相关专题"
        rel_html = '<p style="margin-top:2rem;color:#9d8fa8;font-size:.85rem">' + _rel_lab + '：</p><nav class="stylechips" style="margin-top:.4rem;justify-content:flex-start">'
        _others = [t2 for t2 in topics if t2["slug"] != t["slug"] and (t2.get("lang", "zh") == t.get("lang", "zh"))]
        for t2 in _others[:3]:
            _sub2 = 'en/topics' if t2.get("lang") == "en" else 'topics'
            rel_html += '<a class="chip" style="background:linear-gradient(135deg,#2a1832,#a855f766)" href=/' + _sub2 + '/' + t2["slug"] + '>' + html.escape(t2["title"][:20]) + '</a>'
            rel_html += '</nav>'

        chase = ""
        try:
            _cl = json.loads((ROOT / "data" / "changelog.json").read_text(encoding="utf-8"))
            _my = [c for c in _cl if c.get("slug") == t["slug"]]
            if _my:
                _lab = "Chase log" if is_en else "追更日志"
                _items = "".join("<div style=\"margin:.25rem 0\"><b style=\"color:#ffd9a8\">" + c["date"] + "</b> — " + html.escape(c["note"]) + "</div>" for c in _my[-3:])
                chase = '<div class="chase"><b>🔄 ' + _lab + '</b>' + _items + '</div>'
            elif t.get("updated"):
                chase = '<div class="chase"><b>追更</b> · ' + html.escape(t["updated"]) + '</div>'
        except Exception:
            if t.get("updated"):
                chase = '<div class="chase"><b>追更</b> · ' + html.escape(t["updated"]) + '</div>'
        badge = '<span class="badge">HOT</span>' if t.get("type") == "hot" else '<span class="badge">EVERGREEN</span>'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": t["title"],
                         "description": t["lede"][:150], "datePublished": today,
                         "author": {"@type": "Organization", "name": "FitSaga"}}, ensure_ascii=False)
        home_link = "/en/topics.html" if is_en else "/topics.html"
        brand = "FitSaga AI Reference" if is_en else "FitSaga AI 画法研究所"
        parts = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">' if is_en else '<html lang="zh-CN"><head><meta charset="utf-8">',
                 '<meta name="viewport" content="width=device-width,initial-scale=1">',
                 '<meta name="referrer" content="no-referrer">',
                 "<title>" + html.escape(t["title"]) + " · " + brand + "</title>",
                 '<meta name="description" content="' + html.escape(t["lede"][:120]) + '">',
                 '<link rel="canonical" href="https://fitsaga.pages.dev/' + sub + '/' + t["slug"] + '">',
                 "<style>" + CSS + "</style><style>" + TOPIC_CSS + "</style>",
                 '<script type="application/ld+json">' + ld + "</script>", "</head><body>",
                 '<div class="twrap"><article>', badge,
                 "<h1>" + html.escape(t["title"]) + "</h1>",
                 '<div class="meta">' + brand + " · " + today + "</div>",
                 '<div class="lede">' + html.escape(t["lede"]) + "</div>",
                 body, ex_html, rel_html, chase, dl_btn, faq,
                 '<p style="margin-top:2.5rem"><a href="' + home_link + '">← ' + ("All topics" if is_en else "全部专题") + '</a> · <a href="/">Home</a></p>',
                 '</article></div>',
                 '<script src="/lightbox.js" defer></script>',
                 '<script src="/search.js" defer></script>',
                 '<script src="/theme.js" defer></script>',
                 '</body></html>']
        card = '<a class="scard" href="/' + sub + '/' + t["slug"] + '" style="padding:1rem;display:block"><div class="sname">' + ("🔥 " if t.get("type") == "hot" else "📚 ") + html.escape(t["title"]) + '</div><div class="smeta" style="margin-top:.4rem;line-height:1.7">' + html.escape(t["lede"][:70]) + '…</div></a>'
        (en_cards if is_en else zh_cards).append(card)
        (PUB / (sub + "/" + t["slug"] + ".html")).write_text(NL.join(parts), encoding="utf-8")
        print(("en:" if is_en else "zh:") + t["slug"], "| zh_cards:", len(zh_cards))
    # 中文索引
    idx = ["<!doctype html>", '<html lang="zh-CN"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           "<title>AI 画法研究所 · FitSaga</title>",
           '<meta name="description" content="热点与常青专题：把游戏、影视、流行文化的视觉风格翻译成可复制的 AI prompt 方案。">',
           "<style>" + CSS + "</style><style>" + TOPIC_CSS + "</style></head><body>",
           '<header class="hero small"><h1><span style="color:#c793ff">AI 画法研究所</span></h1>',
           "<p class='sub'>热点专题 × 常青风格 — 把任何美学翻译成 prompt</p></header>",
           '<main class="sec"><div class="sgrid">' + "".join(zh_cards) + "</div></main>",
           '<footer><div><b style="color:#f5c76e">FitSaga</b> · AI 画法研究所</div>',
           "<div class='source'>prompt 方案与视觉拆解为原创内容 · © 2026 FitSaga</div></footer>",
           '<script src="/lightbox.js" defer></script><script src="/search.js" defer></script><script src="/theme.js" defer></script>']
    (PUB / "topics.html").write_text(NL.join(idx), encoding="utf-8")
    # 英文索引
    idx_en = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
              '<meta name="viewport" content="width=device-width,initial-scale=1">',
              "<title>AI Reference Topics · FitSaga</title>",
              '<meta name="description" content="Hot and evergreen topics: translating game, film and pop-culture aesthetics into copy-paste AI prompt formulas.">',
              "<style>" + CSS + "</style><style>" + TOPIC_CSS + "</style></head><body>",
              '<header class="hero small"><h1><span style="color:#c793ff">AI Reference Topics</span></h1>',
              "<p class='sub'>Hot topics x evergreen styles — turn any aesthetic into prompts</p></header>",
              '<main class="sec"><div class="sgrid">' + "".join(en_cards) + "</div></main>",
              '<footer><div><b style="color:#f5c76e">FitSaga</b> · AI Reference</div>',
              "<div class='source'>Prompt formulas and visual breakdowns are original content · © 2026 FitSaga</div></footer>",
              '<script src="/lightbox.js" defer></script><script src="/search.js" defer></script><script src="/theme.js" defer></script>']
    (PUB / "en").mkdir(parents=True, exist_ok=True)
    (PUB / "en/topics.html").write_text(NL.join(idx_en), encoding="utf-8")
    print("zh topics:", len(zh_cards), "| en topics:", len(en_cards))

if __name__ == "__main__":
    main()