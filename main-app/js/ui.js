/* Tiny UI helpers: scroll reveal + "Which magnet do I need?" selector. No libraries.
   All text stays in the HTML (crawlable); this only adds highlight/animation. */
(function () {
  var d = document, root = d.documentElement;
  root.classList.add("js");

  /* Scroll reveal */
  var els = [].slice.call(d.querySelectorAll(".reveal"));
  if (els.length && "IntersectionObserver" in window && !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el, i) {
      if (!el.style.getPropertyValue("--d")) el.style.setProperty("--d", (i % 4) * 70 + "ms");
      io.observe(el);
    });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  /* Selector */
  var sel = d.getElementById("selector");
  if (!sel) return;
  var btns = [].slice.call(sel.querySelectorAll(".sel-opts button"));
  var grid = sel.querySelector(".selector-grid");
  var out = sel.querySelector(".sel-result");
  var items = [].slice.call(sel.querySelectorAll(".selector-item"));
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var keys = (b.getAttribute("data-pick") || "").split(" ");
      var already = b.getAttribute("aria-pressed") === "true";
      btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      items.forEach(function (it) { it.classList.remove("pick"); });
      if (already) { grid.classList.remove("has-pick"); out.classList.remove("on"); return; }
      b.setAttribute("aria-pressed", "true");
      grid.classList.add("has-pick");
      var first = null;
      items.forEach(function (it) {
        if (keys.indexOf(it.getAttribute("data-k")) > -1) { it.classList.add("pick"); if (!first) first = it; }
      });
      var names = items.filter(function (it) { return it.classList.contains("pick"); }).map(function (it) {
        return it.querySelector("h3").textContent;
      });
      var q = "My product: " + b.textContent.trim() + ". Which magnetic separator do I need, and what should I send for a quote?";
      out.innerHTML = "";
      var h = d.createElement("h3"); h.textContent = "Likely fit: " + names.join(" or ");
      var p = d.createElement("p"); p.textContent = b.getAttribute("data-why") || "";
      var ask = d.createElement("button"); ask.type = "button"; ask.className = "btn btn-expert-hero"; ask.setAttribute("data-open-magnet-expert", ""); ask.setAttribute("data-expert-q", q); ask.textContent = "Ask the Magnet Expert about this";
      var wa = d.createElement("a"); wa.className = "btn btn-wa"; wa.target = "_blank"; wa.rel = "noopener";
      wa.href = "https://wa.me/60122112522?text=" + encodeURIComponent("Hi Arrowmatics Magnets — " + q);
      wa.textContent = "WhatsApp a photo";
      out.appendChild(h); out.appendChild(p); out.appendChild(ask); out.appendChild(wa);
      out.classList.add("on");
    });
  });
})();

/* Floating Expert pill: quiet on the first screen (hero already has the CTA), visible after scrolling */
(function () {
  var fab = document.getElementById("magnets-expert-fab");
  if (!fab || !document.querySelector(".ph")) return;
  var tick = false;
  function upd() { tick = false; fab.classList.toggle("quiet", window.scrollY < 260); }
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
  upd();
})();
