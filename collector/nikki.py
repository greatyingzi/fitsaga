#!/usr/bin/env python3
"""FitSaga collector: BWIKI 暖暖套装 (MediaWiki API, 零反爬) v2
三库三策略:
  qjnn(奇迹): allimages aiprefix=套装 → 套装·X-部件.png 直链
  synn(闪耀): categorymembers Category:套装 → 每页 prop=images → 文件:部件·Y / 展示图
  wxnn(无限): allimages aiprefix=套装 (套装<名><角度>) 直链
用法: python3 nikki.py [--wikis qjnn,synn,wxnn] [--max-pages 60]
"""
import json, re, sqlite3, subprocess, sys, time, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

def api(wiki, params):
    base = f"https://wiki.biligame.com/{wiki}/api.php"
    q = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"{base}?{q}&format=json"
    r = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url, "--max-time", "30"],
                       capture_output=True, text=True, timeout=40)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}

def upsert_suit(con, game, name, source):
    cur = con.execute("INSERT OR IGNORE INTO suits (game,name,source) VALUES (?,?,?)", (game, name, source))
    sid = con.execute("SELECT id FROM suits WHERE game=? AND name=?", (game, name)).fetchone()
    return (sid[0] if sid else None), cur.rowcount

def add_img(con, sid, url, kind, raw):
    return con.execute("INSERT OR IGNORE INTO suit_imgs (suit_id,img_url,kind,raw_name) VALUES (?,?,?,?)",
                       (sid, url, kind, raw)).rowcount

def file_url(wiki, title):
    """文件:X → 直链"""
    d = api(wiki, {"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url"})
    for pg in (d.get("query") or {}).get("pages", {}).values():
        ii = pg.get("imageinfo") or []
        if ii:
            return ii[0].get("url")
    return None

def collect_qjnn(con, max_pages):
    aicontinue, pages, s_add, i_add = None, 0, 0, 0
    KIND = re.compile(r"套装[·.](.+?)-(.+?)\.(?:png|jpg|jpeg|webp)$", re.I)
    PLAIN = re.compile(r"套装[·.](.+?)\.(?:png|jpg|jpeg|webp)$", re.I)
    while pages < max_pages:
        params = {"action": "query", "list": "allimages", "aiprefix": "套装", "ailimit": 500, "aiprop": "url"}
        if aicontinue: params["aicontinue"] = aicontinue
        d = api("qjnn", params)
        ims = (d.get("query") or {}).get("allimages") or []
        if not ims: break
        for im in ims:
            name, url = im.get("name") or "", im.get("url") or ""
            m = KIND.search(name)
            if m: suit, kind = m.group(1).strip(), m.group(2).strip()
            else:
                m2 = PLAIN.search(name)
                if not m2: continue
                suit, kind = m2.group(1).strip(), "图"
            sid, a = upsert_suit(con, "奇迹暖暖", suit, "bwiki:qjnn"); s_add += a
            if sid: i_add += add_img(con, sid, url, kind, name)
        pages += 1
        cont = (d.get("continue") or {}).get("aicontinue")
        if not cont: break
        aicontinue = cont
        time.sleep(0.7)
    print(f"[qjnn] pages={pages} suits+{s_add} imgs+{i_add}")
    return s_add, i_add

def collect_synn(con, max_pages):
    # 全量套装页 (一次500足够, cmlimit max=500)
    d = api("synn", {"action": "query", "list": "categorymembers", "cmtitle": "Category:套装", "cmlimit": 500})
    suits = [m["title"] for m in (d.get("query") or {}).get("categorymembers", []) if m["title"].startswith("套装·")]
    print(f"[synn] suit pages found: {len(suits)}")
    s_add = i_add = 0
    # 批量 prop=images (每批50页)
    for bi in range(0, len(suits), 50):
        batch = suits[bi:bi+50]
        d2 = api("synn", {"action": "query", "titles": "|".join(batch), "prop": "images", "imlimit": 50})
        pending = []
        for pg in (d2.get("query") or {}).get("pages", {}).values():
            name = (pg.get("title") or "").replace("套装·", "").strip()
            if not name: continue
            sid, a = upsert_suit(con, "闪耀暖暖", name, "bwiki:synn"); s_add += a
            for im in (pg.get("images") or []):
                t = im.get("title") or ""
                if "施工" in t: continue  # 占位图跳过
                kind = "部件" if "部件·" in t else ("展示" if "展示" in t else "图")
                pending.append((sid, t, kind, t))
        # 二次解析 imageinfo 拿直链 (每批25个文件title)
        for si in range(0, len(pending), 25):
            chunk = pending[si:si+25]
            titles = "|".join(c[1] for c in chunk)
            d3 = api("synn", {"action": "query", "titles": titles, "prop": "imageinfo", "iiprop": "url"})
            tmap = {}
            for pg in (d3.get("query") or {}).get("pages", {}).values():
                ii = pg.get("imageinfo") or []
                if ii: tmap[pg.get("title")] = ii[0].get("url")
            for sid, t, kind, raw in chunk:
                u = tmap.get(t)
                if u: i_add += add_img(con, sid, u, kind, raw)
        time.sleep(1.2)
    print(f"[synn] suits+{s_add} imgs+{i_add}")
    return s_add, i_add

def collect_wxnn(con, max_pages):
    # 命名: 套装<名><NN>.png / 套装<名>·<变体><NN>.jpg → 用 aiprefix=套装 枚举
    aicontinue, pages, s_add, i_add = None, 0, 0, 0
    PAT = re.compile(r"^套装(.+?)(\d{2,3})\.(?:png|jpg|jpeg|webp)$", re.I)
    while pages < max_pages:
        params = {"action": "query", "list": "allimages", "aiprefix": "套装", "ailimit": 500, "aiprop": "url"}
        if aicontinue: params["aicontinue"] = aicontinue
        d = api("wxnn", params)
        ims = (d.get("query") or {}).get("allimages") or []
        if not ims: break
        for im in ims:
            name, url = im.get("name") or "", im.get("url") or ""
            m = PAT.match(name)
            if not m: continue
            suit = m.group(1).strip()
            kind = f"展示{m.group(2)}"
            sid, a = upsert_suit(con, "无限暖暖", suit, "bwiki:wxnn"); s_add += a
            if sid: i_add += add_img(con, sid, url, kind, name)
        pages += 1
        cont = (d.get("continue") or {}).get("aicontinue")
        if not cont: break
        aicontinue = cont
        time.sleep(0.7)
    print(f"[wxnn] pages={pages} suits+{s_add} imgs+{i_add}")
    return s_add, i_add


def collect_qjnn_pages(con, max_pages):
    """奇迹暖暖: Category:套装 页面(500+) → 每页 images(部件/海报/无背景)"""
    d = api("qjnn", {"action": "query", "list": "categorymembers", "cmtitle": "Category:套装", "cmlimit": 500})
    suits = [m["title"] for m in (d.get("query") or {}).get("categorymembers", [])
             if m["title"] not in ("模板:套装",)]
    print(f"[qjnn-pages] raw pages: {len(suits)}")
    s_add = i_add = 0
    for bi in range(0, len(suits), 50):
        batch = suits[bi:bi+50]
        d2 = api("qjnn", {"action": "query", "titles": "|".join(batch), "prop": "images", "imlimit": 50})
        pending = []
        for pg in (d2.get("query") or {}).get("pages", {}).values():
            raw = pg.get("title") or ""
            name = raw.replace("套装/", "").strip()
            if not name or name == "套装" or raw.startswith("模板"): continue
            sid, a = upsert_suit(con, "奇迹暖暖", name, "bwiki:qjnn"); s_add += a
            for im in (pg.get("images") or []):
                t = im.get("title") or ""
                kind = "海报" if "海报" in t else ("部件" if "部件" in t else ("无背景" if "无背景" in t else "图"))
                pending.append((sid, t, kind, t))
        for si in range(0, len(pending), 25):
            chunk = pending[si:si+25]
            titles = "|".join(c[1] for c in chunk)
            d3 = api("qjnn", {"action": "query", "titles": titles, "prop": "imageinfo", "iiprop": "url"})
            tmap = {}
            for pg in (d3.get("query") or {}).get("pages", {}).values():
                ii = pg.get("imageinfo") or []
                if ii: tmap[pg.get("title")] = ii[0].get("url")
            for sid, t, kind, raw in chunk:
                u = tmap.get(t)
                if u: i_add += add_img(con, sid, u, kind, raw)
        time.sleep(1.0)
    print(f"[qjnn-pages] suits+{s_add} imgs+{i_add}")
    return s_add, i_add

def main():
    wikis = sys.argv[sys.argv.index("--wikis") + 1].split(",") if "--wikis" in sys.argv else ["qjnn_pages", "synn", "wxnn"]
    max_pages = int(sys.argv[sys.argv.index("--max-pages") + 1]) if "--max-pages" in sys.argv else 60
    con = sqlite3.connect(DB)
    con.executescript(open(ROOT / "collector" / "_schema.sql", encoding="utf-8").read())
    fn = {"qjnn": collect_qjnn, "qjnn_pages": collect_qjnn_pages, "synn": collect_synn, "wxnn": collect_wxnn}
    for w in wikis:
        if w in fn: fn[w](con, max_pages)
        time.sleep(1.5)
    con.commit()
    print("DB suits:", con.execute("SELECT game,COUNT(*) FROM suits GROUP BY game").fetchall())
    print("DB suit_imgs:", con.execute("SELECT COUNT(*) FROM suit_imgs").fetchone())
    con.close()

if __name__ == "__main__":
    main()