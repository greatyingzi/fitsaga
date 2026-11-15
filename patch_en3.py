#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
for i, l in enumerate(lines):
    # 99行: 输出分流
    if l.strip().startswith("(PUB / (" + D + "topics/" + D):
        indent = "        "
        new_lines = [
            indent + "sub = " + S + "en/topics" + S + " if t.get(" + D + "lang" + D + ") == " + D + "en" + D + " else " + S + "topics" + S,
            indent + "(PUB / sub).mkdir(parents=True, exist_ok=True)",
            indent + "(PUB / (sub + " + S + "/" + S + " + t[" + D + "slug" + D + "] + " + S + ".html" + S + ")).write_text(chr(10).join(parts), encoding=" + D + "utf-8" + D + ")",
        ]
        lines[i] = new_lines[0]
        lines.insert(i+1, new_lines[1])
        lines.insert(i+2, new_lines[2])
        print("output branch at", i+1)
        break
# 100行: cards链接分流
for i, l in enumerate(lines):
    if "scard" in l and "/topics/" in l and "append" in l:
        lines[i] = l.replace(S + "/topics/" + S, S + "topics/" + S)
        break
P.write_text(chr(10).join(lines), encoding="utf-8")
print("done")
