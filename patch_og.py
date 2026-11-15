#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
if 'property="og:' not in s:
    s = s.replace(
        "def page(title, desc, body, accent, path=\"/\"):",
        "OG_TAGS = '<meta property=\"og:title\" content=\"FitSaga \u00b7 每一种美，都值得一场时装冒险\"><meta property=\"og:description\" content=\"古风汉服、旗袍、甜美、辣妹、JK、街拍——真实搭配灵感与AI画法专题\"><meta property=\"og:type\" content=\"website\"><meta property=\"og:url\" content=\"https://fitsaga.pages.dev/\"><meta name=\"twitter:card\" content=\"summary\"\'\n\ndef page(title, desc, body, accent, path=\"/\"):",
        1)
    P.write_text(s, encoding="utf-8")
    print("og def added")
else:
    print("og already")
