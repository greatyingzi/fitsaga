#!/usr/bin/env python3
"""lofter.py — Lofter H5 tag页采集(免登录, 汉服/JK/Lolita内容池)
GET www.lofter.com/front/blog/tag/<tag> (iPhone UA) → __initialize_data__ → postList[].postView{firstImage.orign}
每tag第一页20条; 多tag扩面。版权: 高(原创画师/同袍), 热链imglf无防盗链, 署名博主
"""
import subprocess, json, sqlite3, re, sys, time, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1"

TAGS = ["汉服", "JK制服", "Lolita", "汉服日常", "马面裙", "lo娘日常", "旗袍", "中华风lo"]

def fetch_tag(tag):
    q = urllib.parse.quote(tag)
    url = f"https://www.lofter.com/front/blog/tag/{q}"
    r = subprocess.run(["curl","-s","-A",UA,url,"--max-time","30","--compressed"], capture_output=True, text=True, timeout=40)
    h = r.stdout or ""
    m = re.search(r"window\.__initialize_data__\s*=\s*(\{.*?\});?\s*</script>", h, re.S)
    if not m:
        m = re.search(r"window\.__initialize_data__\s*=\s*(\{.*?\})", h, re.S)
    if not m:
        return []
    try:
        d = json.loads(m.group(1))
    except Exception:
        return []
    posts = []
    blog_infos = {}
    def walk(o):
        if isinstance(o, dict):
            if "postList" in o and isinstance(o["postList"], list):
                posts.extend(o["postList"])
            if "blogInfo" in o and isinstance(o["blogInfo"], dict):
                bi = o["blogInfo"]
                bid = str(bi.get("blogId") or bi.get("id") or "")
                if bid: blog_infos[bid] = bi.get("blogNickName")
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d)
    out = []
    for p in posts:
        pv = p.get("postView") or p
        first = ((pv.get("firstImage") or {}) or {})
        img = first.get("orign") or first.get("origin") or first.get("url")
        if not img: continue
        out.append({
            "id": pv.get("id") or pv.get("postId"),
            "img": img,
            "title": (pv.get("title") or "")[:60],
            "digest": (pv.get("digest") or "")[:80],
            "permalink": pv.get("permalink") or pv.get("blogPageUrl"),
            "blog": blog_infos.get(str(pv.get("blogId") or "")),
            "tags": pv.get("tagList") or [],
        })
    return out

def main():
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT/"collector"/"_schema.sql", encoding="utf-8").read())
    total = 0
    for tag in TAGS:
        items = fetch_tag(tag)
        rows = []
        for it in items:
            rows.append((
                "lofter", str(it["id"]), it["img"], it["permalink"] or "",
                it.get("blog"), "hotlink-attribution",
                None, None,
                json.dumps({"kw": tag, "tags": it["tags"][:5], "digest": it["digest"]}, ensure_ascii=False),
                None, json.dumps(it, ensure_ascii=False)[:3000],
            ))
        before = con.total_changes
        con.executemany("INSERT OR IGNORE INTO items (source,src_id,img_url,origin_url,author,license,w,h,tags,aigc_label,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
        n = con.total_changes - before
        total += n
        print(f"[{tag}] +{n} (posts {len(items)})")
        time.sleep(2.0)
    con.commit()
    print("lofter total:", con.execute("SELECT COUNT(*) FROM items WHERE source='lofter'").fetchone())
    con.close()

if __name__ == "__main__":
    main()