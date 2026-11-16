#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path("/Users/liheng/work/self/fitsaga/collector")
PP = json.loads(pathlib.Path("/Users/liheng/work/self/fitsaga/data/prompt_pairs.json").read_text(encoding="utf-8"))

# slug别名映射: en json里的slug → prompt_pairs里的slug
ALIAS = {
  "hanfu-form": "form", "hanfu-dynasty": "dynasty",
}

# 修 en-hanfu
p = ROOT / "_topic_en_hanfu-prompt-guide.json"
t = json.loads(p.read_text(encoding="utf-8"))
for ex in t.get("examples", []):
    key = ALIAS.get(ex["slug"], ex["slug"])
    for pp in PP.get("hanfu-prompt-guide", []):
        if pp["slug"] == key:
            ex["good_prompt"] = pp["good_prompt"]
            ex["bad_prompt"] = pp["bad_prompt"]
p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print("en-hanfu:", sum(1 for e in t["examples"] if e.get("good_prompt")))

# 修 en-gta6(文件名特殊)
p = ROOT / "_topic_en_gta6.json"
t = json.loads(p.read_text(encoding="utf-8"))
for ex in t.get("examples", []):
    for pp in PP.get("gta6-style-prompt", []):
        if pp["slug"] == ex["slug"]:
            ex["good_prompt"] = pp["good_prompt"]
            ex["bad_prompt"] = pp["bad_prompt"]
p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print("en-gta6:", sum(1 for e in t["examples"] if e.get("good_prompt")))

# 查 cny zh json(为什么zh=0)
p = ROOT / "_topic_cny.json"
t = json.loads(p.read_text(encoding="utf-8"))
print("cny zh examples:", [(e["slug"], bool(e.get("good_prompt"))) for e in t.get("examples", [])])
