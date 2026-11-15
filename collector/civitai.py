#!/usr/bin/env python3
"""civitai.py — AI生成图采集(civitai公开API, 高清, 免登录)
tag维度: fashion/hanfu/portrait/anime-girl/wedding-dress...
nsfw=Soft 控尺度; 存 items 表(source='civitai', aigc_label=1)
"""
import subprocess, json, sqlite3, sys, time, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

TAGS = ["fashion", "hanfu", "portrait", "dress", "wedding dress", "gown", "kimono", "qipao"]

def fetch(tag, limit=10):
    url = f"https://civitai.com/api/v1/models?limit={limit}&sort=Highest%20Rated&tag={urllib.parse.quote(tag)}"
    r = subprocess.run(["curl","-s",url,"--max-time","35"], capture_output=True, text=True, timeout=45)
    try: return json.loads(r.stdout).get("items") or []
    except: return []

def main(pages_per_tag=1):
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT/"collector"/"_schema.sql", encoding="utf-8").read())
    total = 0
    for tag in TAGS:
        models = fetch(tag)
        rows = []
        for m in models:
            mname = m.get("name") or ""
            all_imgs = []
            for v in (m.get("modelVersions") or []):
                all_imgs += (v.get("images") or [])
            for img in all_imgs[:8]:
                u = img.get("url") or ""
                if not u: continue
                iid = (u.split("/")[-1] if u else "")[:40]
                origin = f"https://civitai.com/models/{m.get('id')}"
                rows.append((
                    "civitai", f"{m.get('id')}-{iid[-20:]}", u, origin,
                    mname, "civitai-model-license",
                    img.get("width"), img.get("height"),
                    json.dumps({"tag": tag, "model": mname, "modelType": m.get("type"),
                                "aigc": True, "prompt": (img.get("meta") or {}).get("prompt","")[:300]},
                               ensure_ascii=False),
                    1, json.dumps(img, ensure_ascii=False)[:4000],
                ))
        before = con.total_changes
        con.executemany("INSERT OR IGNORE INTO items (source,src_id,img_url,origin_url,author,license,w,h,tags,aigc_label,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
        total += con.total_changes - before
        print(f"[{tag}] +{con.total_changes - before} (models {len(models)})")
        time.sleep(1.2)
    con.commit()
    print("civitai total:", con.execute("SELECT COUNT(*) FROM items WHERE source='civitai'").fetchone())
    con.close()

if __name__ == "__main__":
    main()