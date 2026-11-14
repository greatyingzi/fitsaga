#!/usr/bin/env python3
"""FitSaga collector: ZARA woman 官方大片 (ajax JSON, 版权低)
多品类页: new-in / dresses / coats / knitwear / jeans / shoes...
每页 ~20 商品 × 2-6 图
"""
import json, re, sqlite3, subprocess, sys, time, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# 女装品类页 (zara.com/jp/ja)
PAGES = [f"woman-new-in-l1180.html?page={p}" for p in range(1, 11)]

def fetch(url):
    r = subprocess.run(["curl","-s","-A",UA,"-H","Accept-Language: ja","--compressed",url,"--max-time","40"],
                       capture_output=True, text=True, timeout=50)
    try:
        return json.loads(r.stdout)
    except Exception:
        return None

def collect(con, pages, per_page_cap=150):
    s_add = i_add = 0
    for pg in PAGES[:pages]:
        sep = '&' if '?' in pg else '?'
        url = f"https://www.zara.com/jp/ja/{pg}{sep}ajax=true"
        d = fetch(url)
        if not d:
            print(f"[{pg}] fetch fail"); continue
        s = json.dumps(d, ensure_ascii=False)
        # 商品块: name + commercialComponents? 直接抓jpg+商品名配对: 用detail.colors[].name
        # 简化: 抓全部unique jpg, 商品名从 name 字段附近不好配 → 用页面级 slug 作为"系列"
        jpgs = re.findall(r'https://static\.zara\.net/assets/public/[^"\\\s]+?\.(?:jpg|jpeg)', s)
        jpgs = [u.rstrip('\\').split('?ts=')[0] for u in jpgs]
        jpgs = list(dict.fromkeys(jpgs))
        jpgs = [u for u in jpgs if '/poster/' not in u][:per_page_cap]
        m = re.search(r'page=(\d+)', pg)
        cat = f"new-in-p{m.group(1)}" if m else pg
        label = "ZARA " + cat.upper()
        sid_row = con.execute("SELECT id FROM suits WHERE game=? AND name=?", ("ZARA大片", label)).fetchone()
        if sid_row:
            sid = sid_row[0]
        else:
            cur = con.execute("INSERT INTO suits (game,name,source) VALUES (?,?,?)", ("ZARA大片", label, "zara"))
            sid = cur.lastrowid; s_add += 1
        for i, u in enumerate(jpgs):
            u_clean = u.split('?ts=')[0] + ('?ts=' + re.search(r'ts=(\d+)', u).group(1) if re.search(r'ts=(\d+)', u) else '')
            icur = con.execute("INSERT OR IGNORE INTO suit_imgs (suit_id,img_url,kind,raw_name) VALUES (?,?,?,?)",
                               (sid, u_clean, f"look{i+1}", f"{cat}-{i+1}"))
            i_add += icur.rowcount
        print(f"[{pg}] imgs {len(jpgs)}")
        time.sleep(2.0)
    return s_add, i_add

def main():
    pages = int(sys.argv[sys.argv.index("--pages") + 1]) if "--pages" in sys.argv else 4
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT / "collector" / "_schema.sql", encoding="utf-8").read())
    s, i = collect(con, pages)
    con.commit()
    print(f"added suits+{s} imgs+{i}")
    print("DB suit_imgs:", con.execute("SELECT COUNT(*) FROM suit_imgs").fetchone())
    con.close()

if __name__ == "__main__":
    main()