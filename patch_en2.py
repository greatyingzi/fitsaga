#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
old = "        (PUB / (" + chr(34) + "topics/" + chr(34) + " + t[" + chr(34) + "slug" + chr(34) + "] + " + chr(34) + ".html" + chr(34) + ")).write_text"
print("old found:", old in s)
if old in s:
    new = (
        "        sub = " + chr(34) + "en/topics" + chr(34) + " if t.get(" + chr(34) + "lang" + chr(34) + ") == " + chr(34) + "en" + chr(34) + " else " + chr(34) + "topics" + chr(34) + "
"
        "        (PUB / sub).mkdir(parents=True, exist_ok=True)
"
        "        (PUB / (sub + " + chr(34) + "/" + chr(34) + " + t[" + chr(34) + "slug" + chr(34) + "] + " + chr(34) + ".html" + chr(34) + ")).write_text"
    )
    s = s.replace(old, new, 1)
    P.write_text(s, encoding="utf-8")
    print("patched")
