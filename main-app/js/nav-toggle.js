/* Mobile hamburger for the primary nav (<=768px). Progressive enhancement:
   without JS the nav simply stays visible as a compact list. */
(function () {
  'use strict';
  var root = document.documentElement;
  var btn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (!btn || !nav) return;
  root.classList.add('has-nav-js');

  var mq = window.matchMedia ? window.matchMedia('(max-width: 768px)') : null;

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    root.classList.toggle('nav-open', open);
  }

  btn.addEventListener('click', function () {
    setOpen(btn.getAttribute('aria-expanded') !== 'true');
  });
  nav.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (a) setOpen(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      btn.focus();
    }
  });
  document.addEventListener('click', function (e) {
    if (btn.getAttribute('aria-expanded') === 'true' &&
        !nav.contains(e.target) && !btn.contains(e.target)) {
      setOpen(false);
    }
  });
  if (mq) {
    var onChange = function () { if (!mq.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
})();
