#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS={
 "ai-fashion-failure-atlas":("fashion photo with visible mistake, wrong collar direction, plastic fabric, flat lighting, illustration of common AI errors", "clean fashion editorial photo"),
 "fashion-ai-prompt-grammar":("infographic style, layered fashion prompt words connected by lines, elegant typography, dark background, editorial design", "random words scattered, messy"),
 "nikki-design-language":("game costume design sheet, celestial theme, exaggerated silhouette, layered tulle and metal, star palette, concept art, official art style", "plain dress sketch"),
 "the-anatomy-of-a-viral-fashion-prompt":("one dominant deep red dress, clean silhouette, single emotional expression, editorial photography, instantly readable composition", "busy colorful outfit with many competing elements"),
 "chinese-garment-taxonomy-en":("grid of twelve chinese garment forms illustrated, mamian skirt, ruqun, qipao, clean museum style reference sheet, labeled", "random costume collage"),
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
