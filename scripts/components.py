"""Shared HTML snippets for magnets.com.my static pages (used by build_pages.py)."""
import html, json

SITE = "https://magnets.com.my"
WA = "https://wa.me/60122112522"
ASSET_V = "mk1"

ICONS = {
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "custom": '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
 "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "camera": '<path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13.5" r="3.5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 11-12 0c0-4.5 6-11 6-11z"/>',
 "magnet": '<path d="M6 3v9a6 6 0 0012 0V3h-4v9a2 2 0 01-4 0V3z"/><path d="M6 7h4M14 7h4"/>',
 "check": '<path d="M5 12l4 4 10-10"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h7M8.5 14h4"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
}

def icon(name, cls=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % ((' class="%s"' % cls) if cls else "", ICONS[name]))

def e(s):
    return html.escape(s, quote=True)

NAV = [("/", "Home"), ("/magnetic-separators.html", "Separators"), ("/plate-magnets.html", "Plate"),
       ("/ndfeb-magnets.html", "NdFeB"), ("/smco-magnets.html", "SmCo"), ("/industries.html", "Industries"),
       ("/resources.html", "Resources"), ("/about.html", "About"), ("/faq.html", "FAQ")]

def header(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append('        <a href="%s"%s>%s</a>' % (href, cur, label))
    return '''  <header class="site-header">
    <div class="container header-inner">
      <a class="logo" href="/">
          <img class="brand-logo" src="/images/logo-header.png" alt="Arrowmatics AI" width="220" height="48">
          <span>Arrowmatics Magnets<span class="logo-sub">Separators · NdFeB · SmCo</span></span>
        </a>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">
        <span class="nav-toggle-bars" aria-hidden="true"></span>
      </button>
      <nav class="nav" id="primary-nav" aria-label="Primary">
%s
        <a class="nav-cta" href="tel:+60122112522" style="margin-right:0.5rem;">Call</a>
        <a class="nav-cta" href="https://wa.me/60122112522" target="_blank" rel="noopener">WhatsApp Quote</a>
      </nav>
    </div>
  </header>
  <script src="/js/nav-toggle.js?v=mobilenav1"></script>
''' % "\n".join(links)

FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h3><img class="brand-logo" src="/images/logo-header.png" alt="Arrowmatics AI" style="display:block;margin-bottom:0.5rem;" width="280" height="61"><span class="brand-text">Arrowmatics Magnets</span></h3>
          <p class="footer-nap">Magnetic separators, suspension magnets and NdFeB rare-earth magnets for industry in Malaysia.</p>
        </div>
        <div>
          <h3>Products</h3>
          <a href="/magnetic-separators.html">Magnetic separators</a>
          <a href="/plate-magnets.html">Plate magnets</a>
          <a href="/ndfeb-magnets.html">NdFeB magnets</a>
          <a href="/smco-magnets.html">SmCo magnets</a>
          <a href="/industries.html">Industries</a>
          <a href="/resources.html">Resources</a>
          <a href="/about.html">About Arrowmatics</a>
          <a href="/faq.html">FAQ</a>
          <a href="/privacy.html">Privacy</a>
        </div>
        <div class="footer-nap">
          <h3>NAP</h3>
          <p>Arrowmatics AI Sdn Bhd (1305806-W)</p>
          <p>No. 64, Jalan Kapar 27/89, Megah Industrial Park, Taman Alam Megah, Section 27, 40400 Shah Alam, Selangor, Malaysia</p>
          <p>Mobile / WhatsApp: <a href="tel:+60122112522">+60 12-211 2522</a> · Office: <a href="tel:+60351910299">+603 5191 0299</a></p>
          <p><a href="mailto:bensonlok@gmail.com">bensonlok@gmail.com</a> · <a href="mailto:arrowmatics@gmail.com">arrowmatics@gmail.com</a></p>
        </div>
      </div>
      <div class="footer-bottom">
        © Arrowmatics AI Sdn Bhd (1305806-W). All rights reserved. · <a href="https://magnets.com.my/">magnets.com.my</a>
      </div>
    </div>
  </footer>
'''

def fabs(wa_svg):
    return '''  <a class="call-fab" href="tel:+60122112522" aria-label="Call +60 12-211 2522">Call</a>
  <a class="wa-fab" href="https://wa.me/60122112522" target="_blank" rel="noopener" aria-label="WhatsApp for a written quote">
    %s
  </a>
  <link rel="stylesheet" href="/css/magnet-expert-chat.css?v=%s">
  <script src="/js/magnet-expert-chat.js?v=%s" defer></script>
  <script src="/js/ui.js?v=%s" defer></script>
  <script src="/js/site-config.js?v=%s" defer></script>
  <script src="/js/leads.js?v=%s" defer></script>
''' % (wa_svg, ASSET_V, ASSET_V, ASSET_V, ASSET_V, ASSET_V)

def head(title, desc, path, og_image, extra_ld, mdpath=None):
    url = SITE + path
    md = mdpath or path.replace(".html", ".md")
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title)s</title>
  <meta name="description" content="%(desc)s">
  <link rel="canonical" href="%(url)s">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(desc)s">
  <meta property="og:url" content="%(url)s">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Arrowmatics Magnets">
  <meta property="og:locale" content="en_MY">
  <meta property="og:image" content="%(img)s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%(title)s">
  <meta name="twitter:description" content="%(desc)s">
  <meta name="twitter:image" content="%(img)s">
  <link rel="stylesheet" href="/css/styles.css?v=%(v)s">
  <link rel="icon" type="image/png" href="/images/favicon.png">
%(ld)s
  <link rel="describedby" href="/llms.txt">
  <link rel="alternate" type="text/markdown" href="%(md)s">
  <link rel="alternate" type="text/plain" href="/llms-full.txt" title="Full LLM brief">
</head>
''' % dict(title=e(title), desc=e(desc), url=url, img=SITE + og_image, v=ASSET_V, md=md,
           ld="\n".join('  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(x, ensure_ascii=False, indent=2) for x in extra_ld))

def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

def chips(items):
    return '<ul class="chip-list ph-chips" aria-label="Key points">' + "".join(
        '<li>%s%s</li>' % (icon(ic), t) for ic, t in items) + '</ul>'

def hero(crumbs, eyebrow, h1, lead, chip_items, img, alt, cap, wh=(1200, 900), card=True, extra="", persona=None):
    """persona = dict(cta=..., q=...): one primary CTA (opens Magnet Expert upload) + quiet WhatsApp link."""
    bc = " · ".join('<a href="%s">%s</a>' % (u, n) if u else "<span>%s</span>" % n for n, u in crumbs)
    pc = ''
    if card:
        pc = '''<div class="photo-card"><span class="pc-ico">%s</span><div class="pc-text"><strong>Send a photo – get an answer in 1–3 business hours</strong>We aim to reply within 1–3 hours (Malaysia business hours).</div><button type="button" class="btn btn-expert-hero" data-open-magnet-expert data-expert-upload>Upload a photo</button></div>''' % icon("camera")
    if persona:
        actions = '''<button type="button" class="btn btn-expert-hero" data-open-magnet-expert data-expert-upload data-expert-q="%s">%s</button>
          <a class="btn btn-wa-link" href="%s" target="_blank" rel="noopener">or WhatsApp +60 12-211 2522</a>''' % (e(persona["q"]), persona["cta"], WA)
    else:
        actions = '''<a class="btn btn-wa" href="%s" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a>
          <button type="button" class="btn btn-expert-hero" data-open-magnet-expert>Ask the Magnet Expert</button>''' % WA
    return '''  <section class="ph">
    <div class="container ph-grid">
      <div class="ph-copy">
        <nav class="breadcrumb" aria-label="Breadcrumb">%s</nav>
        %s
        <h1>%s</h1>
        <p class="ph-lead">%s</p>
        %s
        <div class="ph-actions">
          %s
        </div>
        %s
      </div>
      <figure class="ph-photo">
        <img src="%s" alt="%s" width="%d" height="%d" fetchpriority="high" decoding="async">
        <figcaption>%s</figcaption>
        %s
      </figure>
    </div>
  </section>
''' % (bc, ('<span class="hero-eyebrow">%s</span>' % eyebrow) if eyebrow else "", h1, lead, chips(chip_items), actions, extra, img, e(alt), wh[0], wh[1], cap, pc)

HOW = '''  <section class="how" aria-label="How it works">
    <div class="container">
      <ol class="how-list">
        <li><span class="hn" aria-hidden="true">1</span><div><strong>Send a photo or sketch</strong><span class="hs">Hopper, chute, pipe or conveyor</span></div></li>
        <li><span class="hn" aria-hidden="true">2</span><div><strong>Get plain-language advice</strong><span class="hs">Which type fits, and why</span></div></li>
        <li><span class="hn" aria-hidden="true">3</span><div><strong>Receive a written quote</strong><span class="hs">Size, grade and build confirmed</span></div></li>
      </ol>
    </div>
  </section>
'''

BAND = '''  <section class="expert-band" aria-label="Magnet Expert">
    <div class="container">
      <p class="expert-band-text"><strong>Stop searching. Ask the Magnet Expert.</strong>Get clear on which magnetic separator type you need. We reply within 1–3 hours (Malaysia business hours).</p>
      <button type="button" class="btn btn-expert" data-open-magnet-expert>Ask the Magnet Expert →</button>
    </div>
  </section>
'''

def vcards(cards):
    out = []
    for href, img, alt, title, text in cards:
        out.append('''          <a class="vcard reveal" href="%s"><span class="vc-img"><img src="%s" alt="%s" width="800" height="600" loading="lazy" decoding="async"></span><span class="vc-body"><h3>%s</h3><p>%s</p><span class="vc-go">See details →</span></span></a>''' % (href, img, e(alt), title, text))
    return '<div class="vcards">\n' + "\n".join(out) + '\n        </div>'

def accordions(qas):
    return "\n".join('''        <details class="acc"><summary><h3>%s</h3></summary><div class="rm-body"><p>%s</p></div></details>''' % (q, a) for q, a in qas)


# ---------------------------------------------------------------- marketing blocks
CONSENT = ('I agree that Arrowmatics AI Sdn Bhd may use these details to reply to this request. '
           'No marketing lists, no selling of data. See the <a href="/privacy.html">privacy notice</a>.')

def _field(fid, label, inner, hint=""):
    return '<div class="field"><label for="%s">%s%s</label>%s</div>' % (fid, label, (' <span class="hint">%s</span>' % hint) if hint else "", inner)

def quote_form(prefix="q", context="", heading="Request a quote", sub="Three short fields. Photo optional. We aim to reply within 1–3 hours (Malaysia business hours)."):
    P = prefix
    return '''<div class="leadbox reveal" id="%(P)s-box">
          <div class="leadbox-head"><h2>%(h)s</h2><p>%(sub)s</p></div>
          <form class="lead-form" data-lead-form="quote" data-context="%(ctx)s" novalidate>
            %(f1)s
            %(f2)s
            %(f3)s
            %(f4)s
            <label class="consent"><input type="checkbox" name="consent" required> <span>%(consent)s</span></label>
            <div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
            <button class="btn btn-wa" type="submit">Send request</button>
            <p class="form-msg" role="status" aria-live="polite"></p>
            <noscript><p class="form-msg">Please enable JavaScript, or WhatsApp us directly.</p></noscript>
          </form>
        </div>''' % dict(P=P, h=heading, sub=sub, ctx=e(context), consent=CONSENT,
        f1=_field(P+"-name", "Your name", '<input id="%s-name" name="name" autocomplete="name" required maxlength="80">' % P),
        f2=_field(P+"-contact", "WhatsApp number or email", '<input id="%s-contact" name="contact" autocomplete="off" required maxlength="120" placeholder="+60… or name@company.com">' % P),
        f3=_field(P+"-msg", "What do you need?", '<textarea id="%s-msg" name="message" rows="3" required maxlength="600" placeholder="Product, size, material, where it fits"></textarea>' % P),
        f4=_field(P+"-photo", "Photo or sketch", '<input id="%s-photo" name="photo" type="file" accept="image/*">' % P, "optional"))

def checklist_form(prefix="c", context="checklist"):
    P = prefix
    return '''<div class="leadbox leadbox-checklist reveal" id="%(P)s-box">
          <div class="leadbox-head"><h2>Free 1-page selection checklist</h2><p>What to measure, what to send and what to confirm before you order a magnetic separator.</p></div>
          <form class="lead-form" data-lead-form="checklist" data-context="%(ctx)s" novalidate>
            %(f1)s
            %(f2)s
            %(f3)s
            <label class="consent"><input type="checkbox" name="consent" required> <span>%(consent)s</span></label>
            <div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
            <button class="btn btn-expert-hero" type="submit">Get the checklist</button>
            <p class="form-msg" role="status" aria-live="polite"></p>
            <div class="form-done" hidden>
              <a class="btn btn-wa" href="/downloads/Magnetic-Separator-Selection-Checklist.pdf" download data-track="checklist_download">Download the PDF</a>
              <a class="btn btn-outline-dark" href="/checklist-print.html" target="_blank" rel="noopener" data-track="checklist_print">Open printable page</a>
            </div>
            <noscript><p class="form-msg">Please enable JavaScript, or <a href="https://wa.me/60122112522">WhatsApp us</a> and we will send it.</p></noscript>
          </form>
        </div>''' % dict(P=P, ctx=e(context), consent=CONSENT,
        f1=_field(P+"-name", "Your name", '<input id="%s-name" name="name" autocomplete="name" required maxlength="80">' % P),
        f2=_field(P+"-email", "Email", '<input id="%s-email" name="email" type="email" autocomplete="email" required maxlength="120">' % P),
        f3=_field(P+"-phone", "WhatsApp number", '<input id="%s-phone" name="phone" type="tel" autocomplete="tel" maxlength="30">' % P, "optional"))

TRUST = '''    <section class="section tight" id="trust">
      <div class="container">
        <div class="section-head compact"><h2>What you can rely on</h2><p>Plain facts about how we work.</p></div>
        <ul class="icards trust-cards">
          <li class="reveal"><span class="ic">%(shield)s</span><h3>Registered company</h3><p>Arrowmatics AI Sdn Bhd (1305806-W), No. 64, Jalan Kapar 27/89, Megah Industrial Park, 40400 Shah Alam.</p></li>
          <li class="reveal"><span class="ic">%(chat)s</span><h3>Written quotes</h3><p>Size, grade and build confirmed in writing on WhatsApp. No online cart, no published list prices.</p></li>
          <li class="reveal"><span class="ic">%(clock)s</span><h3>Reply target</h3><p>We aim to reply within 1–3 hours in Malaysia business hours. A target, not a guarantee.</p></li>
          <li class="reveal"><span class="ic">%(check)s</span><h3>Honest about certification</h3><p>We are not ourselves certified to ISO 22000 or HACCP. We supply magnets for plants working to those standards.</p></li>
        </ul>
      </div>
    </section>
''' % dict(shield=icon("shield"), chat=icon("chat"), clock=icon("clock"), check=icon("check"))

def quote_section(prefix="q", context=""):
    return '''    <section class="section tight section-alt" id="quote">
      <div class="container leadgrid">
        %s
        %s
      </div>
    </section>
''' % (quote_form(prefix, context), checklist_form(prefix + "c", "checklist-" + context))
