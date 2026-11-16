#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")

# 1) prompt_pairs.json 补 gta6-style-prompt 三组
PP = json.loads((ROOT/"data/prompt_pairs.json").read_text(encoding="utf-8"))
PP["gta6-style-prompt"] = [
  {"slug":"sky","good_prompt":"Miami Beach at dusk, pink orange purple gradient sky, natural sky gradient, palm trees, ocean, cinematic still","bad_prompt":"Miami Beach at dusk, sunset, palm trees, ocean, photo"},
  {"slug":"haze","good_prompt":"Miami coastal highway at golden hour, humid haze, atmospheric perspective, neon glow reflecting on wet streets, art deco buildings, cinematic still, film grain","bad_prompt":"Miami coastal highway at golden hour, art deco buildings, cinematic"},
  {"slug":"motion","good_prompt":"a young woman in hawaiian shirt leaning on a muscle car, candid pose, mid-motion, Miami dusk, pink orange sky, cinematic still","bad_prompt":"a young woman in hawaiian shirt standing pose, Miami dusk, cinematic still"},
]
(ROOT/"data/prompt_pairs.json").write_text(json.dumps(PP, ensure_ascii=False, indent=1), encoding="utf-8")
print("gta6 pairs:", len(PP["gta6-style-prompt"]))

# 2) 注入全部zh专题(gta6用_topic_gta6.json)
n = 0
for slug, pairs in PP.items():
    fname = "_topic_gta6.json" if slug == "gta6-style-prompt" else f"_topic_{slug}.json"
    p = ROOT/"collector"/fname
    if not p.exists(): continue
    t = json.loads(p.read_text(encoding="utf-8"))
    if not t.get("examples"): continue
    for ex in t["examples"]:
        for pp in pairs:
            if pp["slug"] == ex["slug"]:
                ex["good_prompt"] = pp["good_prompt"]
                ex["bad_prompt"] = pp["bad_prompt"]
    p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    n += 1
print("zh injected:", n)

# 3) en专题注入(用同slug的zh prompt; en文件名_topic_en_*.json)
m = 0
for slug, pairs in PP.items():
    p = ROOT/"collector"/f"_topic_en_{slug}.json"
    if not p.exists(): continue
    t = json.loads(p.read_text(encoding="utf-8"))
    if not t.get("examples"): continue
    for ex in t["examples"]:
        for pp in pairs:
            if pp["slug"] == ex["slug"]:
                ex["good_prompt"] = pp["good_prompt"]
                ex["bad_prompt"] = pp["bad_prompt"]
    p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    m += 1
print("en injected:", m)
