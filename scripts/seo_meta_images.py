"""SEO phase 2: titles <=60, descriptions <=160, WebP <picture> with JPG/PNG fallback,
lazy-load + real width/height, Product schema on existing product pages. Idempotent."""
import re, html, json, pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent / "main-app"
META = {
 "index.html": ("Magnetic Separators & Custom Magnets Malaysia | Arrowmatics",
   "Grate, bullet, drawer, plate and overband magnets plus NdFeB and SmCo, made to your size in Shah Alam. Food-grade stainless options. WhatsApp a photo."),
 "magnetic-separators.html": ("Magnetic Separators Malaysia | Grate, Bullet, Plate",
   "Grate, bullet, drawer, pulley, plate, overband and liquid-trap magnetic separators for Malaysian plants. Typical 10,000–13,000 gauss. WhatsApp a quote."),
 "plate-magnets.html": ("Full-Weld Plate Magnets up to 10,000 Gauss | Arrowmatics",
   "Full-weld SS304/316/316L plate magnets, up to ~10,000 gauss typical, for food plants working to HACCP / ISO 22000. Arrowmatics is not itself certified."),
 "ndfeb-magnets.html": ("NdFeB Rare-Earth Magnets Malaysia | N35–N52 | Arrowmatics",
   "NdFeB rare-earth magnets in grades N35–N52 and high-temperature series. Discs, blocks, rings or to your drawing, from Shah Alam. WhatsApp a quote."),
 "smco-magnets.html": ("SmCo Magnets Malaysia | Samarium Cobalt | Arrowmatics",
   "Samarium cobalt (SmCo) rare-earth magnets for high temperature and corrosion resistance. Sizes to your drawing, from Shah Alam. WhatsApp a quote."),
 "faq.html": ("FAQ | Magnetic Separators, NdFeB & SmCo | Arrowmatics",
   "Answers on choosing magnetic separators, suspension magnets, gauss levels, stainless grades, NdFeB and SmCo magnets, cleaning and quotes in Malaysia."),
 "industries.html": ("Magnets by Industry Malaysia | Arrowmatics Magnets",
   "Magnetic separators for food, pharma, plastics, recycling and chemical plants in Malaysia. Pick your industry and see the right magnet types."),
 "food-industry-magnets.html": ("Magnets for Food Plants Malaysia | Arrowmatics",
   "Grate, drawer, plate and liquid-trap magnets for food plants in Malaysia. Stainless, full-weld options for HACCP / ISO 22000 programmes. WhatsApp us."),
 "pharma-cosmetics-magnets.html": ("Magnets for Pharma & Cosmetic Powders | Arrowmatics",
   "Keep fine iron out of pharma, nutraceutical and cosmetic powder blends with stainless grate, drawer and bullet magnets. Made to size in Malaysia."),
 "plastics-industry-magnets.html": ("Magnets for Plastics & Extrusion Malaysia | Arrowmatics",
   "Drawer, grate and bullet magnets that protect extruders and moulding machines from tramp iron. Made to fit your feed throat. WhatsApp a quote."),
 "recycling-industry-magnets.html": ("Magnets for Recycling & Aggregates Malaysia | Arrowmatics",
   "Overband, suspension and magnetic pulley separators that pull tramp iron off conveyors in recycling, scrap and aggregates. Quoted to your belt."),
 "chemicals-industry-magnets.html": ("Magnets for Chemicals & Bulk Malaysia | Arrowmatics",
   "Bullet, grate and liquid-trap magnets for chemical powders, pipelines and liquids. Stainless 304/316 builds made to size. WhatsApp a quote."),
 "about.html": ("About Arrowmatics Magnets | Shah Alam, Malaysia",
   "Arrowmatics AI Sdn Bhd supplies magnetic separators, NdFeB and SmCo magnets from Shah Alam to plants across Malaysia. Sensible, simple, systematic."),
 "resources.html": ("Magnetic Separator Guides & Checklist | Arrowmatics",
   "Free magnetic separator selection checklist and short guides: which separator you need, what to send for a quote, and plate magnet cleaning."),
 "selection-checklist.html": ("Free Magnetic Separator Selection Checklist | Arrowmatics",
   "A free 1-page checklist: what to measure, what to send and what to confirm before you order a magnetic separator."),
 "guide-which-magnetic-separator.html": ("Which Magnetic Separator Do I Need? | Arrowmatics",
   "A quick guide to choosing between grate, bullet, drawer, plate, pulley, overband and liquid-trap magnets by product and process point."),
 "guide-what-to-send-for-a-magnet-quote.html": ("What to Send for a Magnet Quote | Arrowmatics",
   "The sizes, product details and photos to send so we can quote a magnetic separator quickly and correctly."),
 "guide-plate-magnet-inspection-cleaning.html": ("Plate Magnet Inspection & Cleaning Checklist | Arrowmatics",
   "How to inspect, clean and record checks on a plate magnet, step by step, for food and process plants."),
 "request-quote.html": ("Request a Magnet Quote | Arrowmatics Magnets Shah Alam",
   "Request a written quote for magnetic separators or custom magnets. Send size, product and a photo. Reply within 1–3 business hours."),
 "privacy.html": ("Privacy Notice | Arrowmatics Magnets",
   "How Arrowmatics AI Sdn Bhd uses the details you send through magnets.com.my quote and checklist forms."),
 "checklist-print.html": ("Magnetic Separator Checklist (Printable) | Arrowmatics", None),
 "drawer-magnet.html": ("Drawer Magnet Malaysia | Hopper & Extruder Feed", None),
 "grate-magnet.html": ("Grate Magnet Malaysia | Hopper & Housing | Arrowmatics", None),
}
for f,(t,d) in META.items():
    assert len(t) <= 60, (f, len(t)); assert d is None or len(d) <= 160, (f, len(d))

PRODUCT = {
 "plate-magnets.html": ("Full-Weld Plate Magnet", "plate-magnet-10000g.jpg"),
 "ndfeb-magnets.html": ("NdFeB Rare-Earth Magnets", "real-ndfeb-1.jpg"),
 "smco-magnets.html": ("SmCo Samarium Cobalt Magnets", "real-smco-1.jpg"),
}
BASE = "https://magnets.com.my/"
dims = {}
def webp(src):
    p = ROOT / src.lstrip("/")
    if not p.exists() or p.suffix.lower() not in (".jpg", ".jpeg", ".png"): return None
    w = p.with_suffix(".webp")
    if not w.exists():
        im = Image.open(p); im = im.convert("RGBA" if im.mode in ("RGBA","P","LA") else "RGB")
        im.save(w, "WEBP", quality=78, method=6)
    if p not in dims: dims[p] = Image.open(p).size
    return w

IMG = re.compile(r'(<picture>\s*<source[^>]*>\s*)?(<img\b[^>]*>)(\s*</picture>)?', re.S)
def fix_img(m):
    if m.group(1): return m.group(0)       # already wrapped
    tag = m.group(2)
    src = re.search(r'src="([^"]+)"', tag)
    if not src: return tag
    s = src.group(1)
    if s.startswith("http") or "logo" in s or "favicon" in s: return tag
    w = webp(s)
    if not w: return tag
    W, H = dims[ROOT / s.lstrip("/")]
    tag = re.sub(r'\s(width|height)="[^"]*"', "", tag)
    tag = tag.replace("<img", f'<img width="{W}" height="{H}"', 1)
    if "fetchpriority" not in tag and "loading=" not in tag:
        tag = tag.replace("<img", '<img loading="lazy"', 1)
    if "decoding=" not in tag: tag = tag.replace("<img", '<img decoding="async"', 1)
    ws = s.rsplit(".", 1)[0] + ".webp"
    return f'<picture><source srcset="{ws}" type="image/webp">{tag}</picture>'

for f in sorted(ROOT.glob("*.html")):
    t = f.read_text(); o = t
    if f.name in META:
        nt, nd = META[f.name]
        t = re.sub(r"<title>.*?</title>", "<title>" + html.escape(nt, quote=False) + "</title>", t, count=1, flags=re.S)
        if nd: t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(nd)+m.group(2), t, count=1)
    if f.name in PRODUCT and '"@type": "Product"' not in t:
        name, img = PRODUCT[f.name]
        d = re.search(r'<meta name="description" content="([^"]*)"', t).group(1)
        obj = {"@context":"https://schema.org","@type":"Product","name":name,"url":BASE+f.name,"image":BASE+"images/"+img,
               "description":html.unescape(d),"brand":{"@type":"Brand","name":"Arrowmatics Magnets"},
               "manufacturer":{"@type":"Organization","name":"Arrowmatics Magnets","legalName":"Arrowmatics AI Sdn Bhd","url":BASE},"category":"Industrial magnets"}
        t = t.replace("</head>", '  <script type="application/ld+json">\n'+json.dumps(obj, indent=2, ensure_ascii=False)+"\n  </script>\n</head>", 1)
    t = IMG.sub(fix_img, t)
    if t != o: f.write_text(t); print("updated", f.name)
