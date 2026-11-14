const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/nikki/s/天鹅童话', { waitUntil: 'networkidle', timeout: 45000 });
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 800) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } });
  await page.waitForLoadState('networkidle').catch(()=>{});
  const res = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('img')];
    return imgs.map(i => ({ src: (i.currentSrc || i.src || '(empty)').slice(0, 70), complete: i.complete, nw: i.naturalWidth, w: i.getBoundingClientRect().width }));
  });
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})();
