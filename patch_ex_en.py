#!/usr/bin/env python3
import json, pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/collector/_topic_en_hanfu-prompt-guide.json")
t = json.loads(P.read_text(encoding="utf-8"))
t["examples"] = [
  {"slug":"hanfu-form","title":"Compare 1 · Form layers",
   "good_cap":"OK: ming dynasty mamian skirt + cross-collar right-over-left + buyao hairpins + garden — form layers all present",
   "bad_cap":"X: bare 'hanfu dress' — photo-studio mashup, no dynasty identity"},
  {"slug":"hanfu-dynasty","title":"Compare 2 · Dynasty difference",
   "good_cap":"OK: tang chest-high ruqun + ribbon sash + dancing + fabric floating — Tang flowing silhouette",
   "bad_cap":"X: bare 'tang costume' — static, costume-rental look"},
]
P.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
print("examples:", len(t["examples"]))
