#!/usr/bin/env python3
import re, pathlib, ast, json
src = pathlib.Path("/Users/liheng/work/self/fitsaga/gen_pairs_batch.py").read_text(encoding="utf-8")
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "PAIRS_BY_TOPIC":
        val = ast.literal_eval(node.value)
        out = {}
        for slug, pairs in val.items():
            out[slug] = [{"slug": p["slug"], "good_prompt": p["good"], "bad_prompt": p["bad"]} for p in pairs]
        pathlib.Path("/Users/liheng/work/self/fitsaga/data/prompt_pairs.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("extracted:", {k: len(v) for k, v in out.items()})
