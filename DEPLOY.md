# FitSaga 部署环境规范（2026-11-15 起）

## 双环境架构

| 环境 | 域名 | 分支 | 用途 |
|---|---|---|---|
| **测试/预览** | fitsaga-dev.pages.dev | test 分支 | 新功能/改版先上这里验收 |
| **正式** | fitsaga.pages.dev | main 分支 | 验收通过后合入 main 发布 |

## 流程铁律（主人定的规则）

1. **任何改动先 push 到 test 分支** → Actions 自动部署到 fitsaga-dev.pages.dev
2. **双飞轮验收**（audit_flywheel.js + linkscan.js + 视觉截图）在测试环境跑
3. **通过后**合入 main（git checkout main && git merge test && git push）→ 自动发布正式
4. 每日定时任务只对当前默认分支跑采集+部署（main），test 分支手动触发验证用

## 本地快速操作

```bash
# 上测试
git checkout -b test && git push origin test   # 首次
# 或 git checkout test && git merge 开发分支 && git push

# 验收后上正式
git checkout main && git merge test && git push

# 手动部署当前目录到某环境
wrangler pages deploy public --project-name=fitsaga-dev --branch=test
```

## 之前的教训
- 直接改线上再补测试 = 主人批评过的「把正式环境搞得不专业」
- pages.dev 预览 URL（随机哈希）只用于部署过程确认，不做验收环境
