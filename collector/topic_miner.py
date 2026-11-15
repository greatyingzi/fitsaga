#!/usr/bin/env python3
"""topic_miner.py — suggest选题挖掘: 种子词→百度/Google suggest递归→查重→topics入池"""
import json, sqlite3, subprocess, sys, time, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

SEEDS = ["老钱风","马面裙","小个子穿搭","梨形身材","白衬衫","纯欲风","汉服日常","JK格裙",
         "通勤穿搭","约会穿搭","多巴胺穿搭","美拉德穿搭","新中式","羽绒服","针织衫",
         "法式穿搭","静奢风","千禧辣妹","旗袍日常","汉元素"]

def b_sug(q):
    r = subprocess.run(["curl","-s",f"https://www.baidu.com/sugrec?prod=pc&wd={urllib.parse.quote(q)}","--max-time","15"], capture_output=True, text=True, timeout=20)
    try: return [x["q"] for x in json.loads(r.stdout).get("g",[])]
    except: return []

def g_sug(q):
    r = subprocess.run(["curl","-s",f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(q)}&hl=zh-CN","--max-time","15"], capture_output=True, text=True, timeout=20)
    try: return json.loads(r.stdout)[1]
    except: return []

def classify(q):
    """按句式自动归类型"""
    if any(k in q for k in ["vs","和 ","与 ","区别","哪个好","对比"]): return "B"
    if any(k in q for k in ["一周","七日","7天","周穿","方案","日历"]): return "C"
    return "A"

def main():
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT/"collector"/"_schema.sql", encoding="utf-8").read())
    added = skipped = 0
    for seed in SEEDS:
        qs = set(b_sug(seed) + g_sug(seed))
        # 二层: 取前3子词再挖
        for w in list(qs)[:3]:
            qs |= set(b_sug(w)) | set(g_sug(w))
            time.sleep(0.3)
        for q in qs:
            q = q.strip()
            if len(q) < 4 or len(q) > 24: continue
            t = classify(q)
            cur = con.execute("INSERT OR IGNORE INTO topics (keyword,type,evidence,source) VALUES (?,?,?,?)",
                              (q, t, f"seed:{seed}", "baidu_goo_sug"))
            added += cur.rowcount
            if cur.rowcount == 0: skipped += 1
        time.sleep(0.8)
    con.commit()
    print(f"入池: +{added} (重复跳过 {skipped})")
    print("按类型:", con.execute("SELECT type,COUNT(*) FROM topics GROUP BY type").fetchall())
    print("状态:", con.execute("SELECT status,COUNT(*) FROM topics GROUP BY status").fetchall())
    # 样例
    print("\n选题样例(A类前10):")
    for (kw,) in con.execute("SELECT keyword FROM topics WHERE type='A' AND status='idea' LIMIT 10"):
        print(" -", kw)
    con.close()

if __name__ == "__main__":
    main()
