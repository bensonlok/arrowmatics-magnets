/* Single place for contact constants + the privacy-friendly event hook.
   To swap the WhatsApp number everywhere (HTML, schema, llms files): python3 scripts/swap_whatsapp.py <old digits> <new digits>
   Then update `wa` / `waDisplay` below. */
window.MAGNETS = {
  wa: "60122112522",
  waDisplay: "+60 12-211 2522",
  office: "+60196626522",
  email: "arrowmatics@gmail.com",
  leadEndpoint: "/api/lead",
  /* Optional first-party event endpoint. Leave empty: no network call is made. */
  eventEndpoint: "",
  /* Google Ads conversion send_to labels (account 196-515-5441 / tag AW-1067610456). */
  awConversions: {
    cta_whatsapp: "AW-1067610456/AEt2CJ73wJ4dENjiif0D",
    cta_call: "AW-1067610456/_r-nCKH3wJ4dENjiif0D",
    quote_form: "AW-1067610456/jusWCJv3wJ4dENjiif0D"
  }
};
/* magnetsTrack(name, props, opts):
   Emits DOM event "magnets:event". Forwards to dataLayer / plausible / gtag unless Do Not Track.
   opts.callback — invoked after the Google Ads conversion ping (or immediately if skipped).
   Beacon transport so wa.me / tel: navigation is never blocked. */
window.magnetsTrack = function (name, props, opts) {
  opts = opts || {};
  var cb = typeof opts.callback === "function" ? opts.callback : null;
  var called = false;
  var done = function () {
    if (called || !cb) return;
    called = true;
    try { cb(); } catch (e) {}
  };
  try {
    props = props || {};
    props.page = location.pathname;
    document.dispatchEvent(new CustomEvent("magnets:event", { detail: { name: name, props: props } }));
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1") { done(); return; }
    if (window.dataLayer && window.dataLayer.push) window.dataLayer.push(Object.assign({ event: name }, props));
    if (typeof window.plausible === "function") window.plausible(name, { props: props });
    if (typeof window.gtag === "function") {
      window.gtag("event", name, props);
      /* Google Ads conversions (AW-1067610456). Do NOT tag "Submit lead forms" — it would double-count Quote form. */
      var AW = (window.MAGNETS && window.MAGNETS.awConversions) || {};
      var to = AW[name];
      if (name === "form_submit" && props.form === "quote" && !props.test) to = AW.quote_form;
      if (to) {
        var payload = { send_to: to, transport_type: "beacon" };
        if (cb) payload.event_callback = done;
        window.gtag("event", "conversion", payload);
        if (cb) return; /* caller also sets a timeout fallback */
      }
    }
    var ep = window.MAGNETS && window.MAGNETS.eventEndpoint;
    if (ep && navigator.sendBeacon) navigator.sendBeacon(ep, JSON.stringify({ n: name, p: props.page }));
  } catch (e) {}
  done();
};
