#!/usr/bin/env python3
"""FitSaga collector: duitang.com (开放 napi, 无需登录)
用法: python3 duitang.py [--kws 穿搭,汉服,...] [--limit 20] [--pages 3]
入库: SQLite data/fitsaga.db 表 items (按 img_url 去重)
"""
import json, sqlite3, subprocess, sys, time, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  src_id TEXT,
  img_url TEXT UNIQUE,
  origin_url TEXT,
  author TEXT,
  license TEXT,
  w INTEGER, h INTEGER,
  tags TEXT,
  aigc_label INTEGER,
  raw TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_tags ON items(tags);
"""

DEFAULT_KWS = [
    # 核心大词
    "穿搭", "每日穿搭", "OOTD", "今日穿搭", "穿搭分享", "日常穿搭", "秋冬穿搭", "一周穿搭",
    # 风格
    "甜美穿搭", "初恋感", "奶系穿搭", "甜妹穿搭", "辣妹穿搭", "纯欲风", "老钱风", "千金风",
    "氛围感穿搭", "法式穿搭", "极简穿搭", "高级感穿搭", "多巴胺穿搭", "美拉德穿搭", "Y2K穿搭",
    "美式复古", "知识分子风", "静奢风",
    # 品类
    "连衣裙", "秋冬大衣", "羽绒服穿搭", "西装穿搭", "裙装搭配", "卫衣穿搭", "针织衫",
    # 圈层
    "汉服", "汉服日常", "马面裙", "新中式", "JK制服", "格裙", "Lolita", "洛丽塔",
    "旗袍", "古镇旅拍", "汉服旅拍",
    # 场景
    "通勤穿搭", "职场穿搭", "约会穿搭", "旅行穿搭", "校园穿搭", "出游穿搭",
    # 韩日
    "韩系穿搭", "日系穿搭", "韩系通勤",
    # 美妆
    "美妆", "化妆教程", "眼妆教程", "日常妆容", "伪素颜", "口红试色", "美甲", "护肤",
    # 身材场景
    "小个子穿搭", "微胖穿搭", "显瘦穿搭", "梨形身材穿搭",
]

def curl_json(url: str):
    r = subprocess.run(["curl", "-s", "-A", UA, url, "--max-time", "25"],
                       capture_output=True, text=True, timeout=30)
    try:
        return json.loads(r.stdout)
    except Exception:
        return None

def init_db():
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    return con

def ingest(con, kw: str, pages: int, limit: int):
    added = 0
    for page in range(pages):
        start = page * limit
        q = urllib.parse.quote(kw)
        url = f"https://www.duitang.com/napi/blog/list/by_search/?kw={q}&start={start}&limit={limit}"
        d = curl_json(url)
        if not d or d.get("status") != 1:
            print(f"  [{kw}] page{page+1}: api fail/empty (status={d and d.get('status')})")
            break
        lst = d.get("data", {}).get("object_list") or []
        if not lst:
            break
        rows = []
        for o in lst:
            ph = o.get("photo") or {}
            img = ph.get("path")
            if not img:
                continue
            rows.append((
                "duitang", str(o.get("id")), img,
                f"https://www.duitang.com/blog/?id={o.get('id')}",
                None,                      # author: sender昵称需详情页, v1存sender_id
                "hotlink-attribution",     # 黄灯: 热链+署名
                ph.get("width"), ph.get("height"),
                json.dumps({"kw": kw, "tags": o.get("tags"), "sender_id": o.get("sender_id")},
                           ensure_ascii=False),
                o.get("photo", {}).get("aigc_label"),
                json.dumps(o, ensure_ascii=False)[:4000],
            ))
        before = con.total_changes
        con.executemany(
            "INSERT OR IGNORE INTO items (source,src_id,img_url,origin_url,author,license,w,h,tags,aigc_label,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            rows)
        added += con.total_changes - before
        print(f"  [{kw}] page{page+1}: +{con.total_changes - before} (list {len(lst)})")
        time.sleep(1.2)
    return added

def main():
    kws = DEFAULT_KWS
    pages, limit = 3, 24
    args = sys.argv[1:]
    if "--kws" in args:
        kws = args[args.index("--kws") + 1].split(",")
    if "--pages" in args: pages = int(args[args.index("--pages") + 1])
    if "--limit" in args: limit = int(args[args.index("--limit") + 1])
    con = init_db()
    total = 0
    for kw in kws:
        total += ingest(con, kw, pages, limit)
    con.commit()
    n = con.execute("SELECT source, COUNT(*) FROM items GROUP BY source").fetchall()
    print("DB total:", n)
    con.close()

if __name__ == "__main__":
    main()