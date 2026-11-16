#!/bin/bash
cd /Users/liheng/work/self/fitsaga
python3 gen_topics.py > /dev/null 2>&1
python3 gen_sitemap.py > /dev/null 2>&1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
export CLOUDFLARE_API_TOKEN=$(python3 -c "import re;print(re.search(r'api_token *= *.[^\"]+.',open('/Users/liheng/.wrangler/config/default.toml').read()).group(1))")
/Users/liheng/work/self/linghub/node_modules/.bin/wrangler pages deploy public --project-name=fitsaga-dev --branch=test --commit-dirty=true > /tmp/dep.log 2>&1
tail -1 /tmp/dep.log
sleep 3
for s in hanfu-prompt-guide lighting-prompt-guide fabric-texture-prompt jk-lolita-ai-guide wedding-dress-ai-guide cny-hanfu-ai cyberpunk-vs-miami nikki-art-reference photo-to-prompt-method; do
  C=$(curl -sL "https://fitsaga-dev.pages.dev/topics/$s" --max-time 20 | grep -o "OK PROMPT" | wc -l | tr -d ' ')
  echo "$s pairs: $C"
done