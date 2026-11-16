#!/usr/bin/env python3
import pathlib
D = chr(34); S = chr(39); NL = chr(10)
SCRIPTS = S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + " + NL + " + S + "<script src=" + D + "/theme.js" + D + " defer></script>" + S

def inject(fname, anchor_part, mode):
    P = pathlib.Path("/Users/liheng/work/self/fitsaga/" + fname)
    s = P.read_text(encoding="utf-8")
    if "search.js" in s and mode == "idx":
        # 已经在文章模板里有了; 只需确认索引模板也有——统一在 </body></html> 前插入到 idx 部分
        # 找最后一个 </body></html> 出现处之前的 footer 文本锚
        pass
    if s.count("search.js") >= 2:
        print(fname, "skip (already)")
        return
    # 直接在文件的 </body></html>''' 前插入 scripts 引用(适用于所有模板尾部)
    tail = "</body></html>"
    if tail in s:
        inject_line = "SCRIPTS_TAIL = " + S + "<script src=" + D + "/search.js" + D + " defer></script><script src=" + D + "/theme.js" + D + " defer></script>" + S
        s = s.replace(tail, "{SCRIPTS_TAIL}" + tail, 1) if "{SCRIPTS_TAIL}" not in s else s
        # 定义 SCRIPTS_TAIL(文件头)
        s = s.replace("import ", "SCRIPTS_TAIL = " + S + "<script src=" + D + "/search.js" + D + " defer></script><script src=" + D + "/theme.js" + D + " defer></script>" + S + NL + "import ", 1)
        P.write_text(s, encoding="utf-8")
        print(fname, "tail-injected")

# 用更直接的方式: 每个生成器的索引页 body 结尾都是 </body></html> — 但 f-string 里才生效
# 最稳: 直接在生成器源码里把固定 footer 字符串替换
for fname, footer_key in [
    ("gen_guide.py", "文章基于站内图片库与搜索词证据生成"),
    ("gen_ai.py", "图片由社区模型生成"),
    ("gen_zara.py", "图片版权归 ZARA"),
]:
    P = pathlib.Path("/Users/liheng/work/self/fitsaga/" + fname)
    s = P.read_text(encoding="utf-8")
    if "search.js" in s.split(footer_key)[1][:200] if footer_key in s else False:
        print(fname, "already")
        continue
    if footer_key not in s:
        print(fname, "footer key missing")
        continue
    # 在footer_key所在行前插入脚本行
    lines = s.split(NL)
    for i, l in enumerate(lines):
        if footer_key in l:
            lines.insert(i, "  <script src=\"/search.js\" defer></script>")
            lines.insert(i+1, "  <script src=\"/theme.js\" defer></script>")
            P.write_text(NL.join(lines), encoding="utf-8")
            print(fname, "injected before footer")
            break
