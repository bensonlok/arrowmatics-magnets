#!/usr/bin/env python3
"""One-off: short first screen + Read-more accordions on key pages (kept for reference)."""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from components import *
D = os.path.join(os.path.dirname(__file__), "..", "main-app")

def rd(f): return open(os.path.join(D, f)).read()
def wr(f, s): open(os.path.join(D, f), "w").write(s)

def page_hero_block(s):
    i = s.index('<div class="page-hero">')
    # end: matching close = the "  </div>\n\n" before expert-band
    j = s.index('  <section class="expert-band"', i)
    return i, j

def strip_strip(s):
    return re.sub(r'\n    <div class="container" style="padding-top:1\.5rem;">\n      <p class="easy-strip">.*?</p>\n    </div>\n', '\n', s, flags=re.S)

def readmore(body, label="Read more"):
    return '<details class="readmore"><summary>%s</summary><div class="rm-body">%s</div></details>' % (label, body)

def accordion_answers(s):
    """answer-box: keep heading + first paragraph, fold the rest into Read more."""
    def fix(m):
        inner = m.group(2)
        ps = re.findall(r'<p[ >].*?</p>', inner, re.S)
        if len(ps) < 2: return m.group(0)
        head = inner[:inner.index(ps[0]) + len(ps[0])]
        rest = inner[inner.index(ps[0]) + len(ps[0]):]
        return m.group(1) + head + "\n          " + readmore(rest.strip()) + "\n        </div>"
    return re.sub(r'(<div class="answer-box">)(.*?)</div>(?=\s*\n\s*(?:<|$))', lambda m: fix(m) if m.group(2).count("<p") > 1 else m.group(0), s, flags=re.S)

def swap_hero(f, **kw):
    s = rd(f)
    s = strip_strip(s)
    i, j = page_hero_block(s)
    old = s[i:j]
    s = s[:i].rstrip() + "\n\n" + kw["html"] + "\n" + s[j:]
    return s

# ---------------- separators ----------------
s = rd("magnetic-separators.html"); s = strip_strip(s)
i, j = page_hero_block(s); old = s[i:j]
oldp = re.search(r"<h1>.*?</h1>\s*(<p>.*?</p>)", old, re.S).group(1)
h = hero([("Home", "/"), ("Magnetic separators", None)], "", 'Magnetic separators <span class="accent">made to fit</span>',
         "Grate, drawer, plate, suspension and liquid-trap magnets — send a photo and get a written quote.",
         [("magnet", "Grate · drawer · plate · suspension"), ("shield", "304 / 316 / 316L available"), ("custom", "Made to your line")],
         "/images/grate-magnet-large-bars-stainless-full-length.jpg", "Full-length view of a stainless steel grate magnet with parallel large-diameter magnetic bars", "Large-bar grate magnet", (1200, 900),
         extra=readmore(oldp.replace("<p>", "<p>", 1)))
s = s[:i].rstrip() + "\n\n" + h + "\n" + HOW + s[j:]
# fold the inline gallery in the first answer-box
a = s.index('<h3 class="gallery-cat">Grate magnet</h3>')
b = s.index('<p>Arrowmatics Magnets supplies these separators', a)
s = s[:a] + '</div></details>'.join(['<details class="readmore"><summary>See separator photos by type</summary><div class="rm-body">' + s[a:b], '']) + s[b:]
wr("magnetic-separators.html", s)

# ---------------- plate ----------------
s = rd("plate-magnets.html")
i, j = page_hero_block(s)
h = hero([("Home", "/"), ("Separators", "/magnetic-separators.html"), ("Plate magnets", None)], "Food-grade · Full weld · Made to your drawing",
         "Full-weld plate magnets. <span class=\"accent\">Up to 10,000 Gauss.</span>",
         "<strong>For food plants working to HACCP / ISO 22000. Arrowmatics is not itself certified</strong> — we supply hygienic-design stainless plate magnets that support your own programme.",
         [("shield", "SS304 / 316 / 316L"), ("check", "100% full weld"), ("magnet", "Up to ~10,000 Gauss (typical)")],
         "/images/plate-magnet-10000g.jpg", "Full-weld stainless steel plate magnet on a workshop floor", "Full-weld plate magnet", (1400, 1050),
         extra=readmore('<p>Continuous-weld SS304/SS316/SS316L stainless housings with a smooth, cleanable finish. Strong ferrous capture you can inspect, clean and trust. See the <a href="#checklist">hygiene checklist</a>.</p>'))
# keep the metric-rail that follows
s = s[:i].rstrip() + "\n\n" + h + "\n" + s[j - 0:]
# metric rail currently sits between hero and band; make sure order: hero, how, rail, band
s = s.replace('\n  <div class="metric-rail"', '\n' + HOW + '\n  <div class="metric-rail"', 1) if 'class="how"' not in s else s
s = accordion_answers(s)
# plate FAQ -> accordions
def faq_to_acc(m):
    return '        <details class="acc"><summary><h3>%s</h3></summary><div class="rm-body"><p>%s</p></div></details>' % (m.group(1), m.group(2))
k = s.index('id="plate-faq"'); k2 = s.index('</section>', k)
seg = re.sub(r'<article class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</article>', lambda m: faq_to_acc(m), s[k:k2], flags=re.S)
s = s[:k] + seg + s[k2:]
wr("plate-magnets.html", s)

# ---------------- ndfeb ----------------
s = rd("ndfeb-magnets.html"); s = strip_strip(s)
i, j = page_hero_block(s); old = s[i:j]
oldp = re.search(r"<h1>.*?</h1>\s*(<p>.*?</p>)", old, re.S).group(1)
grid = re.search(r'<h3 class="gallery-cat">.*?</div>\n(?=\s*\n?\s*</div>)', old, re.S).group(0)
h = hero([("Home", "/"), ("NdFeB magnets", None)], "", 'NdFeB magnets, <span class="accent">N35–N52</span>',
         "Sintered neodymium magnets, cut to your drawing — send a photo or a sketch for a written quote.",
         [("magnet", "Grades N35 to N52"), ("custom", "Shape and size to drawing"), ("shield", "Coatings quoted to suit")],
         "/images/real-ndfeb-1.jpg", "NdFeB rare-earth magnet blocks", "NdFeB magnets", (1024, 768),
         extra=readmore(oldp))
s = s[:i].rstrip() + "\n\n" + h + "\n" + HOW + s[j:]
m_ = s.index("  <main>") + len("  <main>")
s = s[:m_] + '\n    <section class="section tight"><div class="container"><details class="readmore"><summary>See more NdFeB photos</summary><div class="rm-body">' + grid + '</div></details></div></section>\n' + s[m_:]
wr("ndfeb-magnets.html", s)

# ---------------- smco ----------------
s = rd("smco-magnets.html"); s = strip_strip(s)
i, j = page_hero_block(s); old = s[i:j]
oldp = re.search(r"<h1>.*?</h1>\s*(<p>.*?</p>)", old, re.S).group(1)
grid = re.search(r'<h3 class="gallery-cat">.*?</div>\n(?=\s*</div>)', old, re.S).group(0)
h = hero([("Home", "/"), ("SmCo magnets", None)], "", 'SmCo magnets, <span class="accent">samarium cobalt</span>',
         "For heat and corrosion duty where NdFeB will not do — send your drawing or a photo for a written quote.",
         [("magnet", "SmCo5 / Sm2Co17"), ("shield", "Heat & corrosion duty"), ("custom", "Quoted to drawing")],
         "/images/real-smco-2.jpg", "Samarium cobalt disc magnets stacked", "SmCo magnets", (1000, 1000),
         extra=readmore(oldp))
s = s[:i].rstrip() + "\n\n" + h + "\n" + HOW + s[j:]
m_ = s.index("  <main>") + len("  <main>")
s = s[:m_] + '\n    <section class="section tight"><div class="container"><details class="readmore"><summary>See SmCo shapes: discs, blocks, pots, rings</summary><div class="rm-body">' + grid + '</div></details></div></section>\n' + s[m_:]
s = accordion_answers(s)
wr("smco-magnets.html", s)

# ---------------- faq: just drop the strip, shorten nothing ----------------
s = rd("faq.html"); s = strip_strip(s); wr("faq.html", s)

# ---------------- common: asset versions + ui.js + og images ----------------
for f in ["magnetic-separators", "plate-magnets", "ndfeb-magnets", "smco-magnets", "faq"]:
    s = rd(f + ".html")
    s = s.replace("css/styles.css?v=expert1", "css/styles.css?v=%s" % ASSET_V).replace("/css/magnet-expert-chat.css?v=expert1", "/css/magnet-expert-chat.css?v=%s" % ASSET_V)
    s = s.replace('<script src="/js/magnet-expert-chat.js?v=expert1" defer></script>', '<script src="/js/magnet-expert-chat.js?v=%s" defer></script>\n  <script src="/js/ui.js?v=%s" defer></script>' % (ASSET_V, ASSET_V))
    wr(f + ".html", s)
print("ok")
