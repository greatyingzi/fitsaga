#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39); NL = chr(10)
# zh idx: 找 (PUB / "topics.html") 行, 在其前一行是 </body></html>"] 的数组结尾——数组里加3个元素
idx_write = "(PUB / " + S + "topics.html" + S + ").write_text"
if idx_write in s and s.count("search.js") < 3:
    # 找到含 idx_write 的行号, 向上找 </body></html>"] 行
    lines = s.split(NL)
    wi = next(i for i,l in enumerate(lines) if idx_write in l)
    # 向上找数组结尾行
    for j in range(wi, max(wi-8,0), -1):
        if "</body></html>]" in lines[j]:
            tail_elem = "                 " + S + "<script src=" + D + "/lightbox.js" + D + " defer></script>" + S + ", " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ", " + S + "<script src=" + D + "/theme.js" + D + " defer></script>" + S
            lines[j] = lines[j].replace("</body></html>]", "<script src=" + D + "/lightbox.js" + D + " defer></script><script src=" + D + "/search.js" + D + " defer></script><script src=" + D + "/theme.js" + D + " defer></script></body></html>]")
            P.write_text(NL.join(lines), encoding="utf-8")
            print("zh idx: inline scripts appended (html-level)")
            break
# en idx 同理
en_write = "(PUB / " + S + "en/topics.html" + S + ").write_text"
if en_write in s:
    lines = s.split(NL)
    wi = next(i for i,l in enumerate(lines) if en_write in l)
    for j in range(wi, max(wi-8,0), -1):
        if "</body></html>]" in lines[j]:
            lines[j] = lines[j].replace("</body></html>]", "<script src=" + D + "/lightbox.js" + D + " defer></script><script src=" + D + "/search.js" + D + " defer></script><script src=" + D + "/theme.js" + D + " defer></script></body></html>]")
            P.write_text(NL.join(lines), encoding="utf-8")
            print("en idx: inline scripts appended")
            break
