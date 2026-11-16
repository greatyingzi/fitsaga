# 花瓣网接入操作指南（主人一次性操作，约 3 分钟）

## 为什么需要你操作一次
花瓣网用腾讯 EdgeOne 两层防护：
1. 第一层：JS 混淆算 cookie（__tst_status）—— 我可以程序复算
2. 第二层：滑块验证码 —— 必须真浏览器过一次

你的浏览器访问 huaban.com 过一次滑块后，cookie 有效约 30 分钟（tads_cap ticket），
我把 cookie 导入采集器就能批量抓（分类页/boards JSON 大多能直接过）。

## 操作步骤
1. 浏览器打开 https://huaban.com/favorite/apparel
2. 如果出现滑块验证 → 拖过去完成
3. F12 → Application → Cookies → https://huaban.com
4. 把这几个 cookie 的值复制给我（或导出整行）：
   - __tst_status
   - tads_cap_ticket（如果有）
   - 其他 baidu/EO 相关的都带上更稳

## 我拿到 cookie 后做什么
- collector/huaban.py 加 cookie 头
- 抓 31 个分类页（女装搭配/美女/造型美妆...）× 20 pin/页
- 图片即时下载原图存本地（auth_key 时效，不能热链）
- 预计首批 500-1000 张高审美图入库

## 注意
- cookie 过期后（约 30 分钟~几小时）需要你再解锁一次
- 长期方案：低频抓取（3s+间隔）+ 每次只抓增量，减少触发滑块频率
