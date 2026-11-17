#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS={
 "why-ai-fashion-looks-plastic":("portrait with directional light, skin texture with subsurface scattering, fabric with drape, atmospheric haze, photorealistic editorial", "portrait with flat uniform light, plastic skin, no shadows, synthetic look"),
 "seasonal-color-engine":("color palette infographic, four seasonal color quadrants, cream oatmeal rust forest misty blue sapphire swatches, elegant design", "random color splashes, chaotic"),
 "why-saving-more-is-worse":("minimal curated outfit board, three selected reference images, clean annotated notes, organized moodboard", "hundreds of scattered saved images, cluttered overwhelming collage"),
 "ai-fashion-copyright-map":("clean risk level diagram, four tiers, green to red gradient, fashion icons, editorial infographic design", "confusing messy legal documents pile"),
 "prompt-anti-patterns":("clean prompt text with precise descriptors highlighted, minimal editorial typography, dark elegant design", "word cloud of hype words masterpiece 8k best quality, messy"),
}
def gen_img(p,out):
    b=json.dumps({"model":"cogview-3-flash","prompt":p,"size":"1024x1024"})
    r=subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations","-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-d",b,"--max-time","70"],capture_output=True,text=True,timeout=80)
    try:
        u=json.loads(r.stdout)["data"][0]["url"]
        subprocess.run(["curl","-sL",u,"-o",out,"--max-time","60"],capture_output=True,timeout=70)
        return pathlib.Path(out).exists() and pathlib.Path(out).stat().st_size>10000
    except: return False
ok=0
for slug,(g,b) in PAIRS.items():
    d=OUT/slug; d.mkdir(parents=True,exist_ok=True)
    a=gen_img(g,str(d/"style-good.jpg")); time.sleep(2)
    c=gen_img(b,str(d/"style-bad.jpg")); time.sleep(2)
    ok+=(a and c); print(slug,a,c)
print("TOTAL:",ok)
