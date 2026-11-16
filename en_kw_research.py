#!/usr/bin/env python3
"""en_kw_research.py - EN专题的海外真实搜索词挖掘(Google suggest英文)"""
import json, subprocess, urllib.parse, pathlib

SEEDS = {
  "gta6-style-prompt": ["gta 6 aesthetic", "miami aesthetic prompt", "vice city style"],
  "hanfu-prompt-guide": ["hanfu prompt", "chinese traditional dress ai", "mamian skirt"],
  "lighting-prompt-guide": ["cinematic lighting prompt", "golden hour prompt", "rembrandt lighting ai"],
  "fabric-texture-prompt": ["fabric texture prompt", "silk dress prompt ai", "velvet texture ai"],
  "nikki-art-reference": ["infinity nikki outfit ideas", "nikki dress up guide", "game costume concept art"],
  "cyberpunk-vs-miami": ["cyberpunk vs miami", "blade runner aesthetic prompt"],
  "jk-lolita-ai-guide": ["lolita fashion prompt", "jk uniform aesthetic", "sweet lolita ai"],
  "wedding-dress-ai-guide": ["wedding dress prompt", "bridal editorial ai", "lace wedding ai"],
  "cny-hanfu-ai": ["chinese new year outfit", "lunar new year fashion ai"],
  "photo-to-prompt-method": ["photo to prompt", "image to prompt technique"],
}

def g_sug_en(q):
    r = subprocess.run(["curl","-s",f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(q)}&hl=en","--max-time","15"],
                       capture_output=True, text=True, timeout=20)
    try: return json.loads(r.stdout)[1]
    except: return []

def main():
    out = {}
    for slug, seeds in SEEDS.items():
        words = set()
        for s in seeds:
            words.update(g_sug_en(s))
        out[slug] = sorted(words)
        print(f"[{slug}] {len(words)} en queries")
        for w in sorted(words)[:5]: print("   ", w)
    pathlib.Path("/Users/liheng/work/self/fitsaga/data/en_keywords.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(v) for v in out.values())
    print(f"\nEN 关键词池: {total}")

if __name__ == "__main__":
    main()
