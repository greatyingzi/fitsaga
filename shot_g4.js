const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const m = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  const shots = [
    ['https://fitsaga.pages.dev/en/topics/infinity-nikki-outfit-ideas', 'nikki_en_m390.png'],
    ['https://fitsaga.pages.dev/en/topics/image-prompt-techniques', 'ipt_en_m390.png'],
    ['https://fitsaga.pages.dev/collection/eye-makeup', 'collection_b2_m390.png'],
  ];
  for (const [url, name] of shots) {
    await m.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    await m.screenshot({ path: '/Users/liheng/work/self/fitsaga/audit/' + name });
    console.log('shot:', name);
  }
  await browser.close();
})();
