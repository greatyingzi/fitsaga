#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS={
 "the-68-experiments":("laboratory ledger, 68 comparison experiments grid, data table with checkmarks and crosses, clean scientific infographic", "single random experiment photo"),
 "what-4547-images-say":("power law distribution chart, few high bars many low bars, clean data visualization, elegant dark theme", "flat uniform bar chart, no pattern"),
 "why-1587-suits":("structured database visualization, 1587 game outfits as organized grid with tags, data asset concept, clean design", "unstructured pile of game screenshots"),
 "negative-results-matter":("scientific report with crossed out words masterpiece 8k, negative results highlighted, clean editorial design", "glossy success-only poster"),
 "content-as-structure":("few images transformed into structured frameworks, flow diagram, elegant editorial infographic", "large pile of unprocessed images"),
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
