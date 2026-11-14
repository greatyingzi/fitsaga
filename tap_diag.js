const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await page.goto('https://fitsaga.pages.dev/', { waitUntil: 'networkidle', timeout: 45000 });
  const els = await page.evaluate(() => {
    return [...document.querySelectorAll('a,button')]
      .map(el => ({ t: (el.textContent || '').trim().slice(0, 16), ...el.getBoundingClientRect().toJSON(), tag: el.tagName }))
      .filter(e => e.width > 0 && (e.width < 24 || e.height < 24));
  });
  console.log(JSON.stringify(els, null, 1));
  await browser.close();
})();
