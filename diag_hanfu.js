const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/style/hanfu.html', { waitUntil: 'load', timeout: 45000 });
  for (let r = 0; r < 6; r++) { await page.evaluate(x => window.scrollTo(0, x * 1200), r); await page.waitForTimeout(800); }
  await page.evaluate(() => Promise.all([...document.querySelectorAll('img')].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 12000); }))));
  const broken = await page.evaluate(() => [...document.querySelectorAll('img')].filter(i => i.naturalWidth === 0 && (i.currentSrc || i.src) && i.getBoundingClientRect().width > 0).map(i => i.src.slice(0, 90)));
  console.log(JSON.stringify(broken, null, 1));
  await browser.close();
})();
