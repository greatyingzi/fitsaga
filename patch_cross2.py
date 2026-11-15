#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_site.py")
s = P.read_text(encoding="utf-8")
# style_page 的 faq_html 后加专题导流
old = "  <div class=\"masonry\">{cards}</div>\n  {faq_html}\n</main>"
print("anchor:", old in s)
if old in s and "topics.html" not in s.split("def style_page")[1].split("def today_cards_html")[0]:
    # 在faq_html后加导流行(按风格匹配专题)
    new = (
        "  <div class=\"masonry\">{cards}</div>\n  {faq_html}\n"
        "  <p style=\"margin-top:1.5rem\"><a style=\"color:#c793ff\" href=\"/topics/hanfu-prompt-guide\">🎨 想用 AI 生成这种风格？看画法研究所的 prompt 方案 →</a></p>\n"
        "</main>"
    )
    s = s.replace(old, new, 1)
    P.write_text(s, encoding="utf-8")
    print("style cross-link added")
