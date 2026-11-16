#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39)
# 在 faq 渲染后加 rel_html(相关专题: 同语言其他专题3个)
old = "        chase = " + S
probe = s.find(old)
print("chase at:", probe)
if probe > 0 and "rel_html" not in s:
    # 在 chase 赋值行前插入 rel_html 计算
    rel_code = (
        "        rel_html = " + chr(34) + chr(34) + chr(10)
        + "        _others = [t2 for t2 in topics if t2[" + D + "slug" + D + "] != t[" + D + "slug" + D + "] and (t2.get(" + D + "lang" + D + ", " + D + "zh" + D + ") == t.get(" + D + "lang" + D + ", " + D + "zh" + D + "))]" + chr(10)
        + "        for t2 in _others[:3]:" + chr(10)
        + "            _sub2 = " + S + "en/topics" + S + " if t2.get(" + D + "lang" + D + ") == " + D + "en" + D + " else " + S + "topics" + S + chr(10)
        + "            rel_html += " + S + "<a class=" + D + "chip" + D + " style=" + D + "background:linear-gradient(135deg,#2a1832,#a855f766)" + D + " href=/" + S + " + _sub2 + " + S + "/" + S + " + t2[" + D + "slug" + D + "] + " + S + ">" + S + " + html.escape(t2[" + D + "title" + D + "][:20]) + " + S + "</a>" + S + chr(10)
    )
    lines = s.split(chr(10))
    for i, l in enumerate(lines):
        if l.strip().startswith("chase = "):
            lines[i:i] = [x for x in rel_code.split(chr(10))]
            break
    s = chr(10).join(lines)
    # parts 里 chase 前加 rel_html
    s = s.replace("body, ex_html, chase, dl_btn, faq,", "body, ex_html, chase, dl_btn, faq,")  # 已有
    # 找 parts 里 chase 出现处加 rel
    s = s.replace("chase, dl_btn,", "rel_html, chase, dl_btn,", 1)
    # chase后渲染相关专题标题
    s = s.replace(
        "chase, dl_btn, faq,",
        "chase, dl_btn, faq,",
    )
    P.write_text(s, encoding="utf-8")
    print("rel_html added")
