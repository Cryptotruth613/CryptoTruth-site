/* CryptoTruth site script. Runs entirely in the visitor's browser; sends nothing anywhere. */
(function () {
  /* Phone menu */
  var mb = document.getElementById('menu-btn'), nav = document.getElementById('main-nav');
  if (mb && nav) {
    mb.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
      mb.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* Copy link button on posts */
  var btn = document.getElementById('copy-link'), out = document.getElementById('copied');
  if (btn && out) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-url') || location.href;
      try {
        navigator.clipboard.writeText(url).then(
          function () { out.textContent = 'Link copied: ' + url; },
          function () { out.textContent = url; }
        );
      } catch (e) { out.textContent = url; }
    });
  }

  /* Word rain (home page only) */
  var c = document.getElementById('rain');
  if (!c) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var words = ['SATS','HODL','Nakamoto','TRUTH','FirstPrinciples','SelfCustody','21M','SOUND','MONEY','Node','Halving','Keys','FREE','BTC','Satoshi','CryptoTruth','NoShills','Signal'];
  var ctx = c.getContext('2d');
  var cols = [], step = 16, colW = 70, W = 0, H = 0;
  function pick() { return words[(Math.random() * words.length) | 0]; }
  function size() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = c.clientWidth; H = c.clientHeight;
    c.width = W * dpr; c.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
    cols = [];
    for (var k = 0; k < Math.ceil(W / colW); k++) cols.push({ y: Math.random() * H, speed: 0.5 + Math.random() * 0.9, word: pick() });
  }
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.09)';
    ctx.fillRect(0, 0, W, H);
    ctx.font = '10px ui-monospace, Consolas, monospace';
    for (var k = 0; k < cols.length; k++) {
      var col = cols[k];
      ctx.fillStyle = 'rgba(255,217,0,' + (0.12 + Math.random() * 0.25).toFixed(2) + ')';
      ctx.fillText(Math.random() < 0.2 ? pick() : col.word, k * colW + 6, col.y);
      col.y += step * col.speed;
      if (col.y > H + 20) { col.y = -Math.random() * 200; col.word = pick(); col.speed = 0.5 + Math.random() * 0.9; }
    }
  }
  size();
  window.addEventListener('resize', size);
  if (reduce) { for (var s = 0; s < 60; s++) draw(); return; }
  var last = 0;
  (function loop(t) {
    if (t - last > 110) { draw(); last = t; }
    requestAnimationFrame(loop);
  })(0);
})();
