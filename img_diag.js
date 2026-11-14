const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('https://fitsaga.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  // 滚到底触发懒加载
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
  });
  await page.waitForLoadState('networkidle').catch(()=>{});
  await page.waitForTimeout(2500);
  const res = await page.evaluate(async () => {
    const imgs = [...document.querySelectorAll('img')];
    const broken = imgs.filter(i => i.complete && i.naturalWidth === 0);
    const unloaded = imgs.filter(i => !i.complete).length;
    let probe = null;
    if (broken.length) {
      const u = broken[0].src;
      try { const r = await fetch(u, { mode: 'cors' }); probe = { u, status: r.status }; }
      catch (e) { probe = { u, err: String(e).slice(0, 80) }; }
    }
    return { total: imgs.length, broken: broken.length, unloaded, firstBroken: broken.slice(0, 3).map(i => i.src.slice(0, 90)), probe };
  });
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})();
