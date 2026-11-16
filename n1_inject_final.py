#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39); NL = chr(10)
if "themes_html" in s:
    print("already")
    raise SystemExit
B = []
def a(x):
    B.append(x)
a('        if t.get("slug") == "infinity-nikki-outfit-ideas":')
a('            import sqlite3 as _sq')
a('            _c2 = _sq.connect(DB)')
a('            THEMES = [("Dreamy", ["梦", "夜"]), ("Floral", ["花"]), ("Starlit", ["星", "月"]), ("Snowy", ["雪"]), ("Oceanic", ["海"])]')
a("            themes_html = ''")
a('            for tname, kws in THEMES:')
a('                cards2 = []')
a('                seen2 = set()')
a('                for kw2 in kws:')
a("                    for (nm,) in _c2.execute('SELECT name FROM suits WHERE game=? AND name LIKE ? AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) LIMIT 10', ('无限暖暖', '%' + kw2 + '%')):")
a('                        if nm not in seen2:')
a('                            seen2.add(nm)')
a("                            _sid = _c2.execute('SELECT id FROM suits WHERE game=? AND name=?', ('无限暖暖', nm)).fetchone()[0]")
a("                            _img = _c2.execute('SELECT img_url FROM suit_imgs WHERE suit_id=? LIMIT 1', (_sid,)).fetchone()")
a('                            if _img: cards2.append((_img[0], nm))')
a('                cards2 = cards2[:8]')
a("                themes_html += '<h3>' + tname + ' (' + str(len(cards2)) + ')</h3>'")
a('                themes_html += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:.6rem 0 1rem">'')
a('                for u2, nm2 in cards2:')
a('                    themes_html += '<figure style="margin:0"><img src="' + u2 + '" loading="lazy" style="width:100%;border-radius:8px"><figcaption style="font-size:.7rem;color:#9d8fa8;margin-top:.2rem">' + nm2 + '</figcaption></figure>'')
a("                themes_html += '</div>'")
a('            _c2.close()')
lines = s.split(NL)
done = False
for i, l in enumerate(lines):
    if l.strip().startswith("chase = ") and "updated" in l:
        lines[i:i] = B
        done = True
        break
s = NL.join(lines)
s = s.replace("rel_html, chase, dl_btn,", "rel_html, themes_html, chase, dl_btn,", 1)
P.write_text(s, encoding="utf-8")
print("injected:", done)
