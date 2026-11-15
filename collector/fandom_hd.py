#!/usr/bin/env python3
"""fandom_hd.py — lovenikki.fandom 高清套装图采集
策略: allcategories acprefix 遍历套装名分类 → 每分类成员页(File:) → imageinfo 原图URL+尺寸
只收 width>=800 的图(高清标准), 入 suit_imgs 表(game='奇迹暖暖HD')
"""
import subprocess, json, urllib.parse, sqlite3, time, pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

def api(params):
    url = "https://lovenikki.fandom.com/api.php?" + urllib.parse.urlencode(params) + "&format=json"
    r = subprocess.run(["curl","-s","-A","Mozilla/5.0",url,"--max-time","30"], capture_output=True, text=True, timeout=40)
    try: return json.loads(r.stdout)
    except: return {}

def main(max_cats=200):
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT/"collector"/"_schema.sql", encoding="utf-8").read())
    # 套装名分类 = 含"Suits"的年度分类成员? 更好: 全部分类里以套装名命名的太多——
    # 用 Category:Costumes by Set? 先探: 拿"2019 Suits"类成员(=套装名页面)
    added_s = added_i = 0
    year_cats = ["2017 Suits","2018 Suits","2019 Suits","2020 Suits","2021 Suits","2022 Suits","2023 Suits","2024 Suits"]
    suit_pages = []
    for yc in year_cats:
        d = api({"action":"query","list":"categorymembers","cmtitle":f"Category:{yc}","cmlimit":500})
        ms = (d.get("query") or {}).get("categorymembers") or []
        suit_pages += [m["title"] for m in ms]
        time.sleep(0.6)
    suit_pages = list(dict.fromkeys(suit_pages))
    print("suit pages total:", len(suit_pages))
    # 每套装页取 images (批量50)
    for bi in range(0, len(suit_pages), 50):
        batch = suit_pages[bi:bi+50]
        d = api({"action":"query","titles":"|".join(batch),"prop":"images","imlimit":60})
        pending = []
        for pg in (d.get("query") or {}).get("pages",{}).values():
            name = (pg.get("title") or "").strip()
            if not name: continue
            for im in (pg.get("images") or []):
                t = im.get("title") or ""
                if not t.startswith("File:"): continue
                pending.append((name, t))
        # imageinfo批量
        for si in range(0, len(pending), 25):
            chunk = pending[si:si+25]
            d2 = api({"action":"query","titles":"|".join(c[1] for c in chunk),"prop":"imageinfo","iiprop":"url|size"})
            tmap = {}
            for pg in (d2.get("query") or {}).get("pages",{}).values():
                ii = (pg.get("imageinfo") or [{}])[0]
                if ii.get("url") and (ii.get("width") or 0) >= 800:
                    tmap[pg.get("title")] = (ii["url"], ii["width"], ii["height"])
            for name, t in chunk:
                hit = tmap.get(t)
                if not hit: continue
                u, w, h = hit
                cur = con.execute("INSERT OR IGNORE INTO suits (game,name,source) VALUES (?,?,?)",
                                  ("奇迹暖暖HD", name, "fandom:lovenikki"))
                added_s += cur.rowcount
                sid = con.execute("SELECT id FROM suits WHERE game=? AND name=?", ("奇迹暖暖HD", name)).fetchone()
                if sid:
                    icur = con.execute("INSERT OR IGNORE INTO suit_imgs (suit_id,img_url,kind,raw_name) VALUES (?,?,?,?)",
                                       (sid[0], u, f"hd{w}", t))
                    added_i += icur.rowcount
        print(f"batch {bi//50+1}/{(len(suit_pages)+49)//50}: suits+{added_s} imgs+{added_i}")
        time.sleep(1.2)
    con.commit()
    print("DB:", con.execute("SELECT COUNT(*) FROM suits WHERE game='奇迹暖暖HD'").fetchone(),
          con.execute("SELECT COUNT(*) FROM suit_imgs si JOIN suits s ON s.id=si.suit_id WHERE s.game='奇迹暖暖HD'").fetchone())
    con.close()

if __name__ == "__main__":
    main()
