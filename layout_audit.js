const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  // 桌面全页截图(看整体布局权重)
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 })).newPage();
  await page.goto('https://fitsaga.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/home_desktop_full.png', fullPage: true });
  // 量一下各板块的位置权重
  const layout = await page.evaluate(() => {
    const secs = [...document.querySelectorAll('section')];
    return secs.map(s => ({
      id: s.id || s.querySelector('h2')?.textContent?.slice(0,12) || 'hero',
      top: Math.round(s.getBoundingClientRect().top + window.scrollY),
      h: Math.round(s.getBoundingClientRect().height)
    }));
  });
  console.log(JSON.stringify(layout, null, 1));
  await browser.close();
})();
