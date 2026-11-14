const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/nikki/infinity.html', { waitUntil: 'networkidle', timeout: 45000 });
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 900) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } });
  await page.waitForLoadState('networkidle').catch(()=>{});
  await page.waitForTimeout(2000);
  const brokenUrls = await page.evaluate(() => [...document.querySelectorAll('img')].filter(i => i.naturalWidth === 0 && (i.currentSrc || i.src) && i.getBoundingClientRect().width > 0).map(i => i.src));
  console.log('broken count:', brokenUrls.length);
  console.log(brokenUrls.slice(0, 6).join('\n'));
  await browser.close();
  process.stdout.write('URLS\\n' + JSON.stringify(brokenUrls));
})();
