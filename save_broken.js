const { chromium } = require('playwright-core');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/nikki/infinity.html', { waitUntil: 'load', timeout: 45000 });
  for (let round = 0; round < 8; round++) { await page.evaluate(r => window.scrollTo(0, r * 1400), round); await page.waitForTimeout(1200); }
  await page.evaluate(() => Promise.all([...document.querySelectorAll('img')].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 15000); }))));
  const broken = await page.evaluate(() => [...document.querySelectorAll('img')].filter(i => i.naturalWidth === 0 && (i.currentSrc || i.src) && i.getBoundingClientRect().width > 0).map(i => i.src));
  fs.writeFileSync('/tmp/broken_urls.json', JSON.stringify(broken));
  console.log('saved', broken.length);
  await browser.close();
})();
