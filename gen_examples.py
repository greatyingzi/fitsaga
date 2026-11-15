#!/usr/bin/env python3
"""gen_examples.py - GTA6专题正反例对照图生成(智谱CogView)"""
import subprocess, json, pathlib, re, time

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "public" / "topics" / "gta6"
OUT.mkdir(parents=True, exist_ok=True)

def get_key():
    t = open("/Users/liheng/.hermes/config.yaml").read()
    return re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", t).group(1)

KEY = get_key()

PAIRS = [
    # (slug, 正例prompt, 反例prompt, 说明)
    ("sky", "Miami Beach at dusk, pink orange purple gradient sky, natural sky gradient, palm trees, ocean, cinematic still",
     "Miami Beach at dusk, sunset, palm trees, ocean, photo"),
    ("haze", "Miami coastal highway at golden hour, humid haze, atmospheric perspective, neon glow reflecting on wet streets, art deco buildings, cinematic still, film grain",
     "Miami coastal highway at golden hour, art deco buildings, cinematic"),
    ("motion", "a young woman in hawaiian shirt leaning on a muscle car, candid pose, mid-motion, Miami dusk, pink orange sky, cinematic still",
     "a young woman in hawaiian shirt standing pose, Miami dusk, cinematic still"),
]

def gen(prompt, out):
    body = json.dumps({"model":"cogview-3-flash","prompt":prompt,"size":"1024x1024"})
    r = subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations",
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json",
        "-d",body,"--max-time","70"], capture_output=True, text=True, timeout=80)
    try:
        url = json.loads(r.stdout)["data"][0]["url"]
        d = subprocess.run(["curl","-sL",url,"-o",out,"--max-time","60"], capture_output=True, text=True, timeout=70)
        return pathlib.Path(out).stat().st_size > 10000
    except Exception as e:
        print("gen fail:", str(e)[:80], r.stdout[:100])
        return False

results = []
for slug, good, bad in PAIRS:
    ok1 = gen(good, str(OUT / f"{slug}-good.jpg"))
    time.sleep(2)
    ok2 = gen(bad, str(OUT / f"{slug}-bad.jpg"))
    time.sleep(2)
    results.append({"slug":slug, "good_ok":ok1, "bad_ok":ok2})
    print(slug, "good:", ok1, "bad:", ok2)
print(json.dumps(results))
