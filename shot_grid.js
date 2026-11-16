const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const m = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await m.goto('https://fitsaga.pages.dev/en/topics/infinity-nikki-outfit-ideas', { waitUntil: 'networkidle', timeout: 45000 });
  // 滚到主题网格区
  await m.evaluate(() => { const h3 = [...document.querySelectorAll('h3')].find(x => x.textContent.includes('Dreamy')); if (h3) h3.scrollIntoView(); });
  await m.waitForTimeout(1500);
  await m.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/nikki_grid_m390.png' });
  await browser.close();
  console.log('grid shot ok');
})();
