#!/usr/bin/env python3
"""gen_pairs_batch.py - 全专题对照图批量生成(数据驱动)
PAIRS_BY_TOPIC: 每专题的 [{slug, good, bad}] — prompt都为英文(模型通用)
"""
import subprocess, json, pathlib, re, time, sys

ROOT = pathlib.Path(__file__).resolve().parent
def get_key():
    t = open("/Users/liheng/.hermes/config.yaml").read()
    return re.search(r"zai:[\s\S]*?api_key:\s*(\S+)", t).group(1)
KEY = get_key()

PAIRS_BY_TOPIC = {
  "hanfu-prompt-guide": [
    {"slug":"form","good":"a woman wearing a ming dynasty mamian skirt with golden brocade, cross-collar right lapel over left top, buyao hairpins, chinese classical garden, soft window light, cinematic still","bad":"a woman wearing hanfu dress, chinese garden, photo"},
    {"slug":"dynasty","good":"tang dynasty chest-high ruqun, flowing wide sleeves, ribbon sash, dancing pose, fabric floating in wind, golden hour backlight","bad":"tang dynasty costume, standing pose, photo"},
    {"slug":"snow","good":"hanfu woman in red cloak, snow on red walls, plum blossom, cold blue shadows, warm red dress contrast, cinematic still","bad":"hanfu woman, red dress, snow, photo"},
  ],
  "lighting-prompt-guide": [
    {"slug":"golden","good":"portrait of a young woman, golden hour, warm rim light, glowing backlight on hair, sun flare, long soft shadows","bad":"portrait of a young woman, nice lighting, photo"},
    {"slug":"window","good":"indoor portrait, soft window light from left, Rembrandt lighting, gentle light falloff, dust motes in air","bad":"indoor portrait, indoor lighting, photo"},
    {"slug":"blue","good":"city street at blue hour, lights just turned on, deep blue sky, neon signs starting to glow, cinematic","bad":"city street at night, neon lights, photo"},
  ],
  "fabric-texture-prompt": [
    {"slug":"velvet","good":"close-up of deep green velvet fabric with soft matte pile, light-absorbing folds, macro detail","bad":"close-up of green velvet fabric, macro"},
    {"slug":"satin","good":"satin qipao with liquid sheen, highlights flowing along the folds, soft studio light","bad":"satin qipao, studio photo"},
    {"slug":"tulle","good":"layered translucent tulle skirt, fabric floating in wind, layered transparency, backlight","bad":"tulle skirt, photo"},
  ],
  "nikki-art-reference": [
    {"slug":"concept","good":"fantasy character concept art, official art style, painterly rendering, ornate staff with glowing crystal, matte painting backdrop","bad":"fantasy character, pretty dress, digital art"},
    {"slug":"palette","good":"character design, deep blue and silver palette with subtle gold accents, asymmetric hemline, layered sleeves, concept art","bad":"character design, blue and silver dress, digital art"},
  ],
  "cyberpunk-vs-miami": [
    {"slug":"neon","good":"cyberpunk street at night, holographic ads, neon everywhere, dystopian, wet high-reflective street, steam","bad":"miami street at night, neon signs, wet street, photo"},
    {"slug":"miami","good":"miami beach at dusk, pink orange purple gradient sky, palm trees, pastel neon signs, resort vibe, cinematic","bad":"miami beach at night, neon everywhere, cyberpunk"},
  ],
  "jk-lolita-ai-guide": [
    {"slug":"petticoat","good":"sweet lolita with bell-shaped petticoat silhouette, pastel candy prints, big ribbon bow, cafe window light","bad":"lolita dress without petticoat, flat skirt, photo"},
    {"slug":"jk","good":"japanese school uniform, sailor collar, tartan plaid skirt, sakura street, afternoon light, youthful","bad":"school uniform girl, photo"},
  ],
  "wedding-dress-ai-guide": [
    {"slug":"lace","good":"lace wedding dress with floral embroidery, cathedral veil, garden ceremony, golden bokeh, romantic","bad":"wedding dress, garden, photo"},
    {"slug":"tullewind","good":"flowy tulle wedding dress, beach destination, wind-blown veil, sunset backlight, barefoot","bad":"wedding dress on beach, photo"},
  ],
  "photo-to-prompt-method": [
    {"slug":"layered","good":"a young asian woman in a camel wool coat over white straight-leg trousers, walking on a city street at dusk, looking back over her shoulder, warm street lamp light, street style photography, 35mm film grain","bad":"a woman in a coat on a street, photo"},
  ],
  "cny-hanfu-ai": [
    {"slug":"scene","good":"hanfu woman holding red lantern, soft glow on face, ancient chinese town, snow, red lanterns hanging, cobblestone street, cinematic still","bad":"chinese new year, red lanterns, hanfu woman, photo"},
    {"slug":"modern","good":"neo-chinese fashion editorial, mandarin collar blouse, red accent outfit, minimalist studio, high key","bad":"chinese new year fashion, red dress, photo"},
  ],
  "gta6-style-prompt": [],
};

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
            subprocess.run(["sips","-s","format","jpeg",out,"--out",str(p).replace(".png",".jpg")], capture_output=True)
            p.unlink() if p.suffix == ".png" and pathlib.Path(str(p).replace(".png",".jpg")).exists() else None
            return True
    except Exception as e:
        print("  fail:", str(e)[:60])
    return False

def main(only=None):
    total_ok = 0
    for slug, pairs in PAIRS_BY_TOPIC.items():
        if only and slug != only: continue
        if not pairs: continue
        OUT = ROOT/"public"/"topics"/("en-ex" if slug in ("hanfu-prompt-guide",) and False else slug)
        OUT.mkdir(parents=True, exist_ok=True)
        ok_n = 0
        for p in pairs:
            g = gen(p["good"], str(OUT/f"{p['slug']}-good.jpg"))
            time.sleep(2)
            b = gen(p["bad"], str(OUT/f"{p['slug']}-bad.jpg"))
            time.sleep(2)
            ok_n += (g and b)
            print(f"[{slug}/{p['slug']}] good={g} bad={b}")
        total_ok += ok_n
    print("TOTAL pairs ok:", total_ok)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
