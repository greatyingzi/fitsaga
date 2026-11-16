const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const m = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('https://fitsaga.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  await m.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/home_v3_m390.png' });
  const d = await (await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 })).newPage();
  await d.goto('https://fitsaga.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  await d.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/home_v3_d1280.png' });
  await browser.close();
  console.log('shots ok');
})();
