#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS={
 "why-mamian-went-global":("mamian skirt modern street style, horse-face skirt with knit top, diverse body types, cross-cultural fashion editorial", "traditional chinese costume, museum display"),
 "the-economy-of-ai-reference-images":("organized research desk, annotated fashion reference images with notes, structured knowledge board, editorial design", "random pile of photos, messy"),
 "visual-trends-half-life":("timeline infographic of fashion trends, three phases short medium long cycle, clean data visualization", "chaotic colorful trend board"),
 "the-readability-paradox":("single deep red dress, minimal clean composition, one model, editorial fashion photo, instantly readable", "overloaded busy fashion collage with many outfits"),
 "commerce-of-fictional-places":("vice city miami 1980s neon skyline, palm trees, pink teal palette, fictional game world, cinematic", "ordinary city street photo"),
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
