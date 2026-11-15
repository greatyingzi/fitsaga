#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
# 1) 在 home() 前加 topic_cards_html 函数
marker = "def home():"
fn = (
    "def topic_cards_html():" + chr(10)
    + "    import json as _json" + chr(10)
    + "    cards = []" + chr(10)
    + "    for f in sorted((ROOT / " + chr(34) + "collector" + chr(34) + ").glob(" + chr(34) + "_topic_*.json" + chr(34) + ")):" + chr(10)
    + "        t = _json.loads(f.read_text(encoding=" + chr(34) + "utf-8" + chr(34) + "))" + chr(10)
    + "        if t.get(" + chr(34) + "lang" + chr(34) + ") == " + chr(34) + "en" + chr(34) + ": continue" + chr(10)
    + "        sub = " + chr(34) + "en/topics" + chr(34) + " if t.get(" + chr(34) + "lang" + chr(34) + ") == " + chr(34) + "en" + chr(34) + " else " + chr(34) + "topics" + chr(34) + chr(10)
    + "        emoji = " + chr(34) + "🔥" + chr(34) + " if t.get(" + chr(34) + "type" + chr(34) + ") == " + chr(34) + "hot" + chr(34) + " else " + chr(34) + "📚" + chr(34) + chr(10)
    + "        cards.append(" + chr(34) + "<a class='scard' style='padding:1rem;display:block' href=/" + chr(34) + " + sub + " + chr(34) + "/" + chr(34) + " + t[" + chr(34) + "slug" + chr(34) + "] + " + chr(34) + "'><div class='sname'>" + chr(34) + " + emoji + " + chr(34) + " " + chr(34) + " + htmlMod.escape(t[" + chr(34) + "title" + chr(34) + "]) + " + chr(34) + "</div><div class='smeta' style='margin-top:.4rem;line-height:1.7'>" + chr(34) + " + htmlMod.escape(t[" + chr(34) + "lede" + chr(34) + "][:60]) + " + chr(34) + "…</div></a>" + chr(34) + ")" + chr(10)
    + "    return chr(10).join(cards)" + chr(10)
    + chr(10)
    + "def home():"
)
assert marker in s
s = s.replace(marker, fn, 1)
# 2) hero后调topic_cards并填{topic_cards}
s = s.replace("    today_cards = today_cards_html()",
              "    today_cards = today_cards_html()\n    topic_cards = topic_cards_html()", 1)
P.write_text(s, encoding="utf-8")
print("card gen added")
