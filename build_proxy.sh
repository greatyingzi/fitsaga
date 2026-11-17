#!/bin/bash
# FitSaga build for action proxy (ops-runner/proxy.yml)
# proxy固定部署 dist/, 本脚本全量生成到 public/ 后同步到 dist/
set -e
cd "$(dirname "$0")"

python3 gen_site.py
python3 gen_nikki.py
NIKKI_PAGE=2 python3 gen_nikki.py
NIKKI_PAGE=3 python3 gen_nikki.py
python3 gen_nikki_detail.py
python3 gen_nikki_en.py
python3 gen_collections.py
python3 gen_collections_b2.py
python3 gen_collections_b3.py
python3 gen_ai.py
python3 gen_zara.py
python3 gen_guide.py
python3 gen_topics.py
python3 gen_downloads.py
python3 gen_downloads_page.py
python3 gen_search_index.py
python3 gen_sitemap.py

rm -rf dist
cp -r public dist
echo "build done: $(find dist -type f | wc -l | tr -d ' ') files"
