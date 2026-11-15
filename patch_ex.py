#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
NL = chr(10)
marker = "        chase = "
i = s.find(marker)
print("marker at:", i)
if i > 0:
    Q = chr(39)
    ex = []
    ex.append('        ex_html = ""')
    ex.append('        for ex2 in t.get("examples", []):')
    ex.append('            s2 = ex2["slug"]')
    ex.append('            ex_html += "<h3>" + html.escape(ex2["title"]) + "</h3>"')
    ex.append("            ex_html += " + Q + "<div style=" + chr(34) + "display:grid;grid-template-columns:1fr 1fr;gap:10px" + chr(34) + ">" + Q)
    ex.append("            ex_html += " + Q + "<figure style=" + chr(34) + "margin:0" + chr(34) + "><img src=" + chr(34) + "/topics/gta6/" + chr(34) + " + s2 + " + chr(34) + "-good.jpg" + chr(34) + " loading=" + chr(34) + "lazy" + chr(34) + ">" + Q)
    ex.append("            ex_html += " + Q + "<figcaption style=" + chr(34) + "font-size:.75rem;color:#8ec5ff" + chr(34) + ">OK " + chr(34) + " + html.escape(ex2[")
    ex.append("                " + Q + "good_cap" + Q + "]) + " + Q + "</figcaption>" + Q)
    ex.append("            ex_html += " + Q + "<figure style=" + chr(34) + "margin:0" + chr(34) + "><img src=" + chr(34) + "/topics/gta6/" + chr(34) + " + s2 + " + chr(34) + "-bad.jpg" + chr(34) + " loading=" + chr(34) + "lazy" + chr(34) + ">" + Q)
    ex.append("            ex_html += " + Q + "<figcaption style=" + chr(34) + "font-size:.75rem;color:#cbb8d4" + chr(34) + ">X " + chr(34) + " + html.escape(ex2[")
    ex.append("                " + Q + "bad_cap" + Q + "]) + " + Q + "</figcaption>" + Q)
    ex.append("            ex_html += " + Q + "</figure>" + Q)
    ex.append("            ex_html += " + Q + "</div>" + Q)
    s = s[:i] + NL.join(ex) + NL + s[i:]
    s = s.replace("body, chase, faq,", "body, ex_html, chase, faq,")
    P.write_text(s, encoding="utf-8")
    print("patched OK")
