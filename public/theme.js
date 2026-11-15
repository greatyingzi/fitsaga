/* FitSaga theme switcher: dark(default) / light, localStorage persist */
(function () {
  if (window.__fsTheme) return;
  window.__fsTheme = true;
  var css = document.createElement('style');
  css.textContent = [
    'html[data-theme="light"] body{background:#f7f3f8;color:#2b2233}',
    'html[data-theme="light"] .hero{background:radial-gradient(1200px 600px at 20% 10%,rgba(255,126,179,.18),transparent 60%),radial-gradient(1000px 500px at 80% 20%,rgba(181,84,140,.2),transparent 60%),#f7f3f8}',
    'html[data-theme="light"] .hero h1{background:linear-gradient(90deg,#e8608a,#a855f7,#5b8def);-webkit-background-clip:text;background-clip:text}',
    'html[data-theme="light"] .hero .sub{color:#7a6b80}',
    'html[data-theme="light"] .shot{box-shadow:0 6px 20px rgba(43,34,51,.15);background:#fff}',
    'html[data-theme="light"] .scard{background:#fff;box-shadow:0 4px 14px rgba(43,34,51,.12)}',
    'html[data-theme="light"] .sec{color:#2b2233}',
    'html[data-theme="light"] .sec-head p{color:#5a4d63!important}',
    'html[data-theme="light"] .intro{color:#5a4d63}',
    'html[data-theme="light"] .chip{color:#2b2233;opacity:1}',
    'html[data-theme="light"] footer{background:#efe9f2;color:#7a6b80}',
    'html[data-theme="light"] .gwrap p,html[data-theme="light"] .twrap p{color:#3a3040}',
    'html[data-theme="light"] .gwrap .formula,html[data-theme="light"] .gwrap details,html[data-theme="light"] .twrap details,html[data-theme="light"] .twrap pre{background:#fff;border-color:#e0d5e8}',
    'html[data-theme="light"] .twrap pre code{color:#5b8def}',
    'html[data-theme="light"] .fs-sb-box{background:#fff}',
    'html[data-theme="light"] .fs-sb-item{color:#2b2233}',
    'html[data-theme="light"] .fs-sb-item:hover,html[data-theme="light"] .fs-sb-item.sel{background:#f0e5f5}',
    '.fs-theme-btn{position:fixed;right:1rem;bottom:6.8rem;z-index:9998;width:44px;height:44px;border-radius:50%;background:#2a1832;border:1px solid #4a3a55;color:#ffd9a8;font-size:1.05rem;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.4)}',
    'html[data-theme="light"] .fs-theme-btn{background:#fff;color:#a855f7}'
  ].join('');
  document.head.appendChild(css);
  function set(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem('fs-theme', t); } catch (e) {}
    btn.textContent = t === 'light' ? '🌙' : '☀️';
  }
  var btn = document.createElement('button');
  btn.className = 'fs-theme-btn';
  btn.setAttribute('aria-label', '切换主题');
  var saved = 'dark';
  try { saved = localStorage.getItem('fs-theme') || 'dark'; } catch (e) {}
  set(saved);
  btn.addEventListener('click', function () {
    set(document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
  });
  document.body.appendChild(btn);
})();
