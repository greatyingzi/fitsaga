#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga/collector")
PP = json.loads(pathlib.Path("/Users/liheng/work/self/fitsaga/data/prompt_pairs.json").read_text(encoding="utf-8"))
n = 0
for slug, pairs in PP.items():
    p = ROOT / ("_topic_" + slug + ".json")
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
print("prompt injected into", n, "topics")
