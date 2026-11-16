#!/usr/bin/env python3
import pathlib

SCRIPTS = '<script src="/search.js" defer></script>' + chr(10) + '<script src="/theme.js" defer></script>'

# gen_guide.py: guide.html索引
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_guide.py")
s = P.read_text(encoding="utf-8")
if "search.js" not in s.split("def main")[0] or 'source' in s:
    # guide索引的</body>前注入
    anchor = "<div class='source'>文章基于站内图片库与搜索词证据生成 · © 2026 FitSaga</div></footer>"
    if anchor in s and s.count("<script src="/search.js"") < 2:
        s = s.replace("</body></html>'''", SCRIPTS + "
</body></html>'''", 1)
        P.write_text(s, encoding="utf-8")
        print("guide idx injected")

# gen_ai.py
P2 = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_ai.py")
s2 = P2.read_text(encoding="utf-8")
if s2.count("search.js") < 2:
    s2 = s2.replace('<script src="/lightbox.js" defer></script>', '<script src="/lightbox.js" defer></script>' + chr(10) + SCRIPTS, 1)
    P2.write_text(s2, encoding="utf-8")
    print("ai idx injected")

# gen_zara.py
P3 = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_zara.py")
s3 = P3.read_text(encoding="utf-8")
if s3.count("search.js") < 1:
    s3 = s3.replace('<script src="/lightbox.js" defer></script>', '<script src="/lightbox.js" defer></script>' + chr(10) + SCRIPTS, 1)
    P3.write_text(s3, encoding="utf-8")
    print("zara injected")
