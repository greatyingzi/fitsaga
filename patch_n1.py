#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39)
anchor = "        dl_btn = " + S
print("dl anchor:", s.find(anchor) > 0)
if "THEMES" not in s:
    themes_code = (
        "        THEMES = [(" + D + "Dreamy" + D + ", [" + D + "梦" + D + ", " + D + "夜" + D + "]), (" + D + "Floral" + D + ", [" + D + "花" + D + "]), (" + D + "Starlit" + D + ", [" + D + "星" + D + ", " + D + "月" + D + "]), (" + D + "Snowy" + D + ", [" + D + "雪" + D + "]), (" + D + "Oceanic" + D + ", [" + D + "海" + D + "])]" + chr(10)
        + "        themes_html = " + chr(34) + chr(34 + chr(10)
    )
    # 上面拼接复杂——改用多行append方式写(在 ex 循环后插)
    block = [
        "        if t.get(" + D + "slug" + D + ") == " + D + "infinity-nikki-outfit-ideas" + D + ":",
        "            import sqlite3 as _sq",
        "            _c2 = _sq.connect(DB)",
        "            THEMES = [(" + D + "Dreamy" + D + ", [" + D + "梦" + D + "," + D + "夜" + D + "]), (" + D + "Floral" + D + ", [" + D + "花" + D + "]), (" + D + "Starlit" + D + ", [" + D + "星" + D + "," + D + "月" + D + "]), (" + D + "Snowy" + D + ", [" + D + "雪" + D + "]), (" + D + "Oceanic" + D + ", [" + D + "海" + D + "])]",
        "            themes_html = " + S + S,
        "            for tname, kws in THEMES:",
        "                cards2 = []",
        "                seen2 = set()",
        "                for kw2 in kws:",
        "                    for (nm,) in _c2.execute(" + S + "SELECT name FROM suits WHERE game='无限暖暖' AND name LIKE ? AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) LIMIT 10" + S + ", (" + S + "%" + S + " + kw2 + " + S + "%" + S + ",)):",
        "                        if nm not in seen2:",
        "                            seen2.add(nm)",
        "                            _sid = _c2.execute(" + S + "SELECT id FROM suits WHERE game='无限暖暖' AND name=?" + S + ", (nm,)).fetchone()[0]",
        "                            _img = _c2.execute(" + S + "SELECT img_url FROM suit_imgs WHERE suit_id=? LIMIT 1" + S + ", (_sid,)).fetchone()",
        "                            if _img: cards2.append((_img[0], nm))",
        "                cards2 = cards2[:8]",
        "                themes_html += " + S + "<h3>" + S + " + tname + " + S + " (" + S + " + str(len(cards2)) + " + S + ")</h3><div style=" + D + "display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:.6rem 0 1rem" + D + ">" + S,
        "                for u2, nm2 in cards2:",
        "                    themes_html += " + S + "<figure style=" + D + "margin:0" + D + "><img src=" + D + S + " + u2 + " + S + S + " loading=" + D + "lazy" + D + " style=" + D + "width:100%;border-radius:8px" + D + "><figcaption style=" + D + "font-size:.7rem;color:#9d8fa8;margin-top:.2rem" + D + ">" + S + " + html.escape(nm2) + " + S + "</figcaption></figure>" + S,
        "                themes_html += " + S + "</div>" + S,
        "            _c2.close()",
    ]
    lines = s.split(chr(10))
    for i, l in enumerate(lines):
        if l.strip().startswith("chase = "):
            lines[i:i] = block
            break
    s = chr(10).join(lines)
    # parts 里 themes_html 插到 chase 后
    s = s.replace("rel_html, chase, dl_btn,", "rel_html, themes_html, chase, dl_btn,", 1)
    P.write_text(s, encoding="utf-8")
    print("themes grid added")
