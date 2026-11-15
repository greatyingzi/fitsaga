#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
# 输出目录按lang分流 + hreflang
old = '        (PUB / ("topics/" + t["slug"] + ".html")).write_text(chr(10).join(parts), encoding="utf-8")'
new = '''        sub = "en/topics" if t.get("lang") == "en" else "topics"
        (PUB / sub).mkdir(parents=True, exist_ok=True)
        (PUB / (sub + "/" + t["slug"] + ".html")).write_text(chr(10).join(parts), encoding="utf-8")'''
assert old in s
s = s.replace(old, new, 1)
# canonical按lang
old2 = "https://fitsaga.pages.dev/topics/" + chr(34) + " + t["
# 简化: canonical行已有, en时替换——直接在parts里把topics/换成基于lang的路径
s = s.replace(''<link rel="canonical" href="https://fitsaga.pages.dev/topics/' + t["slug"] + "'>', 
              ''https://fitsaga.pages.dev/' + ("en/topics/" if t.get("lang")=="en" else "topics/") + t["slug"] + "'>')
# cards的链接按lang
old3 = ''<a class="scard" href="/topics/' + t["slug"]'
s = s.replace(old3, ''<a class="scard" href="/' + ("en/" if t.get("lang")=="en" else "") + "topics/" + t["slug"]', 1)
P.write_text(s, encoding="utf-8")
print("en support patched")
