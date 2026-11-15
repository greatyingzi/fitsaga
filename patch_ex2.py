#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34)  # "
S = chr(39)  # '
# 67行: img good
lines[66] = ("            ex_html += " + S + "<figure style=" + D + "margin:0" + D + "><img src=" + D
             + " /topics/gta6/" + D + " + s2 + " + D + "-good.jpg" + D + " loading=" + D + "lazy" + D + ">" + S)
# 68-69: figcaption good (合并为一行)
lines[67] = ("            ex_html += " + S + "<figcaption style=" + D + "font-size:.75rem;color:#8ec5ff" + D
             + ">OK " + S + " + html.escape(ex2[" + D + "good_cap" + D + "]) + " + S + "</figcaption>" + S)
lines[68] = ""
# 70行: img bad
lines[69] = ("            ex_html += " + S + "<figure style=" + D + "margin:0" + D + "><img src=" + D
             + " /topics/gta6/" + D + " + s2 + " + D + "-bad.jpg" + D + " loading=" + D + "lazy" + D + ">" + S)
# 71-72: figcaption bad
lines[70] = ("            ex_html += " + S + "<figcaption style=" + D + "font-size:.75rem;color:#cbb8d4" + D
             + ">X " + S + " + html.escape(ex2[" + D + "bad_cap" + D + "]) + " + S + "</figcaption>" + S)
lines[71] = ""
P.write_text(chr(10).join(lines), encoding="utf-8")
print("4 lines rewritten")
