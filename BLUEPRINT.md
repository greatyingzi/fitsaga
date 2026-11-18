# FitSaga P0 信息架构蓝图 v1

> 临时域名 fitsaga.pages.dev 已上线；正式域名待创意定型后从候选池（fitsaga.com/glamfolio.com/dapeiwoo.com 等10个，均已验证可注册）购买。
> 定位：**不做更多图片的网站，做把图片变成结构、把结构变成故事、把故事变成"我想成为她"的机器。**

## 一、URL 结构与页面模板

### 模板 A：风格频道页 /style/<风格>
- 路由：/style/hanfu | /style/sexy | /style/sweet | /style/jk | /style/qipao | /style/street | /style/commute | /style/korean | /style/japanese
- 内容：该风格定义(一段真人向导语) + 筛选器(场合TPO/季节/色系/身高段) + 瀑布流(结构化元数据卡)
- SEO：每风格一篇 800-1500 字原创导语(风格史/关键单品/避坑)，图片带完整 alt
- 数据源：Musinsa(自带风格标签) + WEAR(tag_ids) + 堆糖(kw搜索)

### 模板 B：策展合集页 /collection/<slug>
- 例：/collection/和风婚纱十选 | /collection/秋冬汉服叠穿 | /collection/小个子显高搭配
- 内容：策展导语 + 10-30 张精选图(每张一行策展人评语) + 相关合集互链
- SEO：主题词长尾主战场；每页必须有人类策展逻辑(避免 thin content 判定)
- 生成方式：AI 初选 + 人工确认开关(先全自动+抽样质检)

### 模板 C：套装详情页 /nikki/<套装名slug>
- 数据：BWIKI/Fandom 结构化(套装名/部件清单/海报图/展示图/获取途径/活动期)
- SEO：套装名/活动名长尾，现有供给(灰机403/BWIKI体验差)存在缺口
- 关联：同风格套装推荐 + "现实穿搭同款灵感"(接模板A的图)

### 系统页
- / 首页：六风格色系板块(已上线) + 今日合集 + 热门套装
- /about 版权说明(热链模式+侵权即删通道) —— 合规基建，必须页
- sitemap.xml 分片：styles/collections/nikki 各一片

## 二、数据模型(四表)

items: id, source(duitang/wear/musinsa/...), origin_url(原页面), img_url(原图直链), proxy_url(白标代理路径), w, h, tags[](风格/场合/季节), colors[](主色), license(低/中/中高), author, aigc_label, phash(去重), quality_score, created_at

collections: id, slug, title, style_key, curator_note, item_ids[], cover_item_id, published_at

suits: id, name_zh, name_en, game(nikki3/nikkii4/shining/infinity), parts[], poster_img, showcase_imgs[], source(bwiki/fandom page), obtain, event, style_tags[]

tags: key, name_zh, name_en, aliases[], type(style/occasion/season/color)

## 三、图片代理(已验证方案)

- 短期：wsrv.nl 免费转发(堆糖已验证200+自动webp)
- 正式：自建 CF Worker /img/<hash>?w=800&fmt=avif，服务端带 UA/Referer 回源，immutable 缓存；路径签名+TTL 做白标
- 全量图不入库落盘：元数据入库+热链(合规姿势)；绿灯源(Unsplash/Commons)可额外缓存

## 四、第一批 20 个合集选题(策展日历)

古风线: 1.汉服婚服十选 2.秋冬汉服叠穿图鉴 3.齐胸vs齐腰襦裙对比 4.新中式通勤穿搭
优雅线: 5.旗袍的现代穿法 6.小个子旗袍显高指南
甜美线: 7.马卡龙色系一周穿搭 8.初恋感日系搭配
辣妹线: 9.性感不擦边的边界示范 10.辣妹秋冬羽绒服搭配
青春线: 11.JK制服格裙入门图谱 12.JK×外套秋冬叠穿
潮流线: 13.巴黎世家风街拍解析 14.美式复古Y2K回归
游戏线: 15.无限暖暖和风套装Top10 16.奇迹暖暖限定婚纱图鉴 17.闪耀暖暖3D展示合集 18.暖暖×现实平替穿搭对照
通勤线: 19.Uniqlo胶囊衣橱搭配 20.ZARA新品周更榜单

## 五、合规与质量关卡(打标流水线)

1. pHash 去重 → 2. 分辨率/清晰度过滤 → 3. 人脸完整度检测(保留"有完整人像") → 4. 尺度分级(性感板块卡在"时尚大片"档，AdSense 安全) → 5. 版权字段强制(license/author/origin_url 三字段缺失不入库) → 6. 自动署名渲染("图源:堆糖 @作者")

## 六、里程碑

M1(本周): Musinsa+堆糖采集器跑通 → items 入库1万张 → 首页+2个风格频道页上线
M2: BWIKI 套装采集 → nikki 详情页500个 → 合集页10个
M3: 图片代理白标切换 → sitemap 提交 GSC/Bing → 图片 SEO 基建(alt/image sitemap)
M4: 端侧试穿 demo(档1贴图) → AI remix 云端版(档3,按次付费)验证付费意愿


---

## 七、内容体系现状（2026-11-17 更新）

**定位升级**：不只是「图片→结构→故事」，而是双层内容体系：
- **教程层**：23 篇双语专题（形制/光线/面料/prompt 公式 + 68 组正反例对照图 + prompt 复制块 + 参考图包下载）
- **洞察层**：30 篇数据驱动深度长文（方法论实验室 /deep-lab.html，7 分组）

**内容来源三条线**：①数据驱动（站内图库/实验/套装统计）②问题驱动（Google suggest问题型词→选题，只找空白不量化需求，见 how-we-research-reader-questions）③热点驱动（雷达草稿池→游戏/短剧专题）。

**深度内容的护城河逻辑**：数据别人没有（4,547 图库 / 1,587 套装 / 68 组对照实验 / 132 海外搜索词）+ 框架原创（失败模式图鉴 / prompt 语法学 / 塑料感三因 / 1秒可读性 / 半衰期 / 边界条件…）——不可速成、不可爬取。

**资产规模**：50 合集 + 23 双语专题 + 30 深度文 + 10 决策文 + EN 套装 hub（235 套 / 18 主题）+ 933 套装页 + sitemap 1,068+ URL。

**关键基建**：
- 双环境：test 分支 → fitsaga-dev（staging）；main 分支 → fitsaga（prod，注意 CF 生产分支名 = main，与 git master 解耦）
- action proxy：ops-runner 公共仓 proxy.yml + 私有 hub data-core-01 的 sites.json；cfut OAuth token 无 DNS 权限，DNS 用 ~/.hermes/.env 的 CLOUDFLARE_DNS_TOKEN
- 图片路径：热链 + meta referrer no-referrer；R2 缓存经 img.depthsnap.com 自有域（绕开 workers.dev 风控——该账号 workers.dev 全量 1101，与内容无关，纯 Hello World 也中招）
- 验证工具：audit_flywheel.js（40 场景）+ linkscan.js；curl 验线上必须下载到文件再 grep（管道 grep 会因引号转义假 0）

**待用户输入**：GSC token / 正式域名定名 / 花瓣 cookie（均有文档占位）。
