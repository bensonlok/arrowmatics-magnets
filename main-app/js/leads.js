/* Lead forms + privacy-friendly event hooks. No third-party code. No cookies.
   Test mode: add ?leadtest=1 to any URL — forms validate and show the success state but nothing is sent. */
(function () {
  var C = window.MAGNETS || { wa: "60122112522", waDisplay: "+60 12-211 2522", email: "arrowmatics@gmail.com", leadEndpoint: "/api/lead" };
  var T = function (n, p) { if (window.magnetsTrack) window.magnetsTrack(n, p); };
  var testMode = /[?&]leadtest=1\b/.test(location.search);

  /* ---- click tracking (delegated) ---- */
  document.addEventListener("click", function (ev) {
    var t = ev.target;
    var el = t.closest ? t.closest("a,button") : null;
    if (!el) return;
    var href = el.getAttribute("href") || "";
    if (el.hasAttribute("data-track")) return T(el.getAttribute("data-track"), { label: (el.textContent || "").trim().slice(0, 40) });
    if (/wa\.me\//.test(href)) return T("cta_whatsapp", { label: (el.textContent || "").trim().slice(0, 40) });
    if (/^tel:/.test(href)) return T("cta_call", {});
    if (/^mailto:/.test(href)) return T("cta_email", {});
    if (el.hasAttribute("data-open-magnet-expert")) return T("cta_expert", { label: (el.textContent || "").trim().slice(0, 40) });
    if (el.hasAttribute("data-pick")) return T("selector_use", { pick: (el.getAttribute("data-pick") || "").slice(0, 40) });
  }, true);

  /* ---- forms ---- */
  function compress(file, cb) {
    if (!file) return cb("");
    if (!/^image\//.test(file.type)) return cb("");
    var fr = new FileReader();
    fr.onerror = function () { cb(""); };
    fr.onload = function () {
      var img = new Image();
      img.onerror = function () { cb(""); };
      img.onload = function () {
        var max = 1100, w = img.width, h = img.height, s = Math.min(1, max / Math.max(w, h));
        var c = document.createElement("canvas"); c.width = Math.round(w * s); c.height = Math.round(h * s);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        var q = 0.72, out = c.toDataURL("image/jpeg", q);
        while (out.length > 650000 && q > 0.35) { q -= 0.12; out = c.toDataURL("image/jpeg", q); }
        cb(out.length < 800000 ? out : "");
      };
      img.src = fr.result;
    };
    fr.readAsDataURL(file);
  }
  function waLink(text) { return "https://wa.me/" + C.wa + "?text=" + encodeURIComponent(text); }

  function wire(form) {
    var kind = form.getAttribute("data-lead-form");
    var msg = form.querySelector(".form-msg");
    var btn = form.querySelector("button[type=submit]");
    var started = false;
    function say(html, cls) { msg.className = "form-msg " + (cls || ""); msg.innerHTML = html; }
    form.addEventListener("focusin", function () { if (!started) { started = true; T("form_start", { form: kind }); } });
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var f = form.elements;
      var name = (f.name.value || "").trim();
      var consent = f.consent && f.consent.checked;
      var body = { kind: kind, name: name, consent: !!consent, website: f.website ? f.website.value : "", page: location.pathname, context: form.getAttribute("data-context") || "", test: testMode };
      if (kind === "quote") {
        var c = (f.contact.value || "").trim();
        if (/@/.test(c)) body.email = c; else body.phone = c;
        body.message = (f.message.value || "").trim();
      } else {
        body.email = (f.email.value || "").trim();
        body.phone = f.phone ? (f.phone.value || "").trim() : "";
      }
      if (!name) { say("Please enter your name.", "err"); f.name.focus(); return; }
      if (kind === "quote" && !(body.email || body.phone)) { say("Please give a WhatsApp number or email.", "err"); f.contact.focus(); return; }
      if (kind === "quote" && body.message.length < 5) { say("Please tell us briefly what you need.", "err"); f.message.focus(); return; }
      if (kind === "checklist" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(body.email)) { say("Please enter a valid email.", "err"); f.email.focus(); return; }
      if (!consent) { say("Please tick the consent box so we may reply.", "err"); f.consent.focus(); return; }
      btn.disabled = true; say(testMode ? "Test mode: checking only, nothing will be sent…" : "Sending…", "");
      var file = f.photo && f.photo.files && f.photo.files[0];
      compress(file, function (photo) {
        if (photo) body.photo = photo;
        fetch(C.leadEndpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
          .then(function (r) { return r.json().catch(function () { return { ok: false, error: "Unexpected reply." }; }).then(function (j) { return { s: r.status, j: j }; }); })
          .then(function (x) {
            btn.disabled = false;
            if (!x.j.ok) { say(x.j.error || "Sorry, something went wrong.", "err"); T("form_error", { form: kind }); return; }
            T("form_submit", { form: kind, test: !!x.j.test });
            if (kind === "checklist") {
              form.querySelector(".form-done").hidden = false;
              say(testMode ? "Test mode OK (nothing sent). The downloads are below." : "Thanks. Your checklist is below.", "ok");
              T("checklist_unlocked", {});
            } else if (x.j.test) {
              say("Test mode OK. Nothing was sent.", "ok");
            } else if (x.j.delivered) {
              say("Thanks. We have your request and aim to reply within 1–3 hours (Malaysia business hours). To speed things up you can also <a href=\"" + waLink("Hi, I just sent a quote request on magnets.com.my. My name is " + name + ".") + "\" target=\"_blank\" rel=\"noopener\">message us on WhatsApp</a>.", "ok");
              form.reset();
            } else {
              say("We could not confirm delivery automatically. Please <a href=\"" + waLink("Hi, I need a quote. " + body.message) + "\" target=\"_blank\" rel=\"noopener\">send this on WhatsApp</a> or email <a href=\"mailto:" + C.email + "?subject=Quote%20request&body=" + encodeURIComponent(body.message || "") + "\">" + C.email + "</a>.", "warn");
            }
          })
          .catch(function () {
            btn.disabled = false;
            if (kind === "checklist" && testMode) { form.querySelector(".form-done").hidden = false; return say("Test mode: endpoint unreachable locally; showing downloads.", "ok"); }
            say("Network problem. Please <a href=\"" + waLink("Hi, I need a quote. " + (body.message || "")) + "\" target=\"_blank\" rel=\"noopener\">use WhatsApp</a> or email <a href=\"mailto:" + C.email + "\">" + C.email + "</a>.", "warn");
          });
      });
    });
  }
  var forms = document.querySelectorAll("form[data-lead-form]");
  for (var i = 0; i < forms.length; i++) wire(forms[i]);
})();
