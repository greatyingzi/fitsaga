#!/usr/bin/env python3
"""topic_filter.py — 选题池清洗: 只留穿搭域相关题"""
import sqlite3, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "fitsaga.db"

KEEP = ["穿","搭","裙","衬衫","外套","风 ", "风穿搭","风是什么","风怎么","风vs","风对比",
        "汉服","马面","JK","格裙","Lolita","洛丽塔","旗袍","通勤","约会","体型","身材",
        "显高","显瘦","显胖","配色","颜色","色系","衣","裤","鞋","帽","包","妆","美甲",
        "发型","第一季","春","夏","秋","冬","婚礼","婚","旅拍","学校","职场","面试"]
DROP = ["装修","动画","游戏","图 片素材","英语","英文","游戏名","下载","软件","app","壁纸",
        "表情包","头像","警察","警衔","发黄","清洗","机洗","危害","减肥","减臀","牌子","品牌排名"]

def main():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id,keyword FROM topics").fetchall()
    keep_n = drop_n = 0
    for tid, kw in rows:
        if any(k in kw for k in DROP):
            con.execute("UPDATE topics SET status='retired' WHERE id=?", (tid,)); drop_n += 1
        elif not any(k in kw for k in KEEP):
            con.execute("UPDATE topics SET status='retired' WHERE id=?", (tid,)); drop_n += 1
        else:
            keep_n += 1
    con.commit()
    print(f"保留 {keep_n} | 淘汰 {drop_n}")
    print("各状态:", con.execute("SELECT status,COUNT(*) FROM topics GROUP BY status").fetchall())
    print("\n清洗后精选30题:")
    for (kw,t,) in con.execute("SELECT keyword,type FROM topics WHERE status='idea' ORDER BY RANDOM() LIMIT 30"):
        print(f" [{t}] {kw}")
    con.close()

if __name__ == "__main__":
    main()
