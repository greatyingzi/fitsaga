#!/usr/bin/env python3
"""gen_examples_en.py - EN hanfu topic comparison images (CogView English prompts)"""
import subprocess, json, pathlib, re, time

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "public" / "topics" / "gta6"   # 共享图目录不变; en图放 en-ex/
OUT2 = ROOT / "public" / "topics" / "en-ex"
OUT2.mkdir(parents=True, exist_ok=True)

def get_key():
    t = open("/Users/liheng/.hermes/config.yaml").read()
    return re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", t).group(1)

KEY = get_key()

PAIRS = [
    ("hanfu-form", 
     "a woman wearing a ming dynasty mamian skirt with golden brocade, cross-collar right lapel over left top, traditional chinese hairstyle with buyao hairpins, chinese classical garden, soft window light, cinematic still",
     "a woman wearing hanfu dress, chinese garden, photo"),
    ("hanfu-dynasty",
     "tang dynasty chest-high ruqun, flowing wide sleeves, ribbon sash, dancing pose, fabric floating in wind, golden hour backlight, cinematic",
     "tang dynasty costume, standing pose, photo"),
]

def gen(prompt, out):
    body = json.dumps({"model":"cogview-3-flash","prompt":prompt,"size":"1024x1024"})
    r = subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations",
        "-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json",
        "-d",body,"--max-time","70"], capture_output=True, text=True, timeout=80)
    try:
        url = json.loads(r.stdout)["data"][0]["url"]
        subprocess.run(["curl","-sL",url,"-o",out,"--max-time","60"], capture_output=True, timeout=70)
        p = pathlib.Path(out)
        if p.exists() and p.stat().st_size > 10000:
            # 格式统一转jpg
            subprocess.run(["sips","-s","format","jpeg",out,"--out",out.replace(".png",".jpg")], capture_output=True)
            return True
    except Exception as e:
        print("fail:", str(e)[:60])
    return False

results = []
for slug, good, bad in PAIRS:
    ok1 = gen(good, str(OUT2 / f"{slug}-good.png"))
    time.sleep(2)
    ok2 = gen(bad, str(OUT2 / f"{slug}-bad.png"))
    time.sleep(2)
    results.append({"slug":slug,"good":ok1,"bad":ok2})
    print(slug, ok1, ok2)
print(json.dumps(results))
