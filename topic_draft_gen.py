#!/usr/bin/env python3
"""topic_draft_gen.py - 雷达热点→专题选题草稿(自动, 不发布)"""
import json, pathlib, subprocess, urllib.parse, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"

# 已有的视觉词过滤(同radar)
VISUAL_KW = ["游戏","电影","剧","番","动画","漫画","时装","时尚","汉服","cos",
             "票房","上映","发售","预告","皮肤","画风","角色","主角","武侠","仙侠",
             "古风","婚礼","节日","春节","圣诞","万圣","情人节","档期"]

def suggest(q):
    r = subprocess.run(["curl","-s",f"https://www.baidu.com/sugrec?prod=pc&wd={urllib.parse.quote(q)}","--max-time","15"],
                       capture_output=True, text=True, timeout=20)
    try: return [x["q"] for x in json.loads(r.stdout).get("g",[])]
    except: return []

def main():
    # 取最近雷达归档
    files = sorted(DATA.glob("radar_*.json"))
    if not files:
        print("no radar data"); return
    hits = []
    seen = set()
    for f in files[-3:]:
        for it in json.loads(f.read_text()):
            w = it["word"]
            if w in seen: continue
            seen.add(w)
            if any(k in w for k in VISUAL_KW):
                hits.append({"word": w, "source": it["source"], "date": it["date"]})
    print(f"候选热点: {len(hits)}")
    # 每个热点挖相关词→生成选题草稿
    drafts = []
    for h in hits[:10]:
        w = h["word"]
        subs = suggest(w)[:5]
        drafts.append({
            "keyword": w, "source": h["source"], "date": h["date"],
            "related_queries": subs,
            "topic_type": "A",
            "status": "idea-draft",   # 草稿状态=不自动发布, 等人工挑选
        })
        print(f"  [{w}] → {subs[:3]}")
    out = DATA / "topic_drafts.json"
    old = json.loads(out.read_text()) if out.exists() else []
    known = {x.get("keyword") for x in old}
    new = [d for d in drafts if d["keyword"] not in known]
    json.dump(old + new, out.open("w"), ensure_ascii=False, indent=1)
    print(f"草稿池: +{len(new)} → {out.name} (总{len(old)+len(new)})")

if __name__ == "__main__":
    main()
