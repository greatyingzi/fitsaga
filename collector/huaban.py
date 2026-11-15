#!/usr/bin/env python3
"""huaban.py — 花瓣SSR采集(免登录分类页, auth_key时效图→即时下载存本地data/huaban/)
策略: /favorite/<分类> SSR serverPinList 20pin/页 → 图带auth_key → curl即时下载原图 → 存本地
版权: 用户采集为主(中), 站内展示需下载缓存(auth_key过期567, 不能热链)
"""
import subprocess, json, sqlite3, re, time, pathlib, hashlib, urllib.parse, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
IMG_DIR = ROOT / "data" / "huaban"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

BOARDS = ["apparel", "beauty", "modeling_hair"]  # 女装搭配/美女/造型美妆

def fetch_board(board):
    url = f"https://huaban.com/favorite/{board}"
    r = subprocess.run(["curl","-s","-A",UA,"-H","Accept-Language: zh-CN","--compressed",url,"--max-time","30"], capture_output=True, text=True, timeout=40)
    h = r.stdout or ""
    m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    if not m:
        return None  # 命中EO挑战
    try:
        d = json.loads(m.group(1))
    except Exception:
        return None
    # 找serverPinList
    pins = []
    def walk(o, depth=0):
        if depth > 10 or len(pins) > 40: return
        if isinstance(o, dict):
            if "serverPinList" in o and isinstance(o["serverPinList"], list):
                pins.extend(o["serverPinList"])
                return
            for v in o.values(): walk(v, depth+1)
        elif isinstance(o, list):
            for v in o: walk(v, depth+1)
    walk(d.get("props",{}).get("pageProps",{}))
    return pins

def download(img_url, pin_id):
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg"
    fn = IMG_DIR / f"{pin_id}{ext}"
    if fn.exists(): return str(fn)
    r = subprocess.run(["curl","-s","-A",UA,"-H","Referer: https://huaban.com/","-L",img_url,"--max-time","30","-o",str(fn)], capture_output=True, text=True, timeout=40)
    ok = fn.exists() and fn.stat().st_size > 10000
    return str(fn) if ok else None

def main(per_board=20):
    con = sqlite3.connect(DB)
    total = 0
    for board in BOARDS:
        pins = fetch_board(board)
        if pins is None:
            print(f"[{board}] EO挑战页(需cookie复算), 跳过")
            continue
        got = 0
        for p in pins[:per_board]:
            pin_id = p.get("pin_id")
            f = p.get("file") or {}
            raw = f.get("url") or ""
            if not raw: continue
            img_url = "https://gd-hbimg-edge.huaban.com/" + raw if not raw.startswith("http") else raw
            local = download(img_url, pin_id)
            if not local: continue
            origin = f"https://huaban.com/pins/{pin_id}"
            board_info = p.get("board") or {}
            user = board_info.get("user",{}).get("username") if isinstance(board_info.get("user"), dict) else None
            con.execute("""INSERT OR IGNORE INTO items
                (source,src_id,img_url,origin_url,author,license,w,h,tags,aigc_label,raw)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                ("huaban", str(pin_id), local, origin, user, "download-cache",
                 f.get("width"), f.get("height"),
                 json.dumps({"kw": board, "board": board_info.get("title"), "local": True}, ensure_ascii=False),
                 None, json.dumps(p, ensure_ascii=False)[:3000]))
            got += con.total_changes if False else 0
        con.commit()
        n = con.execute("SELECT COUNT(*) FROM items WHERE source='huaban' AND json_extract(tags,'$.kw')=?", (board,)).fetchone()[0]
        total += n
        print(f"[{board}] pins {len(pins)}, in-db {n}")
        time.sleep(2.0)
    print("huaban total:", con.execute("SELECT COUNT(*) FROM items WHERE source='huaban'").fetchone())
    con.close()

if __name__ == "__main__":
    main()
