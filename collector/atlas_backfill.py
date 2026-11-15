#!/usr/bin/env python3
"""atlas_backfill.py — 把 items 表里同 atlas_id 的图聚合成套图组(更新 sender/fav), 并输出套图统计"""
import sqlite3, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

def main():
    con = sqlite3.connect(DB)
    # 用 raw 里的 atlas_id 回填新列
    con.execute("""UPDATE items SET atlas_id = json_extract(raw,'$.atlas_id')
                   WHERE atlas_id IS NULL AND json_extract(raw,'$.atlas_id') IS NOT NULL""")
    con.execute("""UPDATE items SET fav_count = COALESCE(json_extract(raw,'$.favorite_count'),0)
                   WHERE fav_count = 0 AND json_extract(raw,'$.favorite_count') IS NOT NULL""")
    con.execute("""UPDATE items SET sender = json_extract(raw,'$.sender.name')
                   WHERE sender IS NULL AND json_extract(raw,'$.sender.name') IS NOT NULL""")
    con.commit()
    stats = con.execute("""SELECT atlas_id, COUNT(*) n, MAX(fav_count) fav, MAX(sender) snd
                           FROM items WHERE atlas_id IS NOT NULL GROUP BY atlas_id
                           HAVING n >= 2 ORDER BY fav DESC LIMIT 10""").fetchall()
    print("多图套图组(Top10 by fav):")
    for aid, n, fav, snd in stats:
        print(f"  atlas {aid}: {n}张 收藏{fav} 作者{snd}")
    total_groups = con.execute("SELECT COUNT(DISTINCT atlas_id) FROM items WHERE atlas_id IS NOT NULL").fetchone()[0]
    multi = con.execute("""SELECT COUNT(*) FROM (SELECT atlas_id FROM items WHERE atlas_id IS NOT NULL GROUP BY atlas_id HAVING COUNT(*)>=2)""").fetchone()[0]
    single_named = con.execute("SELECT COUNT(*) FROM items WHERE sender IS NOT NULL").fetchone()[0]
    print(f"\n总atlas组: {total_groups} | 多图组: {multi} | 有作者名: {single_named}")
    con.close()

if __name__ == "__main__":
    main()
