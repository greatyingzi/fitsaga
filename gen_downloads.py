#!/usr/bin/env python3
"""gen_downloads.py - 专题参考图包: 每专题zip打包对照图 → /downloads/ + JSON清单"""
import pathlib, zipfile, json

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
DL = PUB / "downloads"
DL.mkdir(parents=True, exist_ok=True)
TOPICS_DIR = PUB / "topics"

# 专题元数据(slug→标题)
META = {
  "gta6-style-prompt": "GTA6 迈阿密美学",
  "hanfu-prompt-guide": "汉服形制",
  "lighting-prompt-guide": "光线氛围",
  "fabric-texture-prompt": "面料质感",
  "nikki-art-reference": "游戏时装参考",
  "cyberpunk-vs-miami": "赛博 vs 迈阿密",
  "jk-lolita-ai-guide": "JK 与 Lolita",
  "wedding-dress-ai-guide": "婚纱礼服",
  "photo-to-prompt-method": "照片转 prompt",
  "cny-hanfu-ai": "春节国风",
}

def main():
    manifest = []
    for slug, title in META.items():
        src = TOPICS_DIR / slug
        if not src.exists():
            continue
        jpgs = sorted(src.glob("*.jpg"))
        if not jpgs:
            continue
        zpath = DL / f"{slug}-reference-pack.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for j in jpgs:
                z.write(j, j.name)
        size_kb = zpath.stat().st_size // 1024
        manifest.append({
            "slug": slug, "title": title,
            "zip": f"/downloads/{zpath.name}",
            "count": len(jpgs), "size_kb": size_kb,
            "images": [f"/topics/{slug}/{j.name}" for j in jpgs],
        })
        print(f"[{slug}] {len(jpgs)} imgs -> {zpath.name} ({size_kb}KB)")
    (PUB / "downloads" / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print("manifest:", len(manifest), "packs")

if __name__ == "__main__":
    main()
