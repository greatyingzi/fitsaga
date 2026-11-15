/* FitSaga lightbox v2: 大图+套图组翻页+来源链接 */
(function () {
  if (window.__fsLightbox) return;
  window.__fsLightbox = true;
  var css = document.createElement('style');
  css.textContent = [
    '.fs-lb{position:fixed;inset:0;z-index:9999;background:rgba(10,7,14,.94);display:none;align-items:center;justify-content:center;flex-direction:column;padding:1rem}',
    '.fs-lb.on{display:flex}',
    '.fs-lb img{max-width:94vw;max-height:74vh;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.6)}',
    '.fs-lb .fs-lb-bar{margin-top:.7rem;display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;justify-content:center}',
    '.fs-lb a,.fs-lb button{display:inline-block;padding:.5rem .9rem;border-radius:10px;background:#2a1832;color:#fff;font-size:.88rem;border:0;cursor:pointer;min-height:44px;text-decoration:none}',
    '.fs-lb .fs-lb-x{position:absolute;top:.7rem;right:.7rem}',
    '.fs-lb .fs-lb-nav{position:absolute;top:50%;transform:translateY(-50%);font-size:1.6rem;padding:.8rem 1rem;background:#2a1832cc}',
    '.fs-lb .fs-lb-prev{left:.6rem}.fs-lb .fs-lb-next{right:.6rem}',
    '.fs-lb .fs-lb-count{color:#cbb8d4;font-size:.85rem}',
    '.fs-lb .fs-lb-cap{color:#fff;font-size:.9rem;margin-top:.3rem}',
    '.shot img.fs-err,.scard img.fs-err{opacity:.25}',
    '.shot .src-link{position:absolute;top:.5rem;right:.5rem;padding:.3rem .55rem;border-radius:8px;background:#000a;color:#fff;font-size:.72rem;z-index:3}'
  ].join('');
  document.head.appendChild(css);
  var lb = document.createElement('div');
  lb.className = 'fs-lb';
  lb.innerHTML = [
    '<button class="fs-lb-x" aria-label="关闭">✕</button>',
    '<button class="fs-lb-nav fs-lb-prev" aria-label="上一张">‹</button>',
    '<img alt="大图查看">',
    '<button class="fs-lb-nav fs-lb-next" aria-label="下一张">›</button>',
    '<div class="fs-lb-cap"></div>',
    '<div class="fs-lb-bar">',
    '<span class="fs-lb-count"></span>',
    '<a class="fs-lb-origin" target="_blank" rel="nofollow noopener">查看原始分享页 ↗</a>',
    '<a class="fs-lb-src" target="_blank" rel="nofollow noopener">作者/来源 ↗</a>',
    '<button class="fs-lb-close">关闭</button>',
    '</div>'
  ].join('');
  document.body.appendChild(lb);
  var img = lb.querySelector('img'), cap = lb.querySelector('.fs-lb-cap'),
      count = lb.querySelector('.fs-lb-count'), origin = lb.querySelector('.fs-lb-origin'),
      srcA = lb.querySelector('.fs-lb-src');
  var group = [], gi = 0;
  function render() {
    var it = group[gi];
    if (!it) return;
    img.src = it.src; img.alt = it.alt || '大图';
    cap.textContent = it.cap || '';
    count.textContent = (gi + 1) + ' / ' + group.length;
    origin.href = it.origin || '#';
    origin.style.display = it.origin ? '' : 'none';
    srcA.href = it.srcUrl || '#';
    srcA.style.display = it.srcUrl ? '' : 'none';
    var has = group.length > 1;
    lb.querySelector('.fs-lb-prev').style.display = has ? '' : 'none';
    lb.querySelector('.fs-lb-next').style.display = has ? '' : 'none';
  }
  function openWith(list, idx) { group = list; gi = idx || 0; render(); lb.classList.add('on'); document.body.style.overflow = 'hidden'; }
  function close() { lb.classList.remove('on'); document.body.style.overflow = ''; img.src = ''; group = []; }
  lb.querySelector('.fs-lb-x').addEventListener('click', close);
  lb.querySelector('.fs-lb-close').addEventListener('click', close);
  lb.querySelector('.fs-lb-prev').addEventListener('click', function () { gi = (gi - 1 + group.length) % group.length; render(); });
  lb.querySelector('.fs-lb-next').addEventListener('click', function () { gi = (gi + 1) % group.length; render(); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') lb.querySelector('.fs-lb-prev').click();
    if (e.key === 'ArrowRight') lb.querySelector('.fs-lb-next').click();
  });
  // 点击图片: 把同页同组(atlas)图聚成组
  document.addEventListener('click', function (e) {
    var im = e.target.closest ? e.target.closest('.shot img, .scard img') : null;
    if (!im) return;
    e.preventDefault();
    var fig = im.closest('figure');
    var capText = fig && fig.querySelector('.cap') ? fig.querySelector('.cap').textContent.trim() : '';
    // 组: 同figure内的兄弟不适用,用同页所有.shot img按顺序,但优先atlas分组的data-atlas
    var all = [...document.querySelectorAll('.shot img, .scard img')].filter(i => !i.classList.contains('fs-err'));
    var list = all.map(function (i) {
      var f = i.closest('figure');
      var o = f && f.querySelector('a[data-origin]');
      var s = f && f.querySelector('a[data-src]');
      return {
        src: i.currentSrc || i.src,
        alt: i.alt,
        cap: f && f.querySelector('.cap') ? f.querySelector('.cap').textContent.trim() : '',
        origin: o ? o.getAttribute('href') : (f && f.querySelector('a') ? f.querySelector('a').href : null),
        srcUrl: null
      };
    });
    var idx = all.indexOf(im);
    openWith(list, idx < 0 ? 0 : idx);
  }, true);
  // 图片onerror重试
  window.addEventListener('error', function (e) {
    var im = e.target;
    if (!(im instanceof HTMLImageElement)) return;
    if (im.dataset.retried) { im.classList.add('fs-err'); return; }
    im.dataset.retried = '1';
    var sep = im.src.indexOf('?') >= 0 ? '&' : '?';
    setTimeout(function () { im.src = im.src + sep + 'r=' + Date.now(); }, 400 + Math.random() * 800);
  }, true);
})();
