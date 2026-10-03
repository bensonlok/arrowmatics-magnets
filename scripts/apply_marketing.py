#!/usr/bin/env python3
"""One-off transform (kept for reference; do not re-run): wire marketing blocks into hand-written pages."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from components import *
D = os.path.join(os.path.dirname(__file__), "..", "main-app")
rd = lambda f: open(os.path.join(D, f)).read()
def wr(f, s): open(os.path.join(D, f), "w").write(s)
PAGES = ["index", "magnetic-separators", "plate-magnets", "ndfeb-magnets", "smco-magnets", "faq"]
PREFIX = dict(index="h", **{"magnetic-separators": "s", "plate-magnets": "p", "ndfeb-magnets": "n", "smco-magnets": "m", "faq": "f"})

for pg in PAGES:
    s = rd(pg + ".html")
    # nav + footer
    s = s.replace('<a href="/about.html">About</a>', '<a href="/resources.html">Resources</a>\n        <a href="/about.html">About</a>', 1) if 'href="/resources.html">Resources</a>\n        <a href="/about.html">About</a>' not in s else s
    s = re.sub(r'(<a href="/about\.html">About Arrowmatics</a>)(\s*)(<a href="/faq\.html">FAQ</a>)', r'<a href="/resources.html">Resources</a>\2\1\2\3\2<a href="/privacy.html">Privacy</a>', s, 1)
    # assets
    s = s.replace("?v=ui1", "?v=" + ASSET_V)
    if "/js/leads.js" not in s:
        s = re.sub(r'(<script src="/js/ui\.js[^"]*" defer></script>)', r'\1\n  <script src="/js/site-config.js?v=%s" defer></script>\n  <script src="/js/leads.js?v=%s" defer></script>' % (ASSET_V, ASSET_V), s, 1)
    # quote + checklist (+ trust on home)
    if 'id="quote"' not in s and pg != "faq":
        block = quote_section(PREFIX[pg] + "q", pg)
        if pg == "index":
            block = TRUST + block
            anchor = '<section class="section tight section-alt" id="faq-teaser">'
        else:
            anchor = '<section class="cta-band">'
        i = s.index(anchor)
        s = s[:i] + block.lstrip(" ").replace("\n    ", "\n    ", 1) + "\n    " + s[i:]
    wr(pg + ".html", s)

# ---------------- FAQ: buyer questions first + two new answers
s = rd("faq.html")
NEW = [("Is Arrowmatics ISO 22000 or HACCP certified?",
        "No. Arrowmatics is not itself certified to ISO 22000, HACCP or GMP, and we publish no certificates. We supply fit-for-purpose, hygienic-design magnets for food plants working to those standards; your own quality system and certification stay yours. Confirm any document you need at quotation."),
       ("Can I send a photo instead of a drawing?",
        "Yes. Upload a photo, sketch or drawing to the Magnet Expert chat, or send it on WhatsApp +60 12-211 2522. Include the material, the size and where the magnet will go. We aim to reply within 1–3 hours (Malaysia business hours).")]
m = re.search(r'(<div class="container" style="max-width:800px;">\s*)((?:<article class="faq-item">.*?</article>\s*)+)(</div>)', s, re.S)
arts = re.findall(r'<article class="faq-item">.*?</article>', m.group(2), re.S)
def q_of(a): return re.search(r'<h2>(.*?)</h2>', a, re.S).group(1).strip()
by = {q_of(a): a for a in arts}
def newart(q, a): return '<article class="faq-item">\n          <h2>%s</h2>\n          <p>%s</p>\n        </article>' % (q, a)
first_q = ["How do I get a written quote?", "Do you publish prices in RM?", "How fast does Arrowmatics Magnets reply to enquiries?"]
order = [by[q] for q in first_q if q in by] + [newart(*NEW[1]), newart(*NEW[0])]
order += [by[q] for q in ["Do you supply food-grade grate magnets in Malaysia?", "Where is Arrowmatics Magnets based?"] if q in by]
used = set(order)
order += [a for a in arts if a not in used]
s = s[:m.start(2)] + "\n\n        ".join(order) + "\n\n      " + s[m.end(2):]
# JSON-LD
def reld(mm):
    data = json.loads(mm.group(1))
    if data.get("@type") != "FAQPage": return mm.group(0)
    ents = {e_["name"]: e_ for e_ in data["mainEntity"]}
    for q, a in NEW: ents[q] = {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    names = first_q + [NEW[1][0], NEW[0][0], "Do you supply food-grade grate magnets in Malaysia?", "Where is Arrowmatics Magnets based?"]
    lst = [ents[n] for n in names if n in ents] + [e_ for n, e_ in ents.items() if n not in names]
    data["mainEntity"] = lst
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>'
s = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', reld, s, flags=re.S)
wr("faq.html", s)
md = rd("faq.md")
add = "\n## Buyer questions first\n\n" + "\n\n".join("### %s\n\n%s" % (q, a) for q, a in
      [("How do I get a written quote?", "WhatsApp +60 12-211 2522 with a photo, the material, the size and where it fits. Written quote with size, grade and build confirmed."),
       ("Do you publish prices in RM?", "No. Quotes are written, per application."),
       ("How fast do you reply?", "We aim to reply within 1–3 hours in Malaysia business hours; a target, not a guarantee.")] + NEW) + "\n"
md = md.replace("Contact: WhatsApp +60 12-211 2522.\n", "Contact: WhatsApp +60 12-211 2522.\n" + add, 1)
wr("faq.md", md)
print("applied")
