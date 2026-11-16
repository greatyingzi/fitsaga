#!/usr/bin/env python3
"""gen_pairs_en_new.py - 三新EN专题对照图"""
import subprocess, json, pathlib, re, time

ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
OUT = ROOT / "public" / "topics"
def get_key():
    t = open("/Users/liheng/.hermes/config.yaml").read()
    return re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", t).group(1)
KEY = get_key()

PAIRS = {
  "infinity-nikki-outfit-ideas": [
    {"slug":"palette","good":"fantasy dress design, deep blue and silver palette with subtle gold accents, asymmetric hemline, layered sleeves, concept art, painterly rendering","bad":"pretty blue dress, digital art"},
    {"slug":"silhouette","good":"character outfit design, bell-shaped layered skirt, dramatic shoulder silhouette, silver embroidery, official game art style","bad":"fantasy dress, long skirt, art"},
  ],
  "image-prompt-techniques": [
    {"slug":"sixlayer","good":"a young asian woman in a camel wool coat over white straight-leg trousers, walking on a city street at dusk, looking back over her shoulder, warm street lamp light, street style photography, 35mm film grain","bad":"a woman in a coat on a street, photo"},
    {"slug":"fabric-layer","good":"close-up fashion detail, chunky knit sweater with visible stitch texture, soft window light, cozy","bad":"sweater close-up, photo"},
  ],
  "game-costume-design-ai": [
    {"slug":"concept","good":"fantasy character costume concept sheet, ornate armor with flowing sash, gold and deep teal palette, painterly concept art, official art style","bad":"fantasy character armor, cool design, digital art"},
    {"slug":"materials","good":"costume detail study, velvet and brushed metal contrast, embroidered trim, macro concept art rendering","bad":"armor detail, shiny metal, art"},
  ],
}

def gen(prompt, out):
    body = json.dumps({"model":"cogview-3-flash","prompt":prompt,"size":"1024x1024"})
    r = subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations",
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json",
        "-d",body,"--max-time","70"], capture_output=True, text=True, timeout=80)
    try:
        url = json.loads(r.stdout)["data"][0]["url"]
        subprocess.run(["curl","-sL",url,"-o",out,"--max-time","60"], capture_output=True, timeout=70)
        p = pathlib.Path(out)
        return p.exists() and p.stat().st_size > 10000
    except Exception as e:
        print("  fail:", str(e)[:60])
        return False

ok = 0
for slug, pairs in PAIRS.items():
    d = OUT / slug
    d.mkdir(parents=True, exist_ok=True)
    for p in pairs:
        g = gen(p["good"], str(d/f"{p['slug']}-good.jpg"))
        time.sleep(2)
        b = gen(p["bad"], str(d/f"{p['slug']}-bad.jpg"))
        time.sleep(2)
        ok += (g and b)
        print(f"[{slug}/{p['slug']}] {g} {b}")
print("TOTAL:", ok)
