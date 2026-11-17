const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const m = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('https://fitsaga.pages.dev/topics/ai-fashion-failure-atlas', { waitUntil: 'networkidle', timeout: 45000 });
  await m.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/deep_atlas_m390.png' });
  console.log('deep shot ok');
  await browser.close();
})();
