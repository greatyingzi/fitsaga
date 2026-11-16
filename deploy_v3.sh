#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
export CLOUDFLARE_API_TOKEN=$(python3 -c "import re;print(re.search(r'api_token *= *.[^\"]+.',open('/Users/liheng/.wrangler/config/default.toml').read()).group(1))")
cd /Users/liheng/work/self/fitsaga
python3 gen_search_index.py > /dev/null 2>&1
python3 gen_sitemap.py > /dev/null 2>&1
/Users/liheng/work/self/linghub/node_modules/.bin/wrangler pages deploy public --project-name=fitsaga-dev --branch=test --commit-dirty=true > /tmp/d1.log 2>&1
tail -1 /tmp/d1.log
/Users/liheng/work/self/linghub/node_modules/.bin/wrangler pages deploy public --project-name=fitsaga --branch=main --commit-dirty=true > /tmp/d2.log 2>&1
tail -1 /tmp/d2.log
sleep 65
echo "LAYOUT ONLINE"
node layout_audit.js 2>&1 | head -12