/**
 * Light photo motion helpers for magnets.com.my
 * - Staggered fade-up on gallery figures + product cards (IntersectionObserver)
 * - Respects prefers-reduced-motion
 */
(function () {
  'use strict';

  var reduce = false;
  try {
    reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  var nodes = document.querySelectorAll('.photo-grid figure, .grid-3 > .card');
  if (!nodes.length) return;

  function showAll() {
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].classList.add('photo-fx-reveal', 'is-in');
    }
  }

  if (reduce || !('IntersectionObserver' in window)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(
    function (entries) {
      for (var i = 0; i < entries.length; i++) {
        var entry = entries[i];
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      }
    },
    { rootMargin: '0px 0px -6% 0px', threshold: 0.1 }
  );

  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    el.classList.add('photo-fx-reveal');
    el.style.setProperty('--fx-delay', (i % 6) * 70 + 'ms');
    io.observe(el);
  }
})();
