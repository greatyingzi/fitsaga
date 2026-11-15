const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await page.goto('https://fitsaga.pages.dev/guide/laoqianfeng-ruwen', { waitUntil: 'networkidle', timeout: 45000 });
  await page.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/guide_m390.png' });
  const page2 = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await page2.goto('https://fitsaga.pages.dev/ai.html', { waitUntil: 'networkidle', timeout: 45000 });
  await page2.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/ai_m390.png' });
  await browser.close();
  console.log('shots done');
})();
