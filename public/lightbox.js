/* FitSaga lightbox: 点击图片站内大图查看 */
(function () {
  if (window.__fsLightbox) return;
  window.__fsLightbox = true;
  var css = document.createElement('style');
  css.textContent = [
    '.fs-lb{position:fixed;inset:0;z-index:9999;background:rgba(10,7,14,.92);display:none;align-items:center;justify-content:center;flex-direction:column;padding:1rem}',
    '.fs-lb.on{display:flex}',
    '.fs-lb img{max-width:94vw;max-height:78vh;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.6)}',
    '.fs-lb .fs-lb-bar{margin-top:.8rem;display:flex;gap:.7rem;align-items:center;flex-wrap:wrap;justify-content:center}',
    '.fs-lb a,.fs-lb button{display:inline-block;padding:.55rem 1rem;border-radius:10px;background:#2a1832;color:#fff;font-size:.9rem;border:0;cursor:pointer;min-height:44px}',
    '.fs-lb .fs-lb-x{position:absolute;top:.8rem;right:.8rem;padding:.55rem .8rem}'
  ].join('');
  document.head.appendChild(css);
  var lb = document.createElement('div');
  lb.className = 'fs-lb';
  lb.innerHTML = '<button class="fs-lb-x" aria-label="关闭">✕ 关闭</button><img alt="大图查看"><div class="fs-lb-bar"><a class="fs-lb-origin" target="_blank" rel="nofollow noopener">查看原始分享页 ↗</a><button class="fs-lb-close">关闭</button></div>';
  document.body.appendChild(lb);
  var img = lb.querySelector('img'), origin = lb.querySelector('.fs-lb-origin');
  function open(src, href, alt) {
    img.src = src; img.alt = alt || '大图';
    if (href) { origin.href = href; origin.style.display = ''; } else origin.style.display = 'none';
    lb.classList.add('on');
    document.body.style.overflow = 'hidden';
  }
  function close() { lb.classList.remove('on'); document.body.style.overflow = ''; img.src = ''; }
  lb.querySelector('.fs-lb-x').addEventListener('click', close);
  lb.querySelector('.fs-lb-close').addEventListener('click', close);
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  // 全站图片onerror重试一次(换cache-buster) + 失败占位样式
  var retryCss = document.createElement('style');
  retryCss.textContent = '.shot img.fs-err,.scard img.fs-err{opacity:.25}';
  document.head.appendChild(retryCss);
  window.addEventListener('error', function (e) {
    var im = e.target;
    if (!(im instanceof HTMLImageElement)) return;
    if (im.dataset.retried) { im.classList.add('fs-err'); return; }
    im.dataset.retried = '1';
    var sep = im.src.indexOf('?') >= 0 ? '&' : '?';
    setTimeout(function () { im.src = im.src + sep + 'r=' + Date.now(); }, 400 + Math.random() * 800);
  }, true);
  document.addEventListener('click', function (e) {
    var im = e.target.closest ? e.target.closest('.shot img, .scard img') : null;
    if (!im) return;
    e.preventDefault();
    var a = im.closest('a');
    open(im.currentSrc || im.src, a ? a.href : null, im.alt);
  }, true);
})();