#!/usr/bin/env python3
"""gen_search_index.py - 站内搜索索引: 全部页面标题+URL → public/search-index.json"""
import sqlite3, pathlib, json, re

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DB = ROOT / "data" / "fitsaga.db"

def slugify(name):
    return re.sub(r"[^\w\u4e00-\u9fff-]+", "-", str(name).strip()).strip("-") or "x"

def main():
    idx = []
    # 风格频道
    for k, zh in [("hanfu","古风汉服"),("qipao","旗袍优雅"),("sweet","甜美少女"),("sexy","辣妹性感"),
                  ("jk","JK制服"),("street","街头潮流"),("winter","秋冬叠穿"),("beauty","美妆变美"),("korean","韩系街拍")]:
        idx.append({"t": zh + "搭配图鉴", "u": "/style/" + k + ".html", "c": "风格"})
    # 合集
    for slug, t in [("starry-night","星夜漫游"),("fairytale-dream","童话与梦"),("spring-floral","花开时节"),
                    ("ocean-rain","海洋与雨"),("dark-gothic","暗夜哥特"),("jk-uniform","JK制服精选"),
                    ("sweet-girl","甜妹精选"),("quiet-luxury","静奢风"),("dopamine","多巴胺穿搭"),
                    ("millard","美拉德穿搭"),("american-retro","美式复古"),("french-style","法式穿搭"),
                    ("new-chinese","新中式"),("commute","通勤穿搭"),("knitwear","针织衫"),
                    ("coat-season","秋冬大衣"),("qipao-modern","旗袍现代穿法"),("lolita-picks","Lolita精选"),
                    ("hanfu-daily","汉服日常"),("travel-hanfu","古镇旅拍")]:
        idx.append({"t": t, "u": "/collection/" + slug, "c": "合集"})
    # 图鉴与专题
    idx.append({"t":"无限暖暖套装图鉴","u":"/nikki/infinity.html","c":"图鉴"})
    idx.append({"t":"奇迹暖暖套装图鉴(高清)","u":"/nikki/miraclehd.html","c":"图鉴"})
    idx.append({"t":"奇迹暖暖套装图鉴","u":"/nikki/miracle.html","c":"图鉴"})
    idx.append({"t":"闪耀暖暖套装图鉴","u":"/nikki/shining.html","c":"图鉴"})
    idx.append({"t":"ZARA 女装大片","u":"/zara.html","c":"大片"})
    idx.append({"t":"AI 灵感图鉴","u":"/ai.html","c":"AI图"})
    idx.append({"t":"AI 画法研究所","u":"/topics.html","c":"专题"})
    idx.append({"t":"穿搭研究所","u":"/guide.html","c":"文章"})
    # 文章
    con = sqlite3.connect(DB)
    for slug, title in con.execute("SELECT slug,title FROM articles WHERE status='published'"):
        idx.append({"t": title, "u": "/guide/" + slug, "c": "文章"})
    # 专题
    for f in (ROOT/"collector").glob("_topic_*.json"):
        t = json.loads(f.read_text(encoding="utf-8"))
        idx.append({"t": t["title"], "u": "/topics/" + t["slug"], "c": "专题"})
    # 套装详情(中文优先, cap 500)
    for (name,) in con.execute("SELECT COALESCE(alias_zh,name) FROM suits WHERE EXISTS(SELECT 1 FROM suit_imgs WHERE suit_id=suits.id) LIMIT 500"):
        idx.append({"t": str(name) + " 套装图鉴", "u": "/nikki/s/" + slugify(name), "c": "套装"})
    con.close()
    (PUB / "search-index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    print("search index:", len(idx), "entries")

if __name__ == "__main__":
    main()
