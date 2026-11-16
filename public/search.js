/* FitSaga site search: floating palette, pure client-side */
(function () {
  if (window.__fsSearch) return;
  window.__fsSearch = true;
  var css = document.createElement('style');
  css.textContent = [
    '.fs-sb{position:fixed;inset:0;z-index:10000;background:rgba(10,7,14,.9);display:none;align-items:flex-start;justify-content:center;padding-top:12vh}',
    '.fs-sb.on{display:flex}',
    '.fs-sb-box{width:min(92vw,560px);background:#1a1420;border:1px solid #3a2a44;border-radius:16px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.6)}',
    '.fs-sb-box input{width:100%;padding:1rem 1.1rem;background:transparent;border:0;outline:0;color:#fff;font-size:1rem;border-bottom:1px solid #3a2a44;box-sizing:border-box}',
    '.fs-sb-res{max-height:50vh;overflow-y:auto}',
    '.fs-sb-item{display:block;padding:.7rem 1.1rem;border-bottom:1px solid #241b2c;color:#e8dff0;text-decoration:none;cursor:pointer}',
    '.fs-sb-item:hover,.fs-sb-item.sel{background:#2a1832}',
    '.fs-sb-item .sc{font-size:.72rem;color:#a855f7;margin-right:.5rem}',
    '.fs-sb-item .st{font-size:.92rem}',
    '.fs-sb-hint{padding:.5rem 1.1rem;font-size:.75rem;color:#9d8fa8}'
  ].join('');
  document.head.appendChild(css);
  var wrap = document.createElement('div');
  wrap.className = 'fs-sb';
  wrap.innerHTML = '<div class="fs-sb-box"><input placeholder="搜索风格 / 合集 / 套装 / 文章…（ESC 关闭）"><div class="fs-sb-res"></div><div class="fs-sb-hint">↑↓ 选择 · Enter 打开 · ESC 关闭</div></div>';
  document.body.appendChild(wrap);
  var input = wrap.querySelector('input'), res = wrap.querySelector('.fs-sb-res');
  var DATA = null, sel = 0, cur = [];
  function load(cb) {
    if (DATA) return cb();
    fetch('/search-index.json').then(r => r.json()).then(d => { DATA = d; cb(); });
  }
  var _lastQ = "";
  function hl(t) {
    if (!_lastQ) return t;
    var words = _lastQ.toLowerCase().split(/\s+/).filter(function (w) { return w; });
    var out = t;
    for (var i = 0; i < words.length; i++) {
      var rx = new RegExp("(" + words[i].replace(/[.*+?^${}()|[\]\\]/g, "\\\$&") + ")", "gi");
      out = out.replace(rx, "<mark style=\"background:#a855f7;color:#fff;border-radius:3px\">$1</mark>");
    }
    return out;
  }
  function render(items) {
    cur = items.slice(0, 12); sel = 0;
    res.innerHTML = cur.map((it, i) =>
      '<a class="fs-sb-item' + (i === 0 ? ' sel' : '') + '" href="' + it.u + '"><span class="sc">' + it.c + '</span><span class="st">' + hl(it.t) + '</span></a>').join('');
  }
  function query(q) {
    if (!q) return render([]);
    var words = q.toLowerCase().split(/\s+/).filter(function (w) { return w; });
    var scored = [];
    for (var i = 0; i < DATA.length; i++) {
      var t = DATA[i].t.toLowerCase();
      var c = (DATA[i].c || "").toLowerCase();
      var all = t + " " + c;
      var ok = true, firstAt = 99;
      for (var j = 0; j < words.length; j++) {
        var idx = all.indexOf(words[j]);
        if (idx < 0) { ok = false; break; }
        if (idx < firstAt) firstAt = idx;
      }
      if (ok) scored.push([firstAt === 0 ? 0 : 1, i]);
    }
    scored.sort(function (a, b) { return a[0] - b[0]; });
    render(scored.slice(0, 12).map(function (x) { return DATA[x[1]]; }));
  }
  function open() { wrap.classList.add('on'); load(function(){ input.focus(); query(input.value); }); }
  function close() { wrap.classList.remove('on'); }
  // 触发: Ctrl+K / 长按? 简单: 右下角浮动按钮 + 快捷键
  var fab = document.createElement('button');
  fab.innerHTML = '🔍';
  fab.style.cssText = 'position:fixed;right:1rem;bottom:5.2rem;z-index:9998;width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#ff7eb3,#a855f7);border:0;color:#fff;font-size:1.1rem;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.5)';
  fab.addEventListener('click', open);
  document.body.appendChild(fab);
  wrap.addEventListener('click', function (e) { if (e.target === wrap) close(); });
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); open(); return; }
    if (!wrap.classList.contains('on')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, cur.length - 1); highlight(); e.preventDefault(); }
    if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); highlight(); e.preventDefault(); }
    if (e.key === 'Enter' && cur[sel]) location.href = cur[sel].u;
  });
  function highlight() {
    var els = res.querySelectorAll('.fs-sb-item');
    els.forEach(function (el, i) { el.classList.toggle('sel', i === sel); });
  }
  input.addEventListener('input', function () { _lastQ = input.value.trim(); query(_lastQ); });
})();
