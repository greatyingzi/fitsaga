#!/usr/bin/env python3
import pathlib
# 1) gen_topics.py: 两个索引页(idx/idx_en)补脚本
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
old = '"</body></html>"]' + chr(10) + "    (PUB / " + chr(34) + "topics.html" + chr(34) + ").write_text"
if old in s and s.count("search.js") >= 1:
    # idx 的 parts 结尾(119行附近) — 找 zh idx 的 </body></html>]
    idx_tail = '"' + chr(10) + "    (PUB / " + chr(34) + "topics.html" + chr(34) + ").write_text"
    idx_new = (', ' + chr(39) + '<script src="/lightbox.js" defer></script>' + chr(39)
               + ', ' + chr(39) + '<script src="/search.js" defer></script>' + chr(39)
               + ', ' + chr(39) + '<script src="/theme.js" defer></script>' + chr(39)
               + chr(10) + "    (PUB / " + chr(34) + "topics.html" + chr(34) + ").write_text")
    s = s.replace(idx_tail, idx_new, 1)
    P.write_text(s, encoding="utf-8")
    print("zh idx scripts added")
