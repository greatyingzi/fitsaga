#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
if "themes_html" in s:
    print("already")
    raise SystemExit
B = []
B.append("        if t.get('slug') == 'infinity-nikki-outfit-ideas':".replace(chr(39), chr(34)))
B.append("            import sqlite3 as _sq")
B.append("            _c2 = _sq.connect(DB)")
B.append("            THEMES = [('Dreamy', ['梦', '夜']), ('Floral', ['花']), ('Starlit', ['星', '月']), ('Snowy', ['雪']), ('Oceanic', ['海'])]")
B.append("            themes_html = ''")
B.append("            for tname, kws in THEMES:")
B.append("                cards2 = []")
B.append("                seen2 = set()")
B.append("                for kw2 in kws:")
B.append("                    for (nm,) in _c2.execute('SELECT name FROM suits WHERE game=? AND name LIKE ? AND EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) LIMIT 10', ('无限暖暖', '%' + kw2 + '%')):")
B.append("                        if nm not in seen2:")
B.append("                            seen2.add(nm)")
B.append("                        _sid = _c2.execute('SELECT id FROM suits WHERE game=? AND name=?', ('无限暖暖', nm)).fetchone()[0]")
B.append("                        _img = _c2.execute('SELECT img_url FROM suit_imgs WHERE suit_id=? LIMIT 1', (_sid,)).fetchone()")
B.append("                            if _img: cards2.append((_img[0], nm))")
B.append("                cards2 = cards2[:8]")
B.append("                themes_html += '<h3>' + tname + ' (' + str(len(cards2)) + ')</h3>'")
B.append('                themes_html += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:.6rem 0 1rem">'')
B.append("                for u2, nm2 in cards2:")
B.append('                    themes_html += '<figure style="margin:0"><img src="' + u2 + '" loading="lazy" style="width:100%;border-radius:8px"><figcaption style="font-size:.7rem;color:#9d8fa8;margin-top:.2rem">' + nm2 + '</figcaption></figure>'')
B.append("                themes_html += '</div>'")
B.append("            _c2.close()")
lines = s.split(chr(10))
done = False
for i, l in enumerate(lines):
    if l.strip().startswith("chase = ") and "updated" in l:
        lines[i:i] = B
        done = True
        break
s = chr(10).join(lines)
s = s.replace("rel_html, chase, dl_btn,", "rel_html, themes_html, chase, dl_btn,", 1)
P.write_text(s, encoding="utf-8")
print("injected:", done)
