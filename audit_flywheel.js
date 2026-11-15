const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE_URL || 'https://fitsaga.pages.dev';
const OUT = process.env.OUT || '/Users/liheng/work/self/fitsaga/audit/' + Date.now();
const PAGES = process.env.PAGES ? process.env.PAGES.split(',') : ['/', '/style/hanfu.html', '/collection/starry-night', '/nikki/s/奶酪与剑'];
const VPS = [
  { name: 'm390', w: 390, h: 844, mobile: true },
  { name: 'd1280', w: 1280, h: 900, mobile: false },
];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  let pass = 0, fail = 0; const fails = [];
  for (const vp of VPS) {
    const ctx = await browser.newContext({
      viewport: { width: vp.w, height: vp.h },
      userAgent: vp.mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined,
      deviceScaleFactor: 2,
    });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    for (const p of PAGES) {
      const url = BASE + p;
      try { await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }); }
      catch (e) { await page.goto(url, { waitUntil: 'load', timeout: 45000 }).catch(()=>{}); }
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
        window.scrollTo(0, 0);
      });
      await page.waitForLoadState('networkidle').catch(()=>{});
      await page.waitForTimeout(2000);
      const tag = vp.name + '_' + (p === '/' ? 'home' : p.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '_').slice(0, 30));
      const shot = path.join(OUT, tag + '.png');
      await page.screenshot({ path: shot, fullPage: false });
      // 断言
      const a = await page.evaluate(() => {
        const imgs = [...document.querySelectorAll('img')];
        const broken = imgs.filter(i => (i.currentSrc || i.src) && (!i.complete || i.naturalWidth === 0)).length;
        const hOverflow = document.documentElement.scrollWidth > window.innerWidth + 2;
        const smallText = [...document.querySelectorAll('p,span,div,a,em,figcaption')].filter(el => {
          const fs = parseFloat(getComputedStyle(el).fontSize);
          const t = (el.textContent || '').trim();
          return t.length > 3 && fs < 12;
        }).length;
        const tapSmall = [...document.querySelectorAll('a,button')].filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && (r.width < 24 || r.height < 24);
        }).length;
        const visImgs = imgs.length;
        return { broken, hOverflow, smallText, tapSmall, visImgs, err: window.__errs || 0 };
      });
      const perr = errors.length;
      const checks = [
        ['brokenImgs', a.broken === 0],
        ['hOverflow', !a.hOverflow],
        ['pageError', perr === 0],
        ['tinyText', a.smallText <= 2],
        ['tapTargets', a.tapSmall <= 6],
      ];
      for (const [k, ok] of checks) {
        if (ok) pass++; else { fail++; fails.push(`${tag}:${k} ${JSON.stringify(a)} err=${perr}`); }
      }
      console.log(`${tag}: broken=${a.broken}/${a.visImgs} overflow=${a.hOverflow} small=${a.smallText} tap=${a.tapSmall} err=${perr}`);
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'summary.json'), JSON.stringify({ pass, fail, fails }, null, 2));
  console.log(`RESULT: pass=${pass} fail=${fail}`);
  if (fails.length) console.log(fails.join('\n'));
})();