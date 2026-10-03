#!/usr/bin/env python3
"""Generate industry pages, industries hub and About page (+ .md mirrors) into main-app/.
Run from repo root:  python3 scripts/build_pages.py
Only facts already on the site are used. No stats, customers, certifications or prices."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from components import *

OUT = os.path.join(os.path.dirname(__file__), "..", "main-app")
WA_SVG = open("/tmp/wa_svg.txt").read() if os.path.exists("/tmp/wa_svg.txt") else ""
if not WA_SVG:
    import re
    WA_SVG = re.search(r'<a class="wa-fab".*?>\s*(<svg.*?</svg>)\s*</a>', open(os.path.join(OUT, "faq.html")).read(), re.S).group(1)

NOTE_CERT = "Arrowmatics is not itself certified to ISO 22000, HACCP or GMP, and publishes no certificates. We supply fit-for-purpose magnets for plants working to those standards; your own quality system, validation and certification stay yours. Confirm any document or standard you need at quotation."

IND = [
 dict(slug="food-industry-magnets", short="Food", name="Food & ingredient plants",
  title="Magnets for Food Plants Malaysia | Grate, Drawer & Plate | Arrowmatics",
  desc="Stainless grate, drawer and plate magnets for food and ingredient powders in Malaysia. For plants working to HACCP / ISO 22000. Arrowmatics is not itself certified. WhatsApp +60 12-211 2522.",
  h1="Magnets for <span class=\"accent\">food plants</span>",
  lead="Catch fine iron before it reaches the pack — stainless magnets made to your hopper, chute or pipe.",
  eyebrow="Food · ingredients · packing",
  chips=[("shield","Stainless 304 / 316 / 316L available"),("custom","Made to your hopper or chute"),("check","For plants working to HACCP / ISO 22000")],
  img="/images/plate-magnet-10000g.jpg", alt="Full-weld stainless steel plate magnet for food plants", cap="Full-weld plate magnet", wh=(1400,1050),
  ogimg="/images/plate-magnet-10000g.jpg",
  intro="Food processors use stainless grate, drawer and plate magnets in hoppers, sifters, chutes and over conveyors to catch fine ferrous fragments from wear and rust before metal detectors or finished goods. Full-weld construction is available built to order, so there are no screws or crevices for deposit to sit in; confirm the build at quotation.",
  cards=[("/magnetic-separators.html#types","/images/real-hopper-grate-1.jpg","Round stainless hopper grate magnet with handle","Grate / hopper magnet","Dry powders and grains falling through a hopper or chute."),
         ("/plate-magnets.html","/images/plate-magnet-10000g.jpg","Full-weld stainless plate magnet","Plate magnet","Chute wall or above a conveyor; easy to wipe and inspect."),
         ("/magnetic-separators.html#liquid-line-trap","/images/real-liquid-trap-1.jpg","Stainless liquid-line magnetic trap","Liquid-line trap","Sauces, pastes and liquids moving through a pipe.")],
  send=["Product (powder, grain, liquid)","Hopper, chute or pipe size","Food-grade needs and cleaning method","Photo of the spot"],
  faq=[("Which magnet suits a food powder hopper?","A grate or drawer magnet usually suits dry powders falling through a hopper or chute. Stainless 304, 316 and 316L are available; confirm the grade, bar spacing and build at quotation. Send a photo of the hopper opening for a recommendation."),
       ("Are your food-plant magnets certified?","No. "+NOTE_CERT)]),
 dict(slug="pharma-cosmetics-magnets", short="Pharma & cosmetics", name="Pharma, nutraceutical & cosmetic powders",
  title="Magnets for Pharma, Nutraceutical & Cosmetic Powders | Arrowmatics Malaysia",
  desc="Stainless drawer and grate magnets for powder blending and filling in pharma, nutraceutical and cosmetic plants in Malaysia. Arrowmatics is not itself certified. WhatsApp +60 12-211 2522.",
  h1="Magnets for <span class=\"accent\">pharma &amp; cosmetic</span> powders",
  lead="Keep fine iron out of powder blends — stainless drawer and grate magnets sized to your outlet or hopper.",
  eyebrow="Pharma · nutraceutical · cosmetics",
  chips=[("shield","Stainless 304 / 316 / 316L available"),("layers","Drawer or grate, to your outlet"),("check","Documents confirmed at quotation")],
  img="/images/real-drawer-1.jpg", alt="Double-drawer stainless magnetic separator housing on a pallet", cap="Drawer separator", wh=(1400,1050),
  ogimg="/images/real-drawer-1.jpg",
  intro="Powder blending, sieving and filling steps are where small ferrous fragments from equipment wear tend to show up. Drawer and grate magnets sit under a hopper or in a spout and pull out for cleaning. Full-weld stainless builds are available, built to order. We make no pharma or GMP certification claim for ourselves; tell us which documents your quality system needs and we will confirm what can be supplied at quotation.",
  cards=[("/magnetic-separators.html#types","/images/real-drawer-1.jpg","Double-drawer stainless magnetic separator","Drawer magnet","Rows of magnetic bars that slide out for cleaning without stripping the line."),
         ("/magnetic-separators.html#types","/images/real-hopper-grate-1.jpg","Round stainless hopper grate magnet","Grate / hopper magnet","Bars across a hopper or outlet for free-flowing powder."),
         ("/magnetic-separators.html#bars-full-weld","/images/real-bars-1.jpg","Polished stainless magnetic bar","Magnetic bars (full weld available)","Single bars or frames; full weld is built to order.")],
  send=["Powder type and particle size","Outlet, hopper or spout size","Cleaning method and finish needed","Any documents your QA requires"],
  faq=[("Can you supply magnets with pharma or GMP certificates?","We make no pharma or GMP certification claim and publish no certificates. Tell us which documents your quality system needs; we will confirm what can be supplied at quotation, with no promises beforehand."),
       ("Drawer or grate magnet for a powder outlet?","Both suit free-flowing powder. A drawer magnet slides out for cleaning in a housing; a grate sits across a hopper or chute. Send the outlet size and a photo and the Magnet Expert will help you choose.")]),
 dict(slug="plastics-industry-magnets", short="Plastics", name="Plastics compounding & extrusion",
  title="Magnets for Plastics Compounding & Extrusion Malaysia | Arrowmatics",
  desc="Hopper grate, drawer and bullet magnets that catch tramp iron in pellets and regrind before extruders and moulds. Made to size in Shah Alam, Malaysia. WhatsApp +60 12-211 2522.",
  h1="Magnets that protect your <span class=\"accent\">extruder</span>",
  lead="Catch tramp iron in pellets and regrind at the hopper — before it reaches screws, dies and moulds.",
  eyebrow="Plastics · compounding · extrusion",
  chips=[("magnet","Hopper grate, drawer, bullet"),("custom","Made to your inlet size"),("pin","Shah Alam · Malaysia-wide")],
  img="/images/real-hopper-grate-1.jpg", alt="Round hopper grate magnet with drawer handle", cap="Hopper grate magnet", wh=(1000,750),
  ogimg="/images/real-hopper-grate-1.jpg",
  intro="Tramp iron in pellets or regrind can damage screws, dies and moulds, and it is cheaper to catch it at the hopper. Hopper grate and drawer magnets suit gravity feed; bullet magnets suit pipelines and pneumatic conveying. Rare-earth separator designs we commonly quote sit around 10,000–13,000 gauss (typical; confirm per application).",
  cards=[("/magnetic-separators.html#types","/images/real-hopper-grate-1.jpg","Round hopper grate magnet","Hopper grate","Across the inlet of a hopper for pellets and regrind."),
         ("/magnetic-separators.html#types","/images/real-drawer-2.jpg","Drawer magnet for a vertical pipe","Drawer magnet","Multi-row capture under hoppers or before extruders."),
         ("/magnetic-separators.html#types","/images/real-bullet-1.jpg","Bullet magnet front and side views","Bullet magnet","In a pipe for pneumatic or gravity lines.")],
  send=["Pellet or regrind size and flow rate","Hopper or pipe size","Photo of the inlet","Temperature, if the material is hot"],
  faq=[("Which magnet for plastic pellets before an extruder?","A hopper grate or drawer magnet suits gravity-fed pellets; a bullet magnet suits a pipe or pneumatic line. Send the inlet size, pellet size and a photo, and we will recommend a type and quote it in writing."),
       ("Can the magnet be made to fit our hopper?","Yes, sizes, housings and drawing-based builds are worth exploring; feasibility, size and grade are confirmed at quotation.")]),
 dict(slug="recycling-industry-magnets", short="Recycling & aggregates", name="Recycling, scrap & aggregates",
  title="Magnets for Recycling, Scrap & Aggregates Malaysia | Overband & Pulley | Arrowmatics",
  desc="Suspension (overband) magnets, magnetic pulleys and drum separators for recycling, scrap and aggregates conveyors in Malaysia. Quoted to belt width and duty. WhatsApp +60 12-211 2522.",
  h1="Pull iron off your <span class=\"accent\">conveyor</span>",
  lead="Overband, suspended plate and pulley magnets that clear tramp iron from bulk material on the belt.",
  eyebrow="Recycling · scrap · aggregates",
  chips=[("magnet","Overband & suspended plate"),("custom","Quoted to belt width and duty"),("pin","Shah Alam · Malaysia-wide")],
  img="/images/suspension-overband-magnet-yellow-frame-workshop.jpg", alt="Yellow overband suspension magnet frame with hanging lugs and black ribbed belt on a workshop floor", cap="Overband suspension magnet", wh=(1200,900),
  ogimg="/images/suspension-overband-magnet-yellow-frame-workshop.jpg",
  intro="Tramp iron riding on a belt hurts crushers, screens and downstream equipment. A suspension magnet hangs over the conveyor and pulls iron out of the burden: overband (self-cleaning) types carry it off on a running belt, suspended plates are cleaned by hand. A magnetic pulley at the head end splits ferrous from non-magnetic material. Sizes are quoted to belt width, belt speed, burden depth and hanging height.",
  cards=[("/magnetic-separators.html#suspension-magnets","/images/suspension-overband-magnet-self-cleaning-belt.jpg","Self-cleaning overband magnet seen along its belt","Overband (self-cleaning)","Running belt carries captured iron to a discharge point."),
         ("/magnetic-separators.html#suspension-magnets","/images/suspension-plate-magnet-yellow-four-eyebolts.jpg","Yellow suspended plate magnet with four eyebolts","Suspended plate","Fixed plate over the belt, cleaned by hand."),
         ("/magnetic-separators.html#types","/images/real-drum-1.jpg","Magnetic drum separator with motor","Drum / pulley separators","Head-end or drum separation of ferrous material.")],
  send=["Belt width and speed","Burden depth and hanging height","What you need to remove","Photo of the conveyor"],
  faq=[("Overband or suspended plate magnet for a conveyor?","Overband magnets have a running belt and suit continuous or heavier tramp-iron loads; suspended plates are fixed and suit lighter loads with easy access for hand cleaning. Send belt width, burden depth and hanging height for a recommendation."),
       ("What do you need to quote a conveyor magnet?","Belt width, belt speed, burden depth, hanging height, the iron you need to remove, and ideally a photo. Size, field strength and finish are confirmed at quotation.")]),
 dict(slug="chemicals-industry-magnets", short="Chemicals", name="Chemicals & bulk materials",
  title="Magnets for Chemicals & Bulk Materials Malaysia | Bullet, Grate & Liquid Trap | Arrowmatics",
  desc="Bullet, grate, drawer and liquid-line magnetic traps in stainless for chemical powders, liquids and bulk materials in Malaysia. Made to size. WhatsApp +60 12-211 2522.",
  h1="Magnets for <span class=\"accent\">chemicals</span> &amp; bulk",
  lead="Iron out of powders, pipes and liquids — stainless bullet, grate and liquid-trap magnets made to size.",
  eyebrow="Chemicals · powders · liquids",
  chips=[("shield","304 / 316 / 316L available"),("drop","Powders, pipes & liquids"),("custom","Made to your pipe or hopper")],
  img="/images/real-bullet-2.jpg", alt="Bullet magnet with its internal magnetic core assembly pulled out", cap="Bullet magnet · core pulled out", wh=(800,800),
  ogimg="/images/real-bullet-2.jpg",
  intro="Chemical and bulk-material lines move powders, liquids and slurries through hoppers, pipes and pneumatic lines. Bullet magnets sit in a pipe, grate and drawer magnets in a hopper or chute, and liquid-line traps in a liquid pipeline. 316 / 316L stainless generally suits more corrosive duty (general guidance; confirm the grade at quotation). Tell us the process temperature, since heat limits the magnet choice.",
  cards=[("/magnetic-separators.html#types","/images/real-bullet-2.jpg","Bullet magnet with core assembly","Bullet magnet","Pneumatic or gravity pipelines."),
         ("/magnetic-separators.html#types","/images/real-grate-2.jpg","Heavy-duty grate magnet with conical-tipped bars","Grate / drawer magnet","Hoppers and chutes for dry powders and granules."),
         ("/magnetic-separators.html#liquid-line-trap","/images/real-liquid-trap-1.jpg","Stainless liquid-line magnetic trap","Liquid-line trap","In-line on liquid and slurry pipes.")],
  send=["Material and form (powder, liquid, slurry)","Pipe, hopper or chute size","Process temperature","Corrosion or washdown conditions"],
  faq=[("Which magnet for a chemical powder or liquid line?","Bullet magnets suit pipes and pneumatic lines, grate or drawer magnets suit hoppers and chutes, and liquid-line traps suit liquids and slurries. Send the material, size, temperature and a photo for a recommendation."),
       ("Which stainless grade for corrosive duty?","304, 316 and 316L are available. 316 / 316L generally suit more corrosive or washdown-heavy conditions. This is general guidance with no test data; confirm the grade for your chemicals at quotation.")]),
]

PERSONA = {
 "food-industry-magnets": dict(h1='Tell us what is getting into <span class="accent">your product</span>', lead="Food QA? Send a photo of the hopper or chute. We suggest a stainless magnet and quote it in writing.", cta="Send a photo of your line", q="I am in food QA and want a magnet for this hopper or chute. Photo attached."),
 "pharma-cosmetics-magnets": dict(h1='Keep fine iron out of <span class="accent">your powder blend</span>', lead="Send your outlet size or a photo. We quote a stainless drawer or grate magnet to fit.", cta="Send your outlet photo", q="I need a magnet for a powder outlet in a pharma or cosmetics line."),
 "plastics-industry-magnets": dict(h1='Protect your <span class="accent">extruder</span> from tramp iron', lead="Send a photo of your hopper inlet. We size a grate, drawer or bullet magnet to fit.", cta="Send a photo of your hopper", q="I want to protect an extruder or mould from tramp iron in pellets or regrind."),
 "recycling-industry-magnets": dict(h1='Pull iron off <span class="accent">your conveyor</span>', lead="Send a photo of the belt. We quote an overband, suspended plate or pulley magnet to fit.", cta="Send a photo of your conveyor", q="I want to remove tramp iron from a conveyor belt in a recycling or aggregates line."),
 "chemicals-industry-magnets": dict(h1='Iron out of <span class="accent">powders, pipes and liquids</span>', lead="Send a photo of the pipe or hopper. We quote a stainless bullet, grate or liquid-line magnet.", cta="Send a photo of your line", q="I want a magnet for a chemical powder or liquid line."),
}

def ind_page(d):
    pr = PERSONA[d["slug"]]
    d = dict(d, h1=pr["h1"], lead=pr["lead"])
    path = "/%s.html" % d["slug"]
    ld = [
      {"@context":"https://schema.org","@type":"Service","name":"Magnets for "+d["name"],"url":SITE+path,
       "image":SITE+d["ogimg"],"description":d["desc"],"serviceType":"Magnetic separators and magnets",
       "provider":{"@type":"LocalBusiness","@id":SITE+"/#organization","name":"Arrowmatics Magnets"},
       "areaServed":{"@type":"Country","name":"Malaysia"}},
      breadcrumb_ld([("Home","/"),("Industries","/industries.html"),(d["short"],path)]),
      faq_ld(d["faq"]),
    ]
    h = head(d["title"], d["desc"], path, d["ogimg"], ld)
    body = '<body>\n' + header("/industries.html") + "\n"
    body += hero([("Home","/"),("Industries","/industries.html"),(d["short"],None)], d["eyebrow"], d["h1"], d["lead"], d["chips"], d["img"], d["alt"], d["cap"], d["wh"], persona=pr,
                 extra='<details class="readmore"><summary>Read more</summary><div class="rm-body"><p>%s</p></div></details>' % d["intro"])
    body += HOW + BAND
    body += '''
  <main>
    <section class="section tight">
      <div class="container">
        <div class="section-head compact"><h2>Which magnet fits?</h2><p>Pick by how your material moves. Not sure? Send a photo.</p></div>
        %s
      </div>
    </section>

    <section class="section tight section-alt">
      <div class="container">
        <div class="section-head compact"><h2>What to send for a quote</h2></div>
        <ul class="chip-list">%s</ul>
        <p class="sec-note">Size, grade, gauss and build are confirmed at quotation. We publish no RM prices or stock levels; written quotes on WhatsApp.</p>
      </div>
    </section>

%s
    <section class="section tight">
      <div class="container">
        <div class="section-head compact"><h2>Quick answers</h2></div>
%s
        <p class="ind-note"><strong>Honest note:</strong> %s</p>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>Send a photo – get an answer in 1–3 business hours</h2>
        <p>We aim to reply within 1–3 hours (Malaysia business hours). Include product, size and where the magnet will go.</p>
        <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a>
        <button type="button" class="btn btn-expert-hero" data-open-magnet-expert style="margin-left:0.5rem;">Ask the Magnet Expert</button>
      </div>
    </section>
  </main>

''' % (vcards(d["cards"]), "".join("<li>%s</li>" % x for x in d["send"]), quote_section("q", d["slug"]), accordions(d["faq"]), NOTE_CERT if d["slug"] in ("food-industry-magnets","pharma-cosmetics-magnets") else "Size, grade and build are confirmed at quotation; no certificates are implied.", WA)
    body += FOOTER + "\n" + fabs(WA_SVG) + "</body>\n</html>\n"
    open(os.path.join(OUT, d["slug"] + ".html"), "w").write(h + body)
    md = "# %s — Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s · WhatsApp +60 12-211 2522\n\n%s\n\n## Which magnet fits?\n\n%s\n\n## What to send for a quote\n\n%s\n\nSize, grade, gauss and build are confirmed at quotation. No published RM prices or stock levels.\n\n## Quick answers\n\n%s\n\n## Honest note\n\n%s\n" % (
        "Magnets for " + d["name"], SITE, path, d["intro"],
        "\n".join("- **%s** — %s (%s%s)" % (c[3], c[4], SITE, c[0]) for c in d["cards"]),
        "\n".join("- " + x for x in d["send"]),
        "\n\n".join("### %s\n\n%s" % (q, a) for q, a in d["faq"]),
        NOTE_CERT if d["slug"] in ("food-industry-magnets","pharma-cosmetics-magnets") else "Size, grade and build are confirmed at quotation; no certificates are implied.")
    open(os.path.join(OUT, d["slug"] + ".md"), "w").write(md)

def hub():
    path = "/industries.html"
    title = "Magnets by Industry | Food, Pharma, Plastics, Recycling, Chemicals | Arrowmatics Malaysia"
    desc = "Which magnet for your industry? Food, pharma and cosmetics, plastics, recycling and chemicals in Malaysia. Photo-first advice and written quotes from Shah Alam. WhatsApp +60 12-211 2522."
    ld = [{"@context":"https://schema.org","@type":"CollectionPage","name":"Magnets by industry","url":SITE+path,"description":desc,
           "isPartOf":{"@type":"WebSite","url":SITE+"/"},
           "hasPart":[{"@type":"WebPage","name":"Magnets for "+d["name"],"url":SITE+"/%s.html"%d["slug"]} for d in IND]},
          breadcrumb_ld([("Home","/"),("Industries",path)])]
    h = head(title, desc, path, "/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg", ld)
    cards = [("/%s.html"%d["slug"], d["img"], d["alt"], d["name"], d["lead"]) for d in IND]
    body = '<body>\n' + header(path)
    body += hero([("Home","/"),("Industries",None)], "Industries we serve", "Magnets for <span class=\"accent\">your industry</span>",
                 "Pick your industry for the right magnet type, what to send, and quick answers.",
                 [("magnet","Separators, plate, suspension"),("custom","Made to your line"),("pin","Shah Alam · Malaysia-wide")],
                 "/images/grate-magnet-large-bars-stainless-tubes-cross-frame.jpg", "Large grate magnet with thick polished stainless steel magnetic bars in a cross frame", "Grate magnet · large bars")
    body += HOW + BAND + '''
  <main>
    <section class="section tight">
      <div class="container">
        <div class="section-head compact"><h2>Choose your industry</h2><p>Five short guides. Each links to the product pages and a quote path.</p></div>
        %s
        <p class="ind-note"><strong>Also served:</strong> OEMs and MRO (see <a href="/ndfeb-magnets.html">NdFeB</a> and <a href="/smco-magnets.html">SmCo</a> magnets). Size, grade and build are confirmed at quotation.</p>
      </div>
    </section>
    <section class="cta-band">
      <div class="container">
        <h2>Not sure which one you are?</h2>
        <p>Send a photo of your line. We aim to reply within 1–3 hours (Malaysia business hours).</p>
        <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a>
      </div>
    </section>
  </main>

''' % (vcards(cards), WA)
    body += FOOTER + "\n" + fabs(WA_SVG) + "</body>\n</html>\n"
    open(os.path.join(OUT, "industries.html"), "w").write(h + body)
    md = "# Magnets by industry — Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s · WhatsApp +60 12-211 2522\n\n%s\n\nOEMs and MRO: see NdFeB and SmCo pages.\n" % (
        SITE, path, "\n".join("- [%s](%s/%s.html): %s" % (d["name"], SITE, d["slug"], d["lead"]) for d in IND))
    open(os.path.join(OUT, "industries.md"), "w").write(md)

def about():
    path = "/about.html"
    title = "About Arrowmatics Magnets | Arrowmatics AI Sdn Bhd, Shah Alam"
    desc = "Arrowmatics Magnets is the trading name of Arrowmatics AI Sdn Bhd (1305806-W), Shah Alam, Selangor. Custom magnetic separators, NdFeB and SmCo magnets. Photo-first advice, written quotes."
    ld = [{"@context":"https://schema.org","@type":"AboutPage","name":"About Arrowmatics Magnets","url":SITE+path,"description":desc,
           "about":{"@type":"LocalBusiness","@id":SITE+"/#organization","name":"Arrowmatics Magnets","legalName":"Arrowmatics AI Sdn Bhd","identifier":"1305806-W"}},
          breadcrumb_ld([("Home","/"),("About",path)])]
    h = head(title, desc, path, "/images/grate-magnet-large-bars-stainless-full-length.jpg", ld)
    facts = [("Company","Arrowmatics AI Sdn Bhd (1305806-W), trading as Arrowmatics Magnets"),
             ("Address","No. 64, Jalan Kapar 27/89, Megah Industrial Park, Taman Alam Megah, Section 27, 40400 Shah Alam, Selangor, Malaysia"),
             ("Office tel",'<a href="tel:+60351910299">+603 5191 0299</a>'),
             ("Mobile / WhatsApp",'<a href="https://wa.me/60122112522">+60 12-211 2522</a>'),
             ("Email",'<a href="mailto:bensonlok@gmail.com">bensonlok@gmail.com</a> · <a href="mailto:arrowmatics@gmail.com">arrowmatics@gmail.com</a>'),
             ("Reply target","We aim to reply within 1–3 hours (Malaysia business hours); a target, not a guarantee")]
    body = '<body>\n' + header(path)
    body += hero([("Home","/"),("About",None)], "Shah Alam · Selangor · Malaysia-wide", "Why <span class=\"accent\">Arrowmatics</span> Magnets",
                 "We build magnets to fit your machine — you send a photo, we give plain advice and a written quote.",
                 [("camera","Photo-first advice"),("custom","Made to your drawing"),("pin","Based in Shah Alam")],
                 "/images/grate-magnet-large-bars-stainless-full-length.jpg", "Full-length view of a stainless steel grate magnet with parallel large-diameter magnetic bars", "Large-bar grate magnet")
    body += '''
  <main>
    <section class="section tight">
      <div class="container">
        <div class="section-head compact"><h2>What we do</h2></div>
        <div class="icards">
          <div class="icard reveal"><span class="ic">%(magnet)s</span><h3>Separators &amp; magnets</h3><p>Grate, drawer, plate, suspension (overband), liquid-line, bullet and pulley separators, plus NdFeB (N35–N52) and SmCo magnets.</p></div>
          <div class="icard reveal"><span class="ic">%(custom)s</span><h3>Made to fit</h3><p>Sizes, grades, housings and drawing-based builds are worth exploring. Feasibility is confirmed at quotation.</p></div>
          <div class="icard reveal"><span class="ic">%(shield)s</span><h3>Stainless options</h3><p>304, 316 and 316L are available. Full-weld construction is built to order for bars, tubes, grate and plate magnets.</p></div>
          <div class="icard reveal"><span class="ic">%(chat)s</span><h3>Plain-language advice</h3><p>The on-site Magnet Expert answers magnet questions in English, 中文 and Bahasa Malaysia; people follow up on WhatsApp.</p></div>
        </div>
      </div>
    </section>

    <section class="section tight section-alt">
      <div class="container">
        <div class="section-head compact"><h2>Company facts</h2></div>
        <div class="nap-block"><dl class="facts">%(facts)s</dl></div>
      </div>
    </section>

    <section class="section tight">
      <div class="container">
        <div class="section-head compact"><h2>How we work</h2></div>
        <details class="acc" open><summary><h3>Photo first, then a written quote</h3></summary><div class="rm-body"><p>Send a photo, sketch or drawing of your hopper, chute, pipe or conveyor, with the product and size. We recommend a type, explain why in plain words and confirm size, grade and build in a written quote on WhatsApp. There is no online cart and no published RM price list.</p></div></details>
        <details class="acc"><summary><h3>What we do not claim</h3></summary><div class="rm-body"><p>Arrowmatics is not itself certified to ISO 22000, HACCP or GMP, and we publish no certificates. For food plants working to HACCP / ISO 22000 we supply hygienic-design magnets that support your own programme. We do not publish stock levels, prices, lead times or customer names we cannot back up.</p></div></details>
        <details class="acc"><summary><h3>Where to find us</h3></summary><div class="rm-body"><p>Our registered business address is No. 64, Jalan Kapar 27/89, Megah Industrial Park, Taman Alam Megah, Section 27, 40400 Shah Alam, Selangor.</p></div></details>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>Send a photo – get an answer in 1–3 business hours</h2>
        <p>We aim to reply within 1–3 hours (Malaysia business hours).</p>
        <a class="btn btn-wa" href="%(wa)s" target="_blank" rel="noopener">WhatsApp +60 12-211 2522</a>
      </div>
    </section>
  </main>

''' % dict(magnet=icon("magnet"), custom=icon("custom"), shield=icon("shield"), chat=icon("chat"),
           facts="".join("<div><dt>%s</dt><dd>%s</dd></div>" % f for f in facts), wa=WA)
    body += BAND.replace('class="expert-band"', 'class="expert-band"') if False else ""
    body += FOOTER + "\n" + fabs(WA_SVG) + "</body>\n</html>\n"
    open(os.path.join(OUT, "about.html"), "w").write(h + body)
    md = "# About Arrowmatics Magnets\n\n> Agent-readable mirror. Canonical: %s%s\n\n%s\n\n## What we do\n\nGrate, drawer, plate, suspension (overband), liquid-line, bullet and pulley separators, plus NdFeB (N35–N52) and SmCo magnets, made to fit; stainless 304/316/316L available; full-weld built to order.\n\n## How we work\n\nPhoto or sketch first, plain-language advice, then a written quote on WhatsApp. No online cart, no published RM prices.\n\n## What we do not claim\n\nArrowmatics is not itself certified to ISO 22000, HACCP or GMP and publishes no certificates.\n" % (
        SITE, path, "\n".join("- **%s:** %s" % (k, __import__("re").sub(r"<[^>]+>", "", v)) for k, v in facts))
    open(os.path.join(OUT, "about.md"), "w").write(md)

if __name__ == "__main__":
    for d in IND: ind_page(d)
    hub(); about()
    print("built", len(IND) + 2, "pages")
