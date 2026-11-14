const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/nikki/infinity.html', { waitUntil: 'load', timeout: 45000 });
  // 分批滚动+等待
  for (let round = 0; round < 8; round++) {
    await page.evaluate((r) => { window.scrollTo(0, r * 1400); }, round);
    await page.waitForTimeout(1200);
  }
  // 等所有img至少complete
  await page.evaluate(() => Promise.all([...document.querySelectorAll('img')].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 15000); }))));
  const stat = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('img')];
    const broken = imgs.filter(i => i.naturalWidth === 0 && (i.currentSrc || i.src) && i.getBoundingClientRect().width > 0);
    return { total: imgs.length, broken: broken.length, sample: broken.slice(0, 4).map(i => i.src.slice(60, 110)) };
  });
  console.log(JSON.stringify(stat));
  await browser.close();
})();
