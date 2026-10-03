#!/usr/bin/env python3
"""One-off restructure of main-app/index.html into a short first screen (kept for reference)."""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from components import *

P = os.path.join(os.path.dirname(__file__), "..", "main-app", "index.html")
s = open(P).read()

def between(s, a, b, incl_b=False):
    i = s.index(a); j = s.index(b, i) + (len(b) if incl_b else 0)
    return i, j

# --- pieces to reuse ---------------------------------------------------
tiles_m = re.search(r'<div class="hero-tiles" aria-label="Our magnet products">.*?\n      </div>\n', s, re.S)
tiles = tiles_m.group(0)
tiles = re.sub(r' fetchpriority="high"', ' loading="lazy"', tiles)
tiles = tiles.replace('<div class="hero-tiles" aria-label="Our magnet products">', '<div class="hero-tiles" aria-label="Our magnet products">')

g_i = s.index('<h3 class="gallery-cat">Grate magnet</h3>')
g_j = s.index('      </div>\n    </section>', g_i)
gallery_inner = s[g_i:g_j]

prod_i = s.index('        <div class="grid-3">', s.index('id="products"'))
prod_j = s.index('      </div>\n    </section>', prod_i)
product_cards = s[prod_i:prod_j]

contact_i = s.index('    <section class="contact-band" id="contact">')
contact_j = s.index('    </section>\n  </main>', contact_i)
contact = s[contact_i:contact_j + len('    </section>\n')]

# --- new hero ----------------------------------------------------------
intro_more = ('<details class="readmore"><summary>Read more about what we make</summary><div class="rm-body"><p>'
 '<strong>Magnets that fit your process for industry.</strong> Almost everything is possible: sizes, grades, housings, food-grade options and drawing-based builds. '
 'We start with sensible advice, make the choice simple, then work systematically toward a magnet that fits your process — from Shah Alam across Malaysia. '
 'Plate magnets, magnetic bars, grate magnets and separators are made to your size and duty. Send a photo or drawing for a quote.</p></div></details>')
hero_html = hero([("Home", None)], "Custom magnet systems · Shah Alam",
    'Magnets made to fit <span class="accent">your machine</span>',
    "Send a photo of your hopper, chute or conveyor — get a custom-fit magnet and a written quote.",
    [("shield", "Stainless 304 / 316 / 316L available"), ("custom", "Made to your drawing"), ("pin", "Shah Alam · Malaysia-wide")],
    "/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg",
    "Large grate magnet with thick polished stainless steel magnetic bars held in a cross frame", "Large-bar grate magnet", (1200, 900),
    extra=intro_more)
hero_html = hero_html.replace('<nav class="breadcrumb" aria-label="Breadcrumb"><span>Home</span></nav>\n        ', '')

# --- selector ----------------------------------------------------------
SEL = [
 ("grate", "/magnetic-separators.html#types", "/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg", "Grate magnet with large stainless bars in a cross frame", "Grate magnet", "Dry powders and granules falling through a hopper or chute. Larger bars suit bigger openings and heavier tramp metal."),
 ("drawer", "/magnetic-separators.html#types", "/images/real-drawer-1.jpg", "Double-drawer stainless magnetic separator housing", "Drawer magnet", "The same duty in a housing: rows of bars slide out for cleaning without stripping the line."),
 ("plate", "/plate-magnets.html", "/images/plate-magnet-10000g.jpg", "Full-weld stainless plate magnet", "Plate magnet", "Chute walls or hung over a falling stream or belt, with an easy-wipe face. Full-weld SS304/316/316L builds available."),
 ("suspension", "/magnetic-separators.html#suspension-magnets", "/images/suspension-overband-magnet-yellow-frame-workshop.jpg", "Yellow overband suspension magnet frame", "Suspension / overband magnet", "Pulls tramp iron off bulk material on a conveyor. Overband clears the iron on a running belt; suspended plates are cleaned by hand."),
 ("liquid", "/magnetic-separators.html#liquid-line-trap", "/images/real-liquid-trap-1.jpg", "Stainless liquid-line magnetic trap", "Liquid-line / filter trap", "Liquids, sauces, pastes and slurries moving through a pipe, where fine iron must be caught in-line."),
 ("bullet", "/magnetic-separators.html#types", "/images/real-bullet-1.jpg", "Bullet magnet front and side views", "Bullet magnet", "Pipelines and pneumatic or gravity product lines."),
 ("bar", "/magnetic-separators.html#bars-full-weld", "/images/real-bars-1.jpg", "Polished stainless magnetic bar", "Magnetic bar", "Tanks, hoppers and chutes, or as the bars inside a custom grid. Full weld is built to order."),
 ("rare", "/ndfeb-magnets.html", "/images/real-ndfeb-1.jpg", "NdFeB rare-earth magnet blocks", "NdFeB / SmCo magnets", "Small parts, OEM fixtures and assemblies; SmCo when heat or corrosion rules out NdFeB."),
]
OPTS = [
 ("Powder or granules in a hopper / chute", "grate drawer", "Free-flowing dry material is usually caught with a grate or drawer magnet across the opening."),
 ("Material on a conveyor belt", "suspension plate", "A suspension (overband or suspended plate) magnet hangs over the belt; a plate magnet can also sit above a belt or chute."),
 ("Liquid, sauce or slurry in a pipe", "liquid bullet", "A liquid-line trap fits a liquid pipeline; a bullet magnet suits pipe and pneumatic lines."),
 ("Food line (hygiene matters)", "plate grate drawer", "Food plants often choose full-weld stainless plate, grate or drawer magnets that are easy to clean and inspect. Arrowmatics is not itself certified to HACCP / ISO 22000."),
 ("Small parts, OEM or high temperature", "rare", "NdFeB for strength at room temperature; SmCo when heat or corrosion rules out NdFeB. Tell us the temperature."),
]
sel_cards = "\n".join('''          <div class="selector-item reveal" data-k="%s"><img class="si-ph" src="%s" alt="%s" width="800" height="600" loading="lazy" decoding="async"><h3>%s</h3><p><strong>Best for:</strong> %s</p><p><a href="%s">See details →</a></p></div>''' % (k, img, e(alt), name, txt, href) for k, href, img, alt, name, txt in SEL)
sel_opts = "\n".join('          <li><button type="button" aria-pressed="false" data-pick="%s" data-why="%s">%s</button></li>' % (k, e(why), t) for t, k, why in OPTS)
selector = '''    <section class="section sel tight" id="selector" aria-labelledby="selector-h">
      <div class="container">
        <div class="section-head compact">
          <span class="eyebrow">Quick selector</span>
          <h2 id="selector-h">Which magnetic separator do I need?</h2>
        </div>
        <div class="answer-box">
          <p><strong>Choose by how your product moves.</strong> Free-flowing powder or granules falling through a hopper or chute usually points to a <strong>grate</strong> or <strong>drawer</strong> magnet. Material on a conveyor belt points to a <strong>suspension (overband or suspended plate)</strong> magnet. Liquids, sauces and slurries in a pipeline point to a <strong>liquid line / filter</strong> magnetic trap. Not sure? Send a photo — we will guide you.</p>
        </div>
        <p class="sel-q" style="margin-top:1.25rem;">Tap what you handle:</p>
        <ul class="sel-opts">
%s
        </ul>
        <div class="sel-result" role="status" aria-live="polite"></div>
        <div class="selector-grid">
%s
        </div>
        <p class="sec-note">To size one, we need the material, flow rate, particle size, moisture, contaminant, temperature, pipe or chute size, and ideally a photo. Size, grade and gauss are confirmed at quotation.</p>
      </div>
    </section>
''' % (sel_opts, sel_cards)

# --- comparison table --------------------------------------------------
cmp_rows = [
 ("Grate", "Dry powders, granules", "Across a hopper or chute opening", "Bars pulled out or wiped clean"),
 ("Drawer", "Dry powders, granules", "In a housing under a hopper or before an extruder", "Drawer slides out for cleaning"),
 ("Plate", "Chute walls, falling streams, belts", "On a chute wall or hung above a belt", "Wipe the face; hinged, suspended or quick-release builds"),
 ("Suspension (overband / plate)", "Tramp iron in bulk on a conveyor", "Hung over the conveyor belt", "Overband: self-cleaning belt. Suspended plate: by hand"),
 ("Liquid-line trap", "Liquids, sauces, pastes, slurries", "In the pipeline", "Open the lid and remove the bars"),
 ("Bullet", "Pipe and pneumatic lines", "Inside a pipe housing", "Core pulls out for cleaning"),
]
cmp_html = '''    <section class="section tight section-alt" id="compare">
      <div class="container">
        <div class="section-head compact"><h2>Compare at a glance</h2><p>General guide only. Size, field strength and build are confirmed at quotation.</p></div>
        <div class="cmp-wrap reveal">
          <table class="cmp">
            <caption class="sr-only">Magnetic separator types compared</caption>
            <thead><tr><th scope="col">Type</th><th scope="col">Best for</th><th scope="col">Where it sits</th><th scope="col">Cleaning</th></tr></thead>
            <tbody>
%s
            </tbody>
          </table>
        </div>
      </div>
    </section>
''' % "\n".join("              <tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in cmp_rows)

range_html = '''    <section class="range" id="range" aria-label="Our range">
      <div class="container">
        <h2>Our range, at a glance</h2>
%s
      </div>
    </section>
''' % tiles

# --- products (compact) ------------------------------------------------
products = '''    <section class="section tight" id="products">
      <div class="container">
        <div class="section-head compact"><span class="eyebrow">Assortment</span><h2>Product families</h2><p>Standard ranges plus almost-anything-to-drawing options.</p></div>
%s
      </div>
    </section>
''' % product_cards

# --- plate section -----------------------------------------------------
plate = '''    <section class="section section-dark tight" id="plate-magnets">
      <div class="container">
        <div class="split">
          <figure class="split-photo reveal">
            <img src="images/plate-magnet-10000g.jpg" alt="Full-weld stainless steel plate magnet for food plants" loading="lazy" width="1200" height="800">
            <figcaption>Full-weld stainless plate magnet</figcaption>
          </figure>
          <div class="reveal">
            <span class="eyebrow light">Food-plant ready</span>
            <h2>Plate magnets up to 10,000 Gauss. 100% full weld.</h2>
            <p style="color:#c5cad6;">For food plants working to HACCP / ISO 22000. <strong style="color:#fff;">Arrowmatics is not itself certified.</strong></p>
            <ul class="chip-list"><li>SS304 / 316 / 316L</li><li>No crevices or exposed fasteners</li><li>Easy to clean &amp; inspect</li></ul>
            <details class="readmore"><summary>Read more</summary><div class="rm-body"><p>Continuous seal welds in SS304/SS316/SS316L, no crevices, no exposed fasteners and a smooth, cleanable finish. Designed to support your HACCP and ISO 22000 programme as a ferrous foreign-body control. Typical rating of up to ~10,000 Gauss; confirm per application and air gap. Customers remain responsible for their own certification.</p></div></details>
            <div class="hero-actions" style="margin-top:1rem;">
              <a class="btn btn-wa" href="/plate-magnets.html">See full-weld plate magnets</a>
              <a class="btn btn-outline" href="https://wa.me/60122112522" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a>
            </div>
          </div>
        </div>
      </div>
    </section>
'''

# --- gallery -----------------------------------------------------------
feat = [("grate-magnet-large-bars-stainless-tubes-cross-frame.jpg","Large grate magnet with thick polished stainless steel magnetic bars held in a cross frame","Grate · large bars",1200,900),
        ("real-drawer-1.jpg","Double-drawer magnetic separator housing","Drawer separator",1400,1050),
        ("suspension-overband-magnet-yellow-frame-workshop.jpg","Yellow overband suspension magnet frame with hanging lugs and black ribbed belt on a workshop floor","Overband magnet",1200,900),
        ("real-hopper-grate-1.jpg","Round hopper grate magnet with drawer handle","Hopper grate",1000,750),
        ("real-liquid-trap-1.jpg","Stainless steel liquid-line magnetic trap with swing-bolt lid","Liquid-line trap",1400,1866),
        ("suspension-plate-magnet-yellow-four-eyebolts.jpg","Yellow suspended plate magnet with four eyebolts for hanging above a conveyor","Suspended plate",960,720)]
featfigs = "\n".join('          <figure><img src="images/%s" alt="%s" loading="lazy" width="%d" height="%d"><figcaption>%s</figcaption></figure>' % (f, a, w, h, c) for f, a, c, w, h in feat)
gallery = '''    <section class="section tight" id="gallery">
      <div class="container">
        <div class="section-head compact"><span class="eyebrow">Photos</span><h2>Magnet types in the workshop</h2><p>Real product photos. Open the full gallery for every type, plus pull-distance and Gauss demos on plate magnets.</p></div>
        <div class="photo-grid">
%s
        </div>
        <details class="readmore" style="margin-top:1rem;">
          <summary>Show all product photos and demo videos</summary>
          <div class="rm-body">
%s
          </div>
        </details>
      </div>
    </section>
''' % (featfigs, gallery_inner)

# --- industries --------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))
import build_pages as bp
ind_cards = [("/%s.html" % d["slug"], d["img"], d["alt"], d["name"], d["lead"]) for d in bp.IND]
industries = '''    <section class="section tight section-alt" id="industries">
      <div class="container">
        <div class="section-head compact"><span class="eyebrow">Industries served</span><h2>Built for Malaysian plants</h2><p>Pick your industry for the right magnet type and what to send. <a href="/industries.html">All industries →</a></p></div>
        %s
        <p class="ind-note"><strong>Also served:</strong> OEMs and MRO — NdFeB blanks and assemblies; aggregates and conveyors — suspension (overband) and plate magnets.</p>
      </div>
    </section>
''' % vcards(ind_cards)

# --- why ---------------------------------------------------------------
why = '''    <section class="section tight" id="why">
      <div class="container">
        <div class="section-head compact"><span class="eyebrow">Why Arrowmatics</span><h2>Simple, honest, made to fit</h2></div>
        <div class="icards">
          <div class="icard reveal"><span class="ic">%s</span><h3>Photo first</h3><p>Send a photo or sketch. We explain the options in plain words.</p></div>
          <div class="icard reveal"><span class="ic">%s</span><h3>Customise to fit</h3><p>Sizes, grades, housings and drawing-based builds are worth exploring.</p></div>
          <div class="icard reveal"><span class="ic">%s</span><h3>Easy to clean</h3><p>Stainless 304 / 316 / 316L available; full weld built to order.</p></div>
          <div class="icard reveal"><span class="ic">%s</span><h3>Honest quotes</h3><p>Written quotes on WhatsApp. No invented prices, stock or certificates. <a href="/about.html">About us</a></p></div>
        </div>
      </div>
    </section>
''' % (icon("camera"), icon("custom"), icon("shield"), icon("chat"))

# --- FAQ ---------------------------------------------------------------
faq_qas = [
 ("Food-grade grate magnets Malaysia?", "Yes. We supply food-grade grate and drawer magnets for Malaysian food plants. Share product and opening size for a written quote."),
 ("NdFeB N52 strongest commercial grade?", "Among common sintered grades, N52 is at the top of the energy-product range we supply (N35–N52). Grade choice also depends on temperature and coating."),
 ("What is a suspension (overband) magnet?", "A suspension magnet hangs over a conveyor belt and pulls tramp iron out of the material passing underneath. Overband types clear the iron automatically on a running belt; suspended plate types are cleaned by hand. Send belt width, burden depth and hanging height for a written quote."),
]
faq = '''    <section class="section tight section-alt" id="faq-teaser">
      <div class="container">
        <div class="section-head compact"><span class="eyebrow">Buyer questions</span><h2>Quick technical answers</h2></div>
%s
        <p style="margin-top:1rem;"><a href="/faq.html" class="card-link">Read all FAQs →</a></p>
      </div>
    </section>
''' % accordions(faq_qas)

# --- contact: shorter -----------------------------------------------------
contact = re.sub(r'\n        <p style="color:#c5cad6;max-width:36rem;margin-bottom:1rem;">.*?</p>\n        <p style="color:#c5cad6;max-width:36rem;margin-bottom:2.5rem;">.*?</p>',
  '\n        <p style="color:#c5cad6;max-width:36rem;margin-bottom:2rem;">Send a photo, sketch or drawing with the size and where it will be used. <strong style="color:#fff;">Photo in – answer in 1–3 business hours</strong> (a target, Malaysia business hours). Written quote on WhatsApp.</p>',
  contact, flags=re.S)
contact = contact.replace('<h2 class="contact-headline">Magnets made to fit your machine and your hygiene needs</h2>', '<h2 class="contact-headline">Send a photo. Get an answer.</h2>')

# --- assemble ----------------------------------------------------------
h_i = s.index('  <section class="hero hero-showcase" id="top">')
m_i = s.index('  <main>')
mend = s.index('  </main>')
main_new = '  <main>\n' + selector + '\n' + BAND.replace('  <section class="expert-band"', '    <section class="expert-band"') + '\n' + range_html + '\n' + cmp_html + '\n' + products + '\n' + plate + '\n' + gallery + '\n' + industries + '\n' + why + '\n' + faq + '\n' + contact
new = s[:h_i] + hero_html + '\n' + HOW + '\n' + s[m_i:m_i] + main_new + s[mend:]
# head: preload + og image + css version
new = new.replace('<link rel="preload" as="image" href="images/hero/tile-plate.jpg" fetchpriority="high">',
                  '<link rel="preload" as="image" href="/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg" fetchpriority="high">')
if 'property="og:image"' not in new:
    new = new.replace('  <meta name="twitter:card" content="summary_large_image">',
      '  <meta property="og:image" content="https://magnets.com.my/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:image" content="https://magnets.com.my/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg">',1)
new = new.replace('css/styles.css?v=expert1', 'css/styles.css?v=%s' % ASSET_V)
new = new.replace('<script src="/js/magnet-expert-chat.js?v=expert1" defer></script>', '<script src="/js/magnet-expert-chat.js?v=%s" defer></script>\n  <script src="/js/ui.js?v=%s" defer></script>' % (ASSET_V, ASSET_V))
new = new.replace('/css/magnet-expert-chat.css?v=expert1', '/css/magnet-expert-chat.css?v=%s' % ASSET_V)
# LocalBusiness: logo + image (own assets)
new = new.replace('"url": "https://magnets.com.my/",\n    "telephone": "+60122112522",', '"url": "https://magnets.com.my/",\n    "logo": "https://magnets.com.my/images/logo.png",\n    "image": "https://magnets.com.my/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg",\n    "telephone": "+60122112522",',1)
open(P, "w").write(new)
print("home rebuilt", len(s), "->", len(new))
