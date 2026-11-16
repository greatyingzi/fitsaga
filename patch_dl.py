#!/usr/bin/env python3
import pathlib
# 1) gen_topics.py: 专题页 chase 区后加下载按钮(有zip的专题)
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
s = P.read_text(encoding="utf-8")
D = chr(34); S = chr(39)
anchor = "        chase = "
add_code = (
    "        dl_btn = " + chr(34) + chr(34) + chr(10)
    + "        try:" + chr(10)
    + "            _mf = json.loads((PUB / " + D + "downloads/manifest.json" + D + ").read_text(encoding=" + D + "utf-8" + D + "))" + chr(10)
    + "            for _m in _mf:" + chr(10)
    + "                if _m[" + D + "slug" + D + "] == t[" + D + "slug" + D + "]:" + chr(10)
    + "                    dl_btn = " + S + "<p style=\"margin-top:1rem\"><a style=\"background:linear-gradient(135deg,#ff7eb3,#a855f7);color:#fff;padding:.7rem 1.2rem;border-radius:10px;text-decoration:none;font-weight:700\" href=\"" + S + " + _m[" + D + "zip" + D + "] + " + S + "\" download>⬇ 下载本专题参考图包（" + S + " + str(_m[" + D + "count" + D + "]) + " + S + " 张）</a></p>" + S + chr(10)
    + "                    break" + chr(10)
    + "        except Exception:" + chr(10)
    + "            pass" + chr(10)
)
if "dl_btn" not in s:
    lines = s.split(chr(10))
    for i, l in enumerate(lines):
        if l.strip().startswith("chase = "):
            lines[i:i] = [x.replace(chr(92)+chr(34), D) for x in add_code.split(chr(10))]
            # chase渲染行后加 dl_btn 到 parts
            for j in range(i, len(lines)):
                if "body, ex_html, chase, faq," in lines[j]:
                    lines[j] = lines[j].replace("chase,", "chase, dl_btn,")
                    break
            P.write_text(chr(10).join(lines), encoding="utf-8")
            print("dl button added")
            break
else:
    print("already")
