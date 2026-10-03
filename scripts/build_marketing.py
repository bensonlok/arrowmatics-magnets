#!/usr/bin/env python3
"""Generate Resources hub, 3 guides, checklist landing + printable page, request-quote page and privacy notice (+ .md mirrors).
Run from repo root: python3 scripts/build_marketing.py
Facts only from the site / marketing pack. No stats, customers, certifications or prices."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
from components import *
OUT = os.path.join(os.path.dirname(__file__), "..", "main-app")
WA_SVG = re.search(r'<a class="wa-fab".*?>\s*(<svg.*?</svg>)\s*</a>', open(os.path.join(OUT, "faq.html")).read(), re.S).group(1)
TODAY = "2026-10-03"
OG = "/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg"
CERT = "Arrowmatics is not itself certified to ISO 22000, HACCP or GMP. This is general guidance; size, grade and build are confirmed at quotation."

def write(name, html_):
    open(os.path.join(OUT, name), "w").write(html_)

def shell(path, title, desc, ld, main, current="/resources.html", ogimg=OG, robots=None):
    h = head(title, desc, path, ogimg, ld, mdpath=path.replace(".html", ".md"))
    if robots:
        h = h.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="%s">' % robots)
    return h + "<body>\n" + header(current) + "\n  <main>\n" + main + "\n  </main>\n\n" + FOOTER + "\n" + fabs(WA_SVG) + "</body>\n</html>\n"

def article_ld(path, title, desc):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "url": SITE + path,
            "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "en",
            "author": {"@type": "Organization", "name": "Arrowmatics Magnets"},
            "publisher": {"@type": "Organization", "name": "Arrowmatics Magnets", "legalName": "Arrowmatics AI Sdn Bhd", "url": SITE + "/"},
            "mainEntityOfPage": SITE + path, "image": SITE + OG}

RELATED = '<p class="related">Related: <a href="/guide-which-magnetic-separator.html">Which magnetic separator?</a> · <a href="/guide-what-to-send-for-a-magnet-quote.html">What to send for a quote</a> · <a href="/guide-plate-magnet-inspection-cleaning.html">Plate magnet inspection &amp; cleaning</a> · <a href="/selection-checklist.html">Free selection checklist</a></p>'
CTA = '''<div class="expert-band" style="margin-top:2rem;"><div class="container"><p class="expert-band-text"><strong>Send a photo – get an answer in 1–3 business hours</strong>We aim to reply within 1–3 hours (Malaysia business hours).</p><button type="button" class="btn btn-expert" data-open-magnet-expert data-expert-upload>Ask the Magnet Expert →</button></div></div>'''

def tick(items): return '<ul class="tick">' + "".join("<li>%s</li>" % i for i in items) + "</ul>"

# ------------------------------------------------------------------ guides
GUIDES = [
 dict(slug="guide-which-magnetic-separator", tag="Guide · 2 min", title="Which magnetic separator do I need? Quick guide | Arrowmatics Magnets",
  h1="Which magnetic separator do I need?",
  desc="Pick a magnetic separator by how your material moves: hopper, conveyor, pipe or chute. Short guide with a decision table from Arrowmatics Magnets, Shah Alam.",
  lead="Choose by how the product moves. Then check the build, the cleaning access and the working gap.",
  card="Decision table: hopper, conveyor, pipe or chute.",
  body=lambda: '''<h2>Start with how the product moves</h2>
<div class="tbl-wrap"><table><thead><tr><th>Your material</th><th>Usual fit</th><th>Where it sits</th></tr></thead><tbody>
<tr><td>Dry powder or granules falling through a hopper or chute</td><td><a href="/magnetic-separators.html#types">Grate or drawer magnet</a></td><td>Across the opening or outlet</td></tr>
<tr><td>Material riding on a conveyor belt</td><td><a href="/magnetic-separators.html#suspension-magnets">Overband (self-cleaning) or suspended plate</a>; magnetic pulley at the head end</td><td>Over or at the end of the belt</td></tr>
<tr><td>Liquid, paste or slurry in a pipe</td><td><a href="/magnetic-separators.html#liquid-line-trap">Liquid-line magnetic trap</a></td><td>In-line on the pipe</td></tr>
<tr><td>Powder or pellets in a pipe or pneumatic line</td><td><a href="/magnetic-separators.html#types">Bullet magnet</a></td><td>Inside the pipe</td></tr>
<tr><td>Chute wall, tank, or a spot where hygiene matters</td><td><a href="/plate-magnets.html">Plate magnet</a> (full-weld stainless available)</td><td>Chute wall or above a conveyor</td></tr>
<tr><td>Small parts, OEM use, or heat and corrosion</td><td><a href="/ndfeb-magnets.html">NdFeB</a> or <a href="/smco-magnets.html">SmCo</a> magnets</td><td>Made to your drawing</td></tr>
</tbody></table></div>
<h2>Then check four things</h2>
''' + tick(["<strong>Build:</strong> stainless 304, 316 or 316L; full weld is available, built to order, when you want no screws or crevices.",
 "<strong>Cleaning:</strong> hand-clean, pull-out drawer or self-cleaning belt. Leave room to reach it.",
 "<strong>Working gap:</strong> field strength depends on the gap to the product. Typical rare-earth separators we quote sit around 10,000–13,000 gauss at the pole; confirm per application.",
 "<strong>Temperature:</strong> NdFeB suits normal duty; SmCo suits heat and corrosion. Give us your maximum temperature."]) + '<p class="sec-note">' + CERT + '</p>'),
 dict(slug="guide-what-to-send-for-a-magnet-quote", tag="Guide · 2 min", title="What to Send for a Magnetic Separator Quote | Arrowmatics Magnets",
  h1="What to send for a magnet quote",
  desc="The details and photos that let Arrowmatics Magnets quote a custom magnetic separator in writing: material, flow, size, temperature and a photo of the spot.",
  lead="A photo plus six facts is usually enough for a first written quote.",
  card="Checklist of details and photo tips.",
  body=lambda: '''<h2>Send these</h2>
''' + tick(["<strong>Photo of the spot.</strong> One wide shot and one close shot of the hopper, chute, pipe or conveyor. A sketch is fine too.",
 "<strong>Material:</strong> powder, granules, pellets, liquid or slurry, and what it is.",
 "<strong>Size:</strong> opening, belt width, pipe size, hanging height or burden depth, whichever applies.",
 "<strong>Flow:</strong> rate, particle size and moisture.",
 "<strong>The problem:</strong> what iron you are finding (rust, wear fragments, tramp iron) and where it does harm.",
 "<strong>Temperature</strong> and any corrosive or washdown conditions.",
 "<strong>Cleaning and hygiene:</strong> how you clean now, and whether you need a full-weld stainless finish.",
 "<strong>Quantity</strong> and any drawing you already have."]) + '''<h2>Photo tips</h2>
''' + tick(["Put a tape measure or ruler in the shot so we can see the scale.", "Circle or mark the problem area on the photo or sketch.", "Photos are resized in your browser before upload; you can also send them on WhatsApp."]) + '''<h2>What you get back</h2>
<p>Plain-language advice on which type fits, then a written quote with size, grade and build confirmed. We publish no RM list prices. We aim to reply within 1–3 hours in Malaysia business hours; that is a target, not a guarantee.</p>
<p class="sec-note">''' + CERT + '</p>'),
 dict(slug="guide-plate-magnet-inspection-cleaning", tag="Guide · 3 min", title="Plate Magnet Inspection & Cleaning Checklist | Arrowmatics Magnets",
  h1="Plate magnet inspection and cleaning checklist",
  desc="A seven-step plate magnet inspection and cleaning checklist to adapt to your own SOP. For food plants working to HACCP / ISO 22000. Arrowmatics is not itself certified.",
  lead="Seven steps to adapt to your own SOP. How often depends on your hazard analysis and how much iron you find.",
  card="Seven-step routine for full-weld plate magnets.",
  body=lambda: '''<p><strong>For food plants working to HACCP / ISO 22000.</strong> Arrowmatics is not itself certified; this checklist supports your programme and does not replace it.</p>
<h2>The routine</h2>
<ol class="checklist">
<li><strong>Isolate and make safe.</strong> Stop the line or divert product. Keep tools, watches and steel items clear of the strong magnet face.</li>
<li><strong>Open or release.</strong> Swing the hinged plate open or use the quick-release to lift it out.</li>
<li><strong>Remove and record captured metal.</strong> Take off ferrous fragments, note the amount and type, and investigate any change or sudden increase.</li>
<li><strong>Clean the face and seams.</strong> Wipe or wash with your approved cleaning method and sanitiser, and confirm nothing remains on the surface.</li>
<li><strong>Inspect the weld seams and face.</strong> Look for dents, cracks, pitting, discolouration or damage to the stainless surface. Report any breach of the seal.</li>
<li><strong>Verify performance.</strong> Do a cling or pull test with a test piece, or take a Gauss-meter reading on the surface if your programme requires it.</li>
<li><strong>Close, refit and sign off.</strong> Return the plate to position, check the latch and mounting, and sign the log.</li>
</ol>
<p>More on the build: <a href="/plate-magnets.html">full-weld plate magnets</a>.</p><p class="sec-note">General guidance only. ''' + CERT + '</p>'),
]

def guide_page(g):
    path = "/%s.html" % g["slug"]
    ld = [article_ld(path, g["h1"], g["desc"]), breadcrumb_ld([("Home", "/"), ("Resources", "/resources.html"), (g["h1"], path)])]
    main = '''    <section class="section tight"><div class="container guide">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · <a href="/resources.html">Resources</a> · <span>%s</span></nav>
      <span class="eyebrow">%s</span>
      <h1>%s</h1>
      <p class="g-lead">%s</p>
      %s
      %s
    </div></section>
    %s''' % (g["h1"], g["tag"], g["h1"], g["lead"], g["body"](), RELATED, CTA)
    write(g["slug"] + ".html", shell(path, g["title"], g["desc"], ld, main))
    txt = re.sub(r"<li>", "- ", g["body"]()); txt = re.sub(r"</?(tr|thead|tbody|table|div|ul|ol)[^>]*>", "\n", txt)
    txt = re.sub(r"</t[dh]>", " | ", txt); txt = re.sub(r"<h2>(.*?)</h2>", r"\n## \1\n", txt); txt = re.sub(r"<[^>]+>", "", txt)
    txt = re.sub(r"\n\s*\n+", "\n\n", txt.replace("&amp;", "&")).strip()
    write(g["slug"] + ".md", "# %s — Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s · WhatsApp +60 12-211 2522\n\n%s\n\n%s\n" % (g["h1"], SITE, path, g["lead"], txt))

# ------------------------------------------------------------------ checklist
CHECK = [
 ("1. How does your material move?", ["Dry powder or granules through a hopper or chute: grate or drawer magnet", "Material on a conveyor belt: overband, suspended plate or magnetic pulley", "Liquid, paste or slurry in a pipe: liquid-line magnetic trap", "Powder or pellets in a pipe or pneumatic line: bullet magnet", "Chute wall, tank or hygiene-sensitive spot: plate magnet", "Small parts, OEM or heat/corrosion duty: NdFeB or SmCo magnet"]),
 ("2. Measure and note", ["Opening size, belt width or pipe size", "Hanging height and burden depth (conveyors)", "Material, particle size and flow rate", "Moisture and temperature", "What iron you are finding: rust, wear fragments, tramp iron", "Room around the magnet to reach and clean it"]),
 ("3. Choose the build", ["Stainless grade: 304, 316 or 316L (316 / 316L generally suit more corrosive or washdown duty)", "Full weld if you want no screws or crevices (built to order)", "Cleaning method: by hand, drawer pull-out or self-cleaning belt", "Seams and finish you can wipe and inspect"]),
 ("4. Confirm before you order", ["Field strength at your working gap (typical rare-earth separators sit around 10,000–13,000 gauss at the pole; plate magnets up to about 10,000 Gauss typical; not a guarantee)", "Temperature limit: NdFeB for normal duty, SmCo for heat and corrosion", "Written spec with size, grade and build", "Which documents your quality system needs (ask at quotation)", "Who cleans and inspects it, and how often"]),
 ("5. Send it", ["Photo of the spot: one wide, one close, with a ruler for scale", "This list, filled in as far as you can", "WhatsApp +60 12-211 2522 or the form at magnets.com.my"]),
]
def checklist_inner():
    return "".join("<h2>%s</h2><ul>%s</ul>" % (t, "".join("<li>%s</li>" % i for i in items)) for t, items in CHECK)

def checklist_pages():
    # printable page (noindex) -> also used to render the PDF
    pm = '''  <div class="print-bar"><button type="button" class="btn btn-wa" onclick="window.print()">Print or save as PDF</button><a class="btn btn-outline-dark" href="/downloads/Magnetic-Separator-Selection-Checklist.pdf" download>Download PDF</a><a class="btn btn-outline-dark" href="/selection-checklist.html">Back</a></div>
  <article class="print-sheet">
    <h1>Magnetic separator selection checklist</h1>
    <p>Arrowmatics Magnets · 1 page · tick as you go, then send it with a photo.</p>
    %s
    <p class="p-foot">General guidance only; size, grade, gauss and build are confirmed at quotation. We publish no RM list prices. %s<br>
    Arrowmatics AI Sdn Bhd (1305806-W) · No. 64, Jalan Kapar 27/89, Megah Industrial Park, Taman Alam Megah, Section 27, 40400 Shah Alam, Selangor · Tel +603 5191 0299 · WhatsApp +60 12-211 2522 · magnets.com.my</p>
  </article>''' % (checklist_inner(), "Arrowmatics is not itself certified to ISO 22000, HACCP or GMP.")
    path = "/checklist-print.html"
    h = head("Magnetic Separator Selection Checklist (printable) | Arrowmatics Magnets", "Printable one-page magnetic separator selection checklist from Arrowmatics Magnets.", path, OG, [], mdpath="/selection-checklist.md")
    h = h.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex,follow">')
    write("checklist-print.html", h + "<body>\n" + header("/resources.html") + pm + "\n" + FOOTER + "\n" + fabs(WA_SVG) + "</body>\n</html>\n")
    # landing page
    path = "/selection-checklist.html"
    title = "Free Magnetic Separator Selection Checklist (1 page) | Arrowmatics Magnets"
    desc = "Free one-page checklist: how your material moves, what to measure, which build to choose and what to confirm before ordering a magnetic separator in Malaysia."
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": "Magnetic separator selection checklist", "url": SITE + path, "description": desc,
           "isPartOf": {"@type": "WebSite", "url": SITE + "/"}}, breadcrumb_ld([("Home", "/"), ("Resources", "/resources.html"), ("Selection checklist", path)])]
    main = '''    <section class="section tight"><div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · <a href="/resources.html">Resources</a> · <span>Selection checklist</span></nav>
      <div class="leadgrid">
        <div>
          <span class="eyebrow">Free · 1 page · PDF</span>
          <h1 style="font-size:clamp(1.8rem,4vw,2.6rem);margin:0.4rem 0 0.6rem;">Magnetic separator selection checklist</h1>
          <p class="g-lead" style="font-size:1.1rem;color:#5d6270;line-height:1.5;">Pick the right type, measure the right things and send what we need for a written quote.</p>
          <ul class="tick guide-tick" style="list-style:none;padding:0;">%s</ul>
          <details class="readmore"><summary>What is on the checklist</summary><div class="rm-body">%s</div></details>
          <p class="sec-note">No invented figures, no certification claims. %s</p>
        </div>
        %s
      </div>
    </section>
    <section class="section tight section-alt"><div class="container guide">%s</div></section>
    %s''' % ("".join("<li style='padding:.4rem 0'>✓ %s</li>" % x for x in ["How your material moves, and the usual fit", "What to measure and note", "Build choices: stainless grade, full weld, cleaning", "What to confirm before you order"]),
             "".join("<h3>%s</h3><ul>%s</ul>" % (t, "".join("<li>%s</li>" % i for i in items)) for t, items in CHECK).replace("<h3>", "<h3 style='margin-top:.8rem'>"),
             CERT, checklist_form("c1", "selection-checklist"), RELATED, CTA)
    write("selection-checklist.html", shell(path, title, desc, ld, main))
    write("selection-checklist.md", "# Magnetic separator selection checklist — Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s · WhatsApp +60 12-211 2522\n\n%s\n\n%s\n" % (
        SITE, path, desc, "\n".join("## %s\n\n%s\n" % (t, "\n".join("- " + i for i in items)) for t, items in CHECK)))

# ------------------------------------------------------------------ quote page
def quote_page():
    path = "/request-quote.html"
    title = "Request a Quote | Custom Magnets & Separators | Arrowmatics Magnets Shah Alam"
    desc = "Request a written quote for magnetic separators, plate, NdFeB or SmCo magnets. Three short fields, photo optional. We aim to reply within 1–3 hours (Malaysia business hours)."
    ld = [{"@context": "https://schema.org", "@type": "ContactPage", "name": "Request a quote", "url": SITE + path, "description": desc,
           "isPartOf": {"@type": "WebSite", "url": SITE + "/"}}, breadcrumb_ld([("Home", "/"), ("Request a quote", path)])]
    main = '''    <section class="section tight"><div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · <span>Request a quote</span></nav>
      <div class="leadgrid">
        <div>
          <span class="eyebrow">Written quote</span>
          <h1 style="font-size:clamp(1.8rem,4vw,2.6rem);margin:0.4rem 0 0.6rem;">Request a quote</h1>
          <p style="font-size:1.1rem;color:#5d6270;line-height:1.5;">Tell us what you need. Add a photo if you can. We aim to reply within 1–3 hours (Malaysia business hours).</p>
          <p style="margin-top:1rem;"><a class="btn btn-wa" href="%s" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a></p>
          <p class="sec-note">Prefer to talk? Office <a href="tel:+60351910299">+603 5191 0299</a>. No RM list prices are published; quotes are written.</p>
        </div>
        %s
      </div>
    </div></section>''' % (WA, quote_form("rq", "request-quote"))
    write("request-quote.html", shell(path, title, desc, ld, main, current="/"))
    write("request-quote.md", "# Request a quote — Arrowmatics Magnets\n\n> Canonical: %s%s\n\nSend name, WhatsApp or email, and what you need (photo optional). Reply target: within 1–3 hours in Malaysia business hours (not a guarantee). WhatsApp +60 12-211 2522 · Tel +603 5191 0299.\n" % (SITE, path))

# ------------------------------------------------------------------ privacy
def privacy():
    path = "/privacy.html"
    title = "Privacy Notice | Arrowmatics Magnets (Arrowmatics AI Sdn Bhd)"
    desc = "How Arrowmatics AI Sdn Bhd handles the details you send through the quote form, checklist form and Magnet Expert chat on magnets.com.my."
    ld = [breadcrumb_ld([("Home", "/"), ("Privacy", path)])]
    main = '''    <section class="section tight"><div class="container guide">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · <span>Privacy</span></nav>
      <h1>Privacy notice</h1>
      <p class="g-lead">Short and plain. Updated %s.</p>
      <h2>Who we are</h2>
      <p>Arrowmatics AI Sdn Bhd (1305806-W), trading as Arrowmatics Magnets, No. 64, Jalan Kapar 27/89, Megah Industrial Park, Taman Alam Megah, Section 27, 40400 Shah Alam, Selangor. Contact: <a href="mailto:arrowmatics@gmail.com">arrowmatics@gmail.com</a> or +603 5191 0299.</p>
      <h2>What we collect, and why</h2>
      %s
      <h2>Who sees it</h2>
      <p>Your form details are sent to our team as a private message notification. The Magnet Expert chat uses a third-party AI service to write replies, so the text and photo you type or upload there are passed to that service. We do not sell your details and we do not add you to a marketing list. Nothing is sent to you unless you asked for it (a reply to your enquiry, or the checklist you requested).</p>
      <h2>On your device</h2>
      <p>The Magnet Expert chat remembers the name and contact you typed in your own browser (local storage) so you do not have to retype it. Clear your browser data to remove it. This site does not set advertising or analytics cookies and does not run third-party trackers.</p>
      <h2>Your choices</h2>
      <p>You may ask to see, correct or delete your details, or to stop being contacted, by emailing <a href="mailto:arrowmatics@gmail.com">arrowmatics@gmail.com</a>. This notice is written with Malaysia's Personal Data Protection Act 2010 in mind.</p>
      %s
    </div></section>''' % (TODAY, tick(["<strong>Quote form:</strong> your name, WhatsApp number or email, your message and an optional photo. Used to reply to your request.", "<strong>Checklist form:</strong> your name, email and optional WhatsApp number. Used to give you the checklist and to answer if you reply.", "<strong>Magnet Expert chat:</strong> name, WhatsApp or email, your messages and any photo or sketch. Used to answer your question and to follow up."]), RELATED)
    write("privacy.html", shell(path, title, desc, ld, main, current="/"))
    write("privacy.md", "# Privacy notice — Arrowmatics Magnets\n\n> Canonical: %s%s\n\nArrowmatics AI Sdn Bhd (1305806-W). Form and chat details are used only to reply to your request or give you the checklist you asked for; they are passed to our team by private message and, for the chat, to an AI service. No sale of data, no marketing list, no advertising or analytics cookies. Contact arrowmatics@gmail.com to access, correct or delete your details.\n" % (SITE, path))

# ------------------------------------------------------------------ resources hub
def resources():
    path = "/resources.html"
    title = "Resources | Magnetic Separator Selection Checklist & Guides | Arrowmatics Magnets"
    desc = "Free one-page magnetic separator selection checklist and three short guides: which separator, what to send for a quote, plate magnet inspection and cleaning. Arrowmatics Magnets, Shah Alam."
    items = [("/selection-checklist.html", "Free download · PDF", "Selection checklist (1 page)", "What to measure, what to choose and what to confirm before you order.", True)] + \
            [("/%s.html" % g["slug"], g["tag"], g["h1"], g["card"], False) for g in GUIDES]
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Resources", "url": SITE + path, "description": desc,
           "isPartOf": {"@type": "WebSite", "url": SITE + "/"},
           "hasPart": [{"@type": "WebPage", "name": i[2], "url": SITE + i[0]} for i in items]}, breadcrumb_ld([("Home", "/"), ("Resources", path)])]
    cards = "".join('<a class="res-card reveal%s" href="%s"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="go">Open →</span></a>' % (" feature" if f else "", u, t, h, p) for u, t, h, p, f in items)
    main = '''    <section class="section tight"><div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · <span>Resources</span></nav>
      <div class="section-head compact"><span class="eyebrow">Resources</span><h1 style="font-size:clamp(1.8rem,4vw,2.6rem);">Short guides and a free checklist</h1><p>Written for buyers, QA and engineers. Each takes a couple of minutes.</p></div>
      <div class="res-grid">%s</div>
      %s
    </div></section>
    %s''' % (cards, '<p class="sec-note">General guidance. ' + CERT + '</p>', CTA)
    write("resources.html", shell(path, title, desc, ld, main))
    write("resources.md", "# Resources — Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s\n\n%s\n" % (SITE, path, "\n".join("- [%s](%s%s): %s" % (i[2], SITE, i[0].replace(".html", ".md"), i[3]) for i in items)))

for g in GUIDES: guide_page(g)
checklist_pages(); quote_page(); privacy(); resources()
print("built marketing pages")
