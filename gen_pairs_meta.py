#!/usr/bin/env python3
import subprocess,json,pathlib,re
ROOT=pathlib.Path("/Users/liheng/work/self/fitsaga")
KEY=re.search(r"zai:[\s\S]*?api_key:\s*(\S+)",open("/Users/liheng/.hermes/config.yaml").read()).group(1)
def img(p,out):
 b=json.dumps({"model":"cogview-3-flash","prompt":p,"size":"1024x1024"})
 r=subprocess.run(["curl","-s","-X","POST","https://open.bigmodel.cn/api/paas/v4/images/generations","-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-d",b,"--max-time","70"],capture_output=True,text=True,timeout=80)
 try:
  u=json.loads(r.stdout)["data"][0]["url"]
  subprocess.run(["curl","-sL",u,"-o",out,"--max-time","60"],capture_output=True,timeout=70)
  return pathlib.Path(out).exists() and pathlib.Path(out).stat().st_size>10000
 except: return False
d=ROOT/"public/topics/how-we-research-reader-questions"; d.mkdir(parents=True,exist_ok=True)
a=img("research methodology diagram, proxy data to insight with uncertainty labels, honest data visualization, clean editorial", str(d/"style-good.jpg"))
b=img("fake precise dashboard with meaningless numbers, misleading data", str(d/"style-bad.jpg"))
print("meta article pairs:",a,b)
