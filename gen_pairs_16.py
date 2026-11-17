#!/usr/bin/env python3
import subprocess, json, pathlib, re, time
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga"); OUT=ROOT/"public/topics"
KEY = re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", open("/Users/liheng/.hermes/config.yaml").read()).group(1)
PAIRS = {
 "cinematic-lighting-types":("portrait with rembrandt lighting setup, triangle of light on cheek, soft window light, cinematic, moody", "portrait with flat harsh lighting, photo"),
 "hanfu-color-meanings":("deep vermilion red hanfu with golden brocade, festive chinese new year, traditional hairpin, warm lantern light", "red chinese dress, photo"),
 "mamian-skirt-plus-size-men":("plus-size woman wearing ming dynasty mamian skirt, high-waisted straight panels, fitted top, confident posture, natural light", "loose chinese skirt, photo"),
 "love-nikki-dress-up-guide":("elegant ancient chinese costume concept art, flowing hanfu silhouette, muted palette, painterly, game art", "pretty dress game screenshot"),
 "wedding-guest-lace-outfit":("wedding guest, dusty rose lace midi dress, garden ceremony, soft natural light, elegant understated", "white lace wedding dress, bride photo"),
 "short-drama-visual-style":("dramatic close-up portrait, high contrast lighting, bokeh city lights, low angle, vertical 9 16, emotional expression", "flat selfie photo"),
 "midnight-cinema-aesthetic":("midnight cinema, empty street, neon marquee, wet reflections, blue hour, warm interior glow, cinematic still, film grain", "empty street at night, photo"),
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
