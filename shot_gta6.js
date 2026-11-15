const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await page.goto('https://fitsaga.pages.dev/topics/gta6-style-prompt', { waitUntil: 'networkidle', timeout: 45000 });
  await page.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/gta6_m390.png' });
  await browser.close();
  console.log('shot ok');
})();
