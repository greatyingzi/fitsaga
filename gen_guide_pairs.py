#!/usr/bin/env python3
"""gen_guide_pairs.py - 决策文对照图(6篇×1组)"""
import subprocess, json, pathlib, re, time
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
OUT = ROOT / "public" / "guide-img"
OUT.mkdir(parents=True, exist_ok=True)
KEY = re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", open("/Users/liheng/.hermes/config.yaml").read()).group(1)

PAIRS = {
  "jingshefeng-zenmechuan": ("quiet luxury outfit, oatmeal camel coat over silk satin skirt, monochrome layered tones, soft diffused daylight, editorial","quiet luxury outfit, beige dress, studio photo"),
  "zhenzhishan-xuankuan": ("oversized knit sweater V-neck with visible stitch texture, straight-leg trousers, soft window light, flattering silhouette","knit sweater, tight fit, photo"),
  "duobapei-secaigongshi": ("dopamine outfit, 631 color ratio, cream coat 60 percent, soft blue trousers 30 percent, pink bag accent 10 percent, street style","colorful outfit, many bright colors, photo"),
  "jkzhifu-ruquan": ("japanese school uniform, sailor collar seifuku, tartan pleated skirt, sakura street, afternoon light","school uniform costume, photo"),
  "tianmei-bianjie": ("sweet style outfit, pastel cardigan with straight jeans, one bow accessory only, balanced not childish, natural light","sweet lolita puffy dress with bows and lace overload, photo"),
  "y2k-huichao": ("y2k fashion, one metallic cami top with modern wide-leg jeans, chunky sneakers, 2000s nostalgia modernized, street style","full y2k shiny low-rise rhinestone outfit, costume"),
}
def gen_img(prompt, out):
    body = json.dumps({"model":"cogview-3-flash","prompt":prompt,"size":"1024x1024"})
    r = subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations",
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-d",body,"--max-time","70"],
        capture_output=True, text=True, timeout=80)
    try:
        url = json.loads(r.stdout)["data"][0]["url"]
        subprocess.run(["curl","-sL",url,"-o",out,"--max-time","60"], capture_output=True, timeout=70)
        return pathlib.Path(out).exists() and pathlib.Path(out).stat().st_size > 10000
    except Exception: return False

ok = 0
for slug, (good, bad) in PAIRS.items():
    g = gen_img(good, str(OUT/f"{slug}-good.jpg")); time.sleep(2)
    b = gen_img(bad, str(OUT/f"{slug}-bad.jpg")); time.sleep(2)
    ok += (g and b); print(slug, g, b)
print("TOTAL:", ok)
