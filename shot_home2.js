const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await page.goto('https://fitsaga-dev.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/home_v2_m390.png' });
  await browser.close();
  console.log('shot ok');
})();
