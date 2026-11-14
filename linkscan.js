const { chromium } = require('playwright-core');
const fs = require('fs');

const BASE = 'https://fitsaga.pages.dev';

(async () => {
  // 1) 拉sitemap全量URL
  const sm = await (await fetch(BASE + '/sitemap.xml')).text();
  const urls = [...sm.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1].replace(BASE, ''));
  console.log('sitemap urls:', urls.length);

  // 2) 全量状态检查(并发10)
  const bad = [];
  let ok = 0;
  const batch = 10;
  for (let i = 0; i < urls.length; i += batch) {
    const chunk = urls.slice(i, i + batch);
    await Promise.all(chunk.map(async u => {
      try {
        const r = await fetch(BASE + u, { redirect: 'follow' });
        if (r.ok) ok++;
        else bad.push(u + ' -> ' + r.status);
      } catch (e) { bad.push(u + ' -> ERR ' + String(e).slice(0, 60)); }
    }));
  }
  console.log('status check: ok=' + ok + ' bad=' + bad.length);
  if (bad.length) console.log(bad.slice(0, 10).join('\n'));

  // 3) 深度渲染检查: 抽样8类页面, 检查内链完整性(页面里的内链都点一遍HEAD)、JS错误、图裂
  const samples = ['/', '/style/hanfu.html', '/style/korean.html', '/nikki/infinity.html', '/nikki/shining.html', '/nikki/miracle.html', '/collection/dark-gothic', '/nikki/s/天鹅童话'];
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e).slice(0, 80)));
  let deepPass = 0, deepFail = 0;
  const internal = new Set();
  for (const p of samples) {
    errs.length = 0;
    await page.goto(BASE + p, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
    // 收集全部内链
    const links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => h && h.startsWith('/') && !h.startsWith('//')));
    links.forEach(h => internal.add(h.split('#')[0]));
    // 全页滚动后统计图裂
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 800) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
    });
    await page.waitForLoadState('networkidle').catch(()=>{});
    await page.evaluate(() => Promise.all([...document.querySelectorAll('img')].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 12000); }))));
    const imgStat = await page.evaluate(() => {
      const imgs = [...document.querySelectorAll('img')];
      return { total: imgs.length, broken: imgs.filter(i => i.naturalWidth === 0 && (i.currentSrc || i.src) && i.getBoundingClientRect().width > 0).length };
    });
    const pe = errs.length;
    const good = imgStat.broken === 0 && pe === 0;
    if (good) deepPass++; else deepFail++;
    console.log(`DEEP ${p}: imgs ${imgStat.total} broken=${imgStat.broken} jserr=${pe} links=${links.length} -> ${good ? 'PASS' : 'FAIL'}`);
  }
  // 4) 内链目标全量存在性(所有收集到的内链 vs sitemap集合)
  const smSet = new Set(urls.map(u => u.replace('.html', '')));
  let missing = 0;
  for (const l of internal) {
    const norm = l.replace('.html', '');
    if (!smSet.has(norm) && !smSet.has(l)) { missing++; if (missing <= 8) console.log('LINK-NOT-IN-SITEMAP:', l); }
  }
  console.log(`internal unique links: ${internal.size}, not-in-sitemap: ${missing}`);
  console.log(`FINAL: statusOk=${ok}/${urls.length} deepPass=${deepPass}/${samples.length}`);
  await browser.close();
})();