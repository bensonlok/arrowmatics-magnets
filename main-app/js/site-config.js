/* Single place for contact constants + the privacy-friendly event hook.
   To swap the WhatsApp number everywhere (HTML, schema, llms files): python3 scripts/swap_whatsapp.py <old digits> <new digits>
   Then update `wa` / `waDisplay` below. */
window.MAGNETS = {
  wa: "60122112522",
  waDisplay: "+60 12-211 2522",
  office: "+60351910299",
  email: "arrowmatics@gmail.com",
  leadEndpoint: "/api/lead",
  /* Optional first-party event endpoint. Leave empty: no network call is made. */
  eventEndpoint: ""
};
/* magnetsTrack(name, props): no cookies, no third-party script.
   Emits a DOM event "magnets:event" and, ONLY IF the site owner later adds one of them,
   forwards to window.dataLayer / plausible / gtag. Honours Do Not Track for forwarding. */
window.magnetsTrack = function (name, props) {
  try {
    props = props || {};
    props.page = location.pathname;
    document.dispatchEvent(new CustomEvent("magnets:event", { detail: { name: name, props: props } }));
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;
    if (window.dataLayer && window.dataLayer.push) window.dataLayer.push(Object.assign({ event: name }, props));
    if (typeof window.plausible === "function") window.plausible(name, { props: props });
    if (typeof window.gtag === "function") window.gtag("event", name, props);
    var ep = window.MAGNETS && window.MAGNETS.eventEndpoint;
    if (ep && navigator.sendBeacon) navigator.sendBeacon(ep, JSON.stringify({ n: name, p: props.page }));
  } catch (e) {}
};
