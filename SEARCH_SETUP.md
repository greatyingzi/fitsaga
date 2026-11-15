# FitSaga 收录开闸操作清单（需要主人 UI 操作的部分）

## 已自动完成
- IndexNow 密钥部署: https://fitsaga.pages.dev/436382538f5c645f9cd191711968c488.txt（200）
- IndexNow 提交 25 个核心 URL → 状态 202（Bing/Yandex 已受理）
- robots.txt + sitemap.xml（968 URL）在线
- Article / ItemList JSON-LD 结构化数据全站

## 需要你做的（约 10 分钟）

### Google Search Console
1. 打开 https://search.google.com/search-console
2. 添加资源 → 网址前缀 → https://fitsaga.pages.dev
3. 所有权验证选「HTML 文件」→ 下载 googleXXXX.html 给我，我部署后你点验证
4. 验证后：站点地图 → 提交 https://fitsaga.pages.dev/sitemap.xml

### Bing 站长工具
1. https://www.bing.com/webmasters → 从 GSC 导入（最省事）
2. 验证文件 BingSiteAuth.xml 给我
3. 提交 sitemap 同 URL

### 域名（可选，但现在决定最省事）
- 候选池 10 个已验证可注册（fitsaga.com 等，约 $10-12/年 via CF Registrar）
- 定名后我执行购买+绑定+301

## 后续自动
- IndexNow 每日随流水线自动提交新增 URL（key 机制已留好）
