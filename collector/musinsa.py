#!/usr/bin/env python3
"""FitSaga collector: musinsa.com/snap (SSR __NEXT_DATA__, 36条/run)
策略: sort=NEWEST+POPULAR 各抓一次, 按 snap id 去重累积。定时跑=持续增量。
用法: python3 musinsa.py [--runs 1]
入库: SQLite data/fitsaga.db 表 items
"""
import json, sqlite3, subprocess, sys, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

SCHEMA = open(ROOT / "collector" / "_schema.sql", encoding="utf-8").read()

SORTS = ["NEWEST", "POPULAR"]

def fetch_page(sort: str):
    url = f"https://www.musinsa.com/snap/main/recommend?sort={sort}"
    r = subprocess.run(["curl", "-s", "-A", UA, "-H", "Accept-Language: ko-KR,ko;q=0.9,en;q=0.8",
                        url, "--max-time", "30"], capture_output=True, text=True, timeout=40)
    h = r.stdout
    m = None
    import re
    m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    if not m:
        return []
    try:
        d = json.loads(m.group(1))
    except Exception:
        return []
    qs = d.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get("queries", [])
    snaps = {}
    for q in qs:
        sd = q.get("state", {}).get("data", {})
        st = json.dumps(sd, ensure_ascii=False)
        if '"medias"' not in st:
            continue
        for pg in (sd.get("pages") or []):
            for blk in (pg.get("data", {}).get("list") or []):
                for cont in (blk.get("contents") or []):
                    ct = cont.get("contentType") or ""
                    if not ct.endswith("SNAP"):
                        continue
                    medias = [mm.get("path") for mm in (cont.get("medias") or []) if mm.get("type") == "IMAGE"]
                    snaps[str(cont.get("id"))] = {
                        "id": str(cont.get("id")),
                        "thumbs": medias,
                        "link": cont.get("linkUrl"),
                        "user": (cont.get("createdBy") or {}).get("nickname") or (cont.get("createdBy") or {}).get("id"),
                    }
    return list(snaps.values())

def init_db():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    return con

def ingest(con, sort: str):
    items = fetch_page(sort)
    rows = []
    for it in items:
        for i, img in enumerate(it["thumbs"]):
            rows.append((
                "musinsa", f"{it['id']}#{i}", img,
                "https://www.musinsa.com" + (it.get("link") or f"/snap/{it['id']}"),
                it.get("user"), "hotlink-attribution", None, None,
                json.dumps({"sort": sort, "snap_id": it["id"], "korean": True}, ensure_ascii=False),
                None, json.dumps(it, ensure_ascii=False)[:4000],
            ))
    before = con.total_changes
    con.executemany(
        "INSERT OR IGNORE INTO items (source,src_id,img_url,origin_url,author,license,w,h,tags,aigc_label,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        rows)
    print(f"[{sort}] snaps {len(items)}, imgs +{con.total_changes - before}")

def main():
    runs = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 1
    con = init_db()
    for r in range(runs):
        for s in SORTS:
            ingest(con, s)
        if r < runs - 1:
            time.sleep(8)
    con.commit()
    print("DB total:", con.execute("SELECT source,COUNT(*) FROM items GROUP BY source").fetchall())
    con.close()

if __name__ == "__main__":
    main()
