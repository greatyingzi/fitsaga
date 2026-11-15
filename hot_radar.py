#!/usr/bin/env python3
"""hot_radar.py - 热点雷达: 热榜API→AI视觉需求初筛→_topic_idea_*.json归档"""
import subprocess, json, re, pathlib, datetime, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

# 视觉需求判定词(命中→值得做专题)
VISUAL_KW = ["游戏","电影","剧","番","动画","漫画","时装","时装周","时尚","汉服","cos",
             "票房","上映","发售","预告","皮肤","画风","角色","主角","民国","武侠","仙侠",
             "古风","婚礼","节日","春节","圣诞","万圣","情人节","暑期档","贺岁"]

def baidu_hot():
    r = subprocess.run(["curl","-s","https://top.baidu.com/api/board?platform=wise&tab=realtime",
                        "-A","Mozilla/5.0","--max-time","20"], capture_output=True, text=True, timeout=25)
    try:
        d = json.loads(r.stdout)
        words = []
        for c in d.get("data",{}).get("cards") or []:
            for grp in (c.get("content") or []):
                for it in (grp.get("content") or []):
                    w = it.get("word")
                    if w: words.append(w)
        return words
    except Exception:
        return []

def toutiao_hot():
    r = subprocess.run(["curl","-s","https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc",
                        "-A","Mozilla/5.0","--max-time","20"], capture_output=True, text=True, timeout=25)
    try:
        d = json.loads(r.stdout)
        return [x.get("Title","") for x in d.get("data",[])]
    except Exception:
        return []

def bilibili_hot():
    r = subprocess.run(["curl","-s","https://api.bilibili.com/x/web-interface/search/square?limit=50",
                        "-A","Mozilla/5.0","-b","buvid3=x","--max-time","20"], capture_output=True, text=True, timeout=25)
    try:
        d = json.loads(r.stdout)
        return [x.get("keyword","") for x in (d.get("data",{}).get("trending",{}).get("list") or [])]
    except Exception:
        return []

def main():
    today = datetime.date.today().isoformat()
    all_hot = []
    for name, fn in [("baidu",baidu_hot),("toutiao",toutiao_hot),("bilibili",bilibili_hot)]:
        try:
            ws = fn()
            all_hot += [(name,w) for w in ws if w]
            print(f"[{name}] {len(ws)} 条")
        except Exception as e:
            print(f"[{name}] fail {str(e)[:60]}")
    # 初筛: 命中视觉关键词
    hits = [(src,w) for src,w in all_hot if any(k in w for k in VISUAL_KW)]
    print(f"\n视觉相关热点: {len(hits)}")
    for src,w in hits[:20]:
        print(f"  [{src}] {w[:50]}")
    # 归档(append到jsonl, 去重)
    out = DATA / f"radar_{today}.json"
    seen = set()
    if out.exists():
        seen = {x["word"] for x in json.loads(out.read_text())}
    items = [{"word":w,"source":src,"date":today} for src,w in hits if w not in seen]
    if out.exists() and items:
        old = json.loads(out.read_text())
        json.dump(old+items, out.open("w"), ensure_ascii=False)
    else:
        json.dump(items, out.open("w"), ensure_ascii=False)
    print(f"\n归档: +{len(items)} → {out.name}")

if __name__ == "__main__":
    main()
