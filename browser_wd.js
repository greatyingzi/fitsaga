const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext()).newPage();
  for (const u of ['https://videoapp.924068818.workers.dev/','https://fitsaga-r2.924068818.workers.dev/r2/hot1.webp']) {
    try {
      const r = await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 30000 });
      const body = await page.content();
      console.log(u.split('/')[2], '->', r.status(), '|', body.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').slice(0,120));
    } catch (e) { console.log(u, 'ERR', e.message.slice(0,60)); }
  }
  await browser.close();
})();
