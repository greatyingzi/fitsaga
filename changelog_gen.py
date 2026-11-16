#!/usr/bin/env python3
"""changelog_gen.py - 专题追更日志: data/changelog.json → 专题页追更区渲染数据"""
import pathlib, json, datetime

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"

# 初始追更记录(手工维护或流水线追加)
SEED = [
  {"slug": "gta6-style-prompt", "date": "2026-11-15", "note": "专题上线：完整 prompt 公式与正反例对照"},
  {"slug": "gta6-style-prompt", "date": "2026-11-16", "note": "参考图包可下载（6 张对照图）"},
  {"slug": "cny-hanfu-ai", "date": "2026-11-15", "note": "专题上线：三大场景+人物动作词库（预排 2027 春节）"},
  {"slug": "hanfu-prompt-guide", "date": "2026-11-16", "note": "专题上线：形制英文映射 + 3 组对照"},
]

def main():
    f = DATA / "changelog.json"
    if not f.exists():
        json.dump(SEED, f.open("w"), ensure_ascii=False, indent=1)
        print("changelog seeded:", len(SEED))
    else:
        print("changelog exists:", len(json.loads(f.read_text())))

if __name__ == "__main__":
    main()
