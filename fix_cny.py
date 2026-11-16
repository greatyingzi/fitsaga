#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga")
PP = json.loads((ROOT/"data/prompt_pairs.json").read_text(encoding="utf-8"))
p = ROOT/"collector/_topic_cny.json"
t = json.loads(p.read_text(encoding="utf-8"))
for ex in t.get("examples", []):
    for pp in PP.get("cny-hanfu-ai", []):
        if pp["slug"] == ex["slug"]:
            ex["good_prompt"] = pp["good_prompt"]
            ex["bad_prompt"] = pp["bad_prompt"]
p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print("cny:", sum(1 for e in t["examples"] if e.get("good_prompt")))
