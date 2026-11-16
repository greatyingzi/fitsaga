#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/collector/huaban.py")
s = P.read_text(encoding="utf-8")
# fetch_board 加 cookie 支持: 读 data/huaban_cookie.txt(格式: name=value; name=value)
old = '    r = subprocess.run(["curl","-s","-A",UA,"-H","Accept-Language: zh-CN","--compressed",url,"--max-time","30"], capture_output=True, text=True, timeout=40)'
new = (
    "    cookie_file = ROOT / " + chr(34) + "data" + chr(34) + " / " + chr(34) + "huaban_cookie.txt" + chr(34) + chr(10)
    + "    extra = []" + chr(10)
    + "    if cookie_file.exists():" + chr(10)
    + "        ck = cookie_file.read_text(encoding=" + chr(34) + "utf-8" + chr(34) + ").strip()" + chr(10)
    + "        if ck: extra = [" + chr(34) + "-H" + chr(34) + ", " + chr(34) + "Cookie: " + chr(34) + " + ck]" + chr(10)
    + "    r = subprocess.run([" + chr(34) + "curl" + chr(34) + "," + chr(34) + "-s" + chr(34) + "," + chr(34) + "-A" + chr(34) + ",UA," + chr(34) + "-H" + chr(34) + "," + chr(34) + "Accept-Language: zh-CN" + chr(34) + "] + extra + [" + chr(34) + "--compressed" + chr(34) + ", url," + chr(34) + "--max-time" + chr(34) + "," + chr(34) + "30" + chr(34) + "], capture_output=True, text=True, timeout=40)"
)
if old in s:
    s = s.replace(old, new, 1)
    P.write_text(s, encoding="utf-8")
    print("cookie support added")
else:
    print("anchor miss")
