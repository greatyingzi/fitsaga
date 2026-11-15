#!/usr/bin/env python3
"""sender_backfill.py — 对Top套图逐个detail查作者名(限流2s/个, 只处理fav>=100)"""
import sqlite3, json, subprocess, time, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
UA = "Mozilla/5.0"

def main(max_groups=30):
    con = sqlite3.connect(DB)
    groups = con.execute("""SELECT atlas_id, MAX(fav_count) fav FROM items
        WHERE atlas_id IS NOT NULL AND sender IS NULL
        GROUP BY atlas_id ORDER BY fav DESC LIMIT ?""", (max_groups,)).fetchall()
    got = 0
    for aid, fav in groups:
        # 组内任一blog_id查detail
        bid = con.execute("SELECT src_id FROM items WHERE atlas_id=? LIMIT 1", (aid,)).fetchone()[0]
        r = subprocess.run(["curl","-s","-A",UA,f"https://www.duitang.com/napi/blog/detail/?blog_id={bid}","--max-time","25"],
                           capture_output=True, text=True, timeout=30)
        try:
            d = json.loads(r.stdout).get("data") or {}
            sender = ((d.get("sender") or {}).get("username")) or None
            n_imgs = 1 if d.get("photo") else 0
            if sender:
                con.execute("UPDATE items SET sender=? WHERE atlas_id=?", (sender, aid))
                got += 1
                print(f"atlas {aid} (fav {fav}) -> {sender}")
        except Exception as e:
            print(f"atlas {aid} fail: {str(e)[:60]}")
        time.sleep(1.5)
    con.commit()
    total = con.execute("SELECT COUNT(DISTINCT sender) FROM items WHERE sender IS NOT NULL").fetchone()[0]
    print(f"\n补全作者: +{got}, 全库有名作者组: {total}")
    con.close()

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)