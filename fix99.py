#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_topics.py")
lines = P.read_text(encoding="utf-8").split(chr(10))
D = chr(34); S = chr(39)
out = []
done = False
for l in lines:
    if not done and "search.js" in l and "defer" in l and not l.strip().endswith(","):
        # 悬挂行: 与前面的行合并重写
        # 找out里最后一个含lightbox的行, 直接重写两个script行为合法
        out.append("                 " + S + "<script src=" + D + "/search.js" + D + " defer></script>" + S + ",")
        done = True
        continue
    out.append(l)
# 找lightbox行, 若其末尾没逗号(说明字符串断开), 修
for i, l in enumerate(out):
    if "lightbox.js" in l and l.rstrip().endswith("</script>"):
        out[i] = l.rstrip() + S + ","
        print("lightbox line fixed at", i+1)
        break
P.write_text(chr(10).join(out), encoding="utf-8")
print("done", done)
