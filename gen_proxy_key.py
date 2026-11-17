#!/usr/bin/env python3
import subprocess, tempfile, os
td = tempfile.mkdtemp(prefix="fitsaga-proxy-key")
kp = os.path.join(td, "k")
subprocess.run(["ssh-keygen", "-t", "ed25519", "-N", "", "-C", "ops-runner-proxy-fitsaga", "-f", kp, "-q"], check=True)
priv = open(kp).read().strip()
pub = open(kp + ".pub").read().strip()
out = "/Users/liheng/work/self/fitsaga/PROXY_SETUP.md"
doc = "# FitSaga action proxy 接入\n\n"
doc += "## 状态\n- ops-runner proxy.yml 已注册 fitsaga 站点（hub tasks/sites.json）\n- fitsaga 仓库已加 deploy key（title=ops-runner-proxy）\n- 本地 build_proxy.sh 已就绪（输出 dist/ 504 文件）\n- 待做：把下面 key 加入 ops-runner 的 PROXY_KEYS_JSON secret\n\n"
doc += "## fitsaga site key（追加到 PROXY_KEYS_JSON，保留原有站点）\n\n```json\n"
doc += chr(34) + "fitsaga" + chr(34) + ": " + chr(34) + priv.replace(chr(10), "\\n") + chr(34) + "\n```\n\n"
doc += "Public key:\n```\n" + pub + "\n```\n\n"
doc += "Private key:\n```\n" + priv + "\n```\n"
open(out, "w", encoding="utf-8").write(doc)
gi = "/Users/liheng/work/self/fitsaga/.gitignore"
existing = open(gi).read()
if "PROXY_SETUP.md" not in existing:
    with open(gi, "a") as f: f.write("\nPROXY_SETUP.md\n")
print("PROXY_SETUP.md written, key len:", len(priv))