#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS={
 "east-west-collar":("three collar types comparison diagram, cross-collar V-neck mandarin collar, cultural body concepts, elegant editorial infographic", "single generic collar photo"),
 "fashion-ai-timeline":("timeline infographic 2022 to 2026, three phases of prompt philosophy, clean data visualization, dark elegant", "random dated screenshots, messy"),
 "what-readers-save":("analytics dashboard concept, download patterns and search queries, clean abstract data visualization, editorial", "raw log files, unreadable"),
 "design-across-cultures":("world map with three fashion vocabularies connected, translation diagram, clean editorial design", "confused mixed styles"),
 "from-tips-to-science":("scientific notebook with A B tests, checklist and criteria, clean minimal editorial design", "pile of unverified tips"),
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
