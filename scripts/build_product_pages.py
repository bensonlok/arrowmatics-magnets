"""Build 8 dedicated product pages (SEO phase 2, 2026-10-16).
Specs come ONLY from the old Arrowmatics catalogue (web.archive.org snapshots of
magnets.com.my, 2012) or the current site. Unknown values say 'contact for spec'.
Re-run: python3 scripts/build_product_pages.py  (overwrites the 8 pages + .md)."""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "main-app"
TPL = (ROOT / "plate-magnets.html").read_text()
lines = TPL.splitlines(keepends=True)
def block(start, end):
    s = next(i for i,l in enumerate(lines) if start in l)
    e = next(i for i,l in enumerate(lines) if i > s and end in l)
    return "".join(lines[s:e+1])
HEADER = block('<header class="site-header">', '/js/nav-toggle.js').replace(' aria-current="page"', '')
QUOTE = block('<section class="section tight section-alt" id="quote">', '</section>')
FOOTER = TPL[TPL.index('  <footer class="site-footer">'):]
BASE = "https://magnets.com.my/"
WA = "+60 12-211 2522"
PROVIDER = {"@type": "Organization", "name": "Arrowmatics Magnets", "legalName": "Arrowmatics AI Sdn Bhd",
            "url": BASE, "telephone": "+60122112522"}

def table(head, rows):
    h = "".join(f"<th>{html.escape(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap" style="overflow-x:auto;"><table class="spec-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def kv(items):
    return table(["Item", "Detail"], items)

P = []
# 1 Bullet
P.append(dict(slug="bullet-magnet", name="Bullet Magnet", short="Bullet magnets",
 title="Bullet Magnet Malaysia | Pipeline Separator | Arrowmatics",
 desc="Stainless bullet magnets for gravity and pneumatic pipelines. CMBullet 110–420 sizes, 1–29 m³/h. Made in Shah Alam to your pipe. WhatsApp quote.",
 h1="Bullet magnets for pipelines", eyebrow="Pipeline · Gravity or pneumatic · Stainless",
 lead="A bullet-shaped magnet core inside a stainless pipe housing. Dry powder or granules flow around it, and iron sticks to the core instead of reaching your mill, extruder or pack.",
 imgs=[("real-bullet-1.jpg","Stainless bullet magnet housing with flanged ends",600,580),("real-bullet-2.jpg","Bullet magnet core pulled out of its housing for cleaning",600,580),("real-bullet-3.jpg","Bullet magnet separator ready for pipeline fitting",800,800)],
 kv=[("Fits","Gravity and pneumatic pipelines carrying dry, free-flowing product"),("Products","Powder, granules, flour, chemicals, plastics, food, pharma and mineral materials"),("Housing","Stainless steel (304 standard; 316/316L — confirm at quotation)"),("Magnet","Rare-earth core — field strength: contact for spec per pipe size"),("Pipe connection","Contact for spec (flange or clamp to your line)"),("Custom builds","OEM and customer-designed sizes welcomed")],
 tables=[("Standard CMBullet sizes", "Dimensions in mm (A–D as on our drawing). Capacity is processing capacity in m³/h. Other sizes made to order.",
   ["Part No.","A","B","C","D","Capacity (m³/h)","Weight (kg)"],
   [["CMBullet-110",114,165,250,400,1,7],["CMBullet-140",140,200,320,470,2,13],["CMBullet-170",168,230,400,610,5,24],["CMBullet-220",219,280,500,710,9,33],["CMBullet-270",273,345,530,740,13,50],["CMBullet-320",325,390,610,870,18,60],["CMBullet-350",351,435,680,940,22,95],["CMBullet-420",426,495,760,1020,29,120]])],
 faq=[("Where does a bullet magnet go?","In a vertical or inclined pipe, gravity-fed or pneumatic. The housing bolts into the line so the product flows around the magnet core."),
      ("Which size do I need?","Start from your pipe diameter and throughput. Our standard CMBullet range covers roughly 114 mm to 426 mm housings and 1 to 29 m³/h; we confirm the size from your pipe and product."),
      ("How is it cleaned?","Open the housing and pull out the core, then wipe the captured iron off into a tray. Set the cleaning interval from how much iron you find."),
      ("What field strength is it?","It depends on pipe size and build. We do not publish a single gauss figure; ask us for the specification of the size you need."),
      ("Can it be food grade?","Stainless housings are standard. Tell us your product and cleaning method and we will confirm the stainless grade and finish at quotation."),
      ("Bullet, grate or drawer magnet?","Bullet magnets suit closed pipelines. Grate and drawer magnets suit hoppers and chutes. See the separator guide if you are unsure.")],
 related=["grate-magnet","drawer-magnet","liquid-trap-magnet","magnetic-bar"],
 industries=[("food-industry-magnets","Food plants"),("plastics-industry-magnets","Plastics"),("chemicals-industry-magnets","Chemicals & bulk")]))
# 2 Grate
P.append(dict(slug="grate-magnet", name="Grate Magnet", short="Grate magnets",
 title="Grate Magnet Malaysia | Hopper & Housing Grates | Arrowmatics",
 desc="Rare-earth grate magnets for hoppers and chutes, ~10,000–13,000 gauss typical. Single or double row housings, 100–400 mm. SS304/316L. WhatsApp quote.",
 h1="Grate magnets for hoppers and chutes", eyebrow="Hopper · Chute · Free-fall powders",
 lead="Rows of magnetic tubes in a frame, sitting across the product flow. Powder and granules fall through the gaps; iron fines stay on the tubes.",
 imgs=[("real-grate-1.jpg","Stainless grate magnet with rare-earth tubes",810,1080),("grate-magnet-large-bars-stainless-tubes-cross-frame.jpg","Large grate magnet, stainless tubes on a cross frame",1200,900),("real-hopper-grate-1.jpg","Hopper grate magnet sized to an opening",1000,750)],
 kv=[("Fits","Hopper openings, chutes, bins, free-fall dry product"),("Typical field","~10,000–13,000 gauss at the tube face (rare-earth, application-dependent)"),("Tube diameter","1 inch (25 mm) standard"),("Housing","304 or 316L stainless; mild steel on request"),("Layout","One, two or more rows; circular or square fitting"),("Builds","Easy-clean version and full-weld builds to order"),("Cleaning","Wipe-down, or pull-out drawer in housing versions")],
 tables=[("Grate magnets in housing — circular fitting, single row","All dimensions in mm. Other dimensions on request.",["Part No.","A","B","C","H"],
   [["CMhousing-C-S-100",100,160,175,200],["CMhousing-C-S-150",150,210,225,200],["CMhousing-C-S-200",200,260,275,200],["CMhousing-C-S-250",250,310,325,220],["CMhousing-C-S-300",300,360,375,220],["CMhousing-C-S-350",350,410,425,250],["CMhousing-C-S-400",400,460,475,250]]),
  ("Circular fitting, double row","All dimensions in mm.",["Part No.","A","B","C","H"],
   [["CMhousing-C-D-100",100,160,175,220],["CMhousing-C-D-150",150,210,225,250],["CMhousing-C-D-200",200,260,275,250],["CMhousing-C-D-250",250,310,325,300],["CMhousing-C-D-300",300,360,375,300],["CMhousing-C-D-350",350,410,425,330],["CMhousing-C-D-400",400,460,475,330]]),
  ("Square fitting, single row","All dimensions in mm.",["Part No.","A=B","C=D","H"],
   [["CMhousing-S-S-100",100,180,200],["CMhousing-S-S-150",150,230,200],["CMhousing-S-S-200",200,280,200],["CMhousing-S-S-250",250,330,220],["CMhousing-S-S-300",300,380,220],["CMhousing-S-S-350",350,430,220],["CMhousing-S-S-400",400,480,220]]),
  ("Square fitting, double row","All dimensions in mm.",["Part No.","A=B","C=D","H"],
   [["CMhousing-S-D-100",100,180,200],["CMhousing-S-D-150",150,230,200],["CMhousing-S-D-200",200,280,200],["CMhousing-S-D-250",250,330,220],["CMhousing-S-D-300",300,380,220],["CMhousing-S-D-350",350,430,220],["CMhousing-S-D-400",400,480,220]])],
 faq=[("What is a grate magnet used for?","Catching fine iron and tramp metal in dry, free-flowing product at a hopper or chute, before it reaches machines or the final pack."),
      ("How strong are your grate magnets?","Rare-earth grate designs we quote typically sit around 10,000–13,000 gauss at the tube face. The real figure depends on build and air gap, so we confirm it per application."),
      ("Single row or double row?","Double row gives two chances to catch iron and suits finer contamination or higher flow. Send your product and flow rate and we will advise."),
      ("Can you make it to my hopper size?","Yes. Standard housings run 100–400 mm; loose grates are made to your opening. Send the inside dimensions or a photo."),
      ("Is a full-weld grate available?","Yes, built to order for food and pharma lines. Not every model is full weld, so confirm the build at quotation."),
      ("How do I clean it?","Loose grates are lifted and wiped. In a housing, pull the drawer out by its handles and wipe the tubes into a catch box. Easy-clean versions slide the tubes out of sleeves.")],
 related=["drawer-magnet","magnetic-bar","bullet-magnet","liquid-trap-magnet"],
 industries=[("food-industry-magnets","Food plants"),("pharma-cosmetics-magnets","Pharma & cosmetics"),("plastics-industry-magnets","Plastics")]))
# 3 Drawer
P.append(dict(slug="drawer-magnet", name="Drawer Magnet", short="Drawer magnets",
 title="Drawer Magnet Malaysia | Hopper & Extruder Feed | Arrowmatics",
 desc="Drawer magnets for injection moulding, blow moulding and extruder feed throats. CMdrawer 100–250 with 3–9 bars. Stainless. WhatsApp quote.",
 h1="Drawer magnets for feed throats and hoppers", eyebrow="Plastics · Extruders · Hoppers",
 lead="A stainless housing with a pull-out drawer of magnetic bars, mounted straight onto the feed throat of your machine. Tramp metal is stopped before it reaches the screw.",
 imgs=[("real-drawer-1.jpg","Stainless drawer magnet housing with pull-out bars",1400,1050),("real-drawer-2.jpg","Drawer magnet with magnetic bars pulled out",600,580),("grate-magnet-drawer-assembly-multi-row-bars.jpg","Multi-row drawer magnet assembly",1200,900)],
 kv=[("Fits","Feed throat of injection moulding, blow moulding and extrusion machines; hoppers"),("Construction","Stainless steel; mild steel on request"),("Finish","Polished or painted"),("Magnets","Ceramic 8 standard; rare-earth for difficult jobs"),("Bars","Waterproof magnetic bars, 3 to 9 per drawer in standard sizes"),("Field strength","Contact for spec (depends on ceramic vs rare-earth)")],
 tables=[("Standard CMdrawer sizes","Dimensions in mm. Other sizes and multi-row versions made to order.",["Part No.","Bars","A","B × C","D","E","F"],
   [["CMdrawer-100",3,265,"100×100",165,65,22],["CMdrawer-150",5,270,"150×150",216,70,45],["CMdrawer-200",7,275,"200×200",267,75,79],["CMdrawer-250",9,280,"250×250","317.5",80,100]])],
 faq=[("Why put a magnet on the feed throat?","Screws, nuts and broken metal in resin or regrind can damage the screw and barrel. A drawer magnet stops it at the last point before the machine."),
      ("Ceramic or rare-earth?","Ceramic suits general tramp metal. Choose rare-earth for fine iron or difficult materials. Tell us your material and we will advise."),
      ("Will it fit my machine?","Standard openings are 100 to 250 mm square. We can match your throat flange; send its dimensions or a photo."),
      ("How do I clean it?","Slide the drawer out and wipe the bars. Clean on a schedule set by how much metal you catch."),
      ("Is it only for plastics?","No. It also works under hoppers for food, powder and granular products."),
      ("Do you have prices online?","No. We give a written B2B quote by WhatsApp or email.")],
 related=["grate-magnet","magnetic-bar","bullet-magnet","magnetic-pulley"],
 industries=[("plastics-industry-magnets","Plastics"),("food-industry-magnets","Food plants"),("chemicals-industry-magnets","Chemicals & bulk")]))
# 4 Suspension
P.append(dict(slug="suspension-overband-magnet", name="Suspension / Overband Magnet", short="Overband magnets",
 title="Overband & Suspension Magnet Malaysia | Arrowmatics",
 desc="Overband (self-cleaning) and suspended plate magnets that pull tramp iron off conveyor belts. Quoted to your belt width and duty. WhatsApp quote.",
 h1="Overband and suspension magnets", eyebrow="Conveyors · Recycling · Aggregates",
 lead="Hung above the belt, the magnet lifts nails, bolts and tramp iron out of the burden before it reaches crushers, screens or the stockpile.",
 imgs=[("suspension-overband-magnet-yellow-frame-workshop.jpg","Overband suspension magnet with frame and belt",1200,900),("suspension-overband-magnet-self-cleaning-belt.jpg","Self-cleaning overband magnet seen along the belt",1200,900),("suspension-plate-magnet-yellow-four-eyebolts.jpg","Suspended plate magnet with four eyebolts",1200,900)],
 kv=[("Types","Overband (self-cleaning belt) and suspended plate (hand-cleaned)"),("Fits","Above conveyor belts, in-line or across the head pulley"),("Sizing","Belt width, speed, burden depth and hanging height"),("Field / reach","Contact for spec — calculated for your hanging height"),("Power","Overband needs a belt motor; plate types need none"),("Applications","Recycling, aggregates, quarry, wood, bulk handling")],
 tables=[],
 faq=[("Overband or suspended plate?","Overband types have a running belt that carries iron away continuously, so they suit heavier, constant loads. Plate types are cheaper and cleaned by hand, so they suit lighter loads."),
      ("What do you need to quote?","Belt width, belt speed, burden depth, the gap from magnet to burden, the material and the size of iron to remove. A photo of the conveyor helps."),
      ("How strong is it?","Reach matters more than surface gauss. We size the magnet for your hanging height and burden; ask for the specification."),
      ("Can I see it working?","Yes. Our separators page has a strength test video of a suspension magnet."),
      ("Do you supply the frame and chains?","Mounting is discussed at quotation. Tell us your structure and space."),
      ("Is a magnetic pulley better?","A head pulley magnet suits shallow burdens and ferrous splitting; an overband suits deeper burdens. See magnetic pulleys.")],
 related=["magnetic-pulley","grate-magnet","magnetic-bar","bullet-magnet"],
 industries=[("recycling-industry-magnets","Recycling & aggregates"),("chemicals-industry-magnets","Chemicals & bulk"),("food-industry-magnets","Food plants")],
 extra='<p style="font-size:0.85rem;color:var(--text-muted);">Some photos show the product type; size, field and drive are confirmed per application. See <a href="/magnetic-separators#suspension-magnets">photo credits and videos</a>.</p>'))
# 5 Pulley
P.append(dict(slug="magnetic-pulley", name="Magnetic Head Pulley", short="Magnetic pulleys",
 title="Magnetic Pulley Malaysia | Conveyor Head Pulley | Arrowmatics",
 desc="Magnetic head pulleys for belt conveyors, Ø50–160 mm, 300–1500 mm long, 8,000–19,500 gauss by size. Continuous tramp iron removal. WhatsApp quote.",
 h1="Magnetic head pulleys for conveyors", eyebrow="Belt conveyors · Continuous separation",
 lead="Replace the head pulley of a belt conveyor with a magnetic one. Non-magnetic product falls forward; iron is held on the belt and drops off underneath.",
 imgs=[("real-drum-1.jpg","Magnetic drum and pulley separator",600,580),("real-drum-2.jpg","Magnetic pulley shell",600,580)],
 kv=[("Fits","Head end of belt conveyors"),("Diameters","50 to 160 mm in the standard range; larger on request"),("Length","300 to 1500 mm"),("Field","8,000 to 19,500 gauss range depending on diameter (see table)"),("Materials handled","Chemicals, plastics, grains, food products, ceramics, coal"),("Sizing","Belt width, speed and tonnage")],
 tables=[("Standard CMpulley range","Diameter and length in mm. Gauss is the range offered for that diameter; confirm for your build.",["Part No.","Diameter","Length range","Gauss range"],
   [["CMpulley-50",50,"300–1500","8,000–12,000"],["CMpulley-75",75,"300–1500","8,000–12,000"],["CMpulley-80",80,"300–1500","8,500–13,000"],["CMpulley-85",85,"300–1500","8,500–13,500"],["CMpulley-100",100,"300–1500","12,000–18,000"],["CMpulley-120",120,"300–1500","12,000–18,500"],["CMpulley-150",150,"300–1500","13,000–19,000"],["CMpulley-160",160,"300–1500","13,000–19,500"]])],
 faq=[("How does a magnetic pulley work?","The pulley holds iron against the belt as it turns. Clean product leaves the belt in its normal path; the iron is carried underneath and drops into a separate chute."),
      ("Can it replace my existing pulley?","Usually yes, if the diameter, face width and shaft match. Send your conveyor drawing or measurements."),
      ("Which diameter?","It depends on belt width, speed and burden. The standard range is 50 to 160 mm; larger pulleys are quoted on request."),
      ("Pulley or overband?","Pulleys suit shallow, evenly spread burden. For deep burden or big tramp iron on top, use an overband magnet."),
      ("Is the gauss guaranteed?","The table shows the range per diameter. We confirm the field for your exact build at quotation."),
      ("Which industries use them?","Recycling, aggregates, food and grain, plastics, ceramics and coal handling.")],
 related=["suspension-overband-magnet","grate-magnet","drawer-magnet","magnetic-bar"],
 industries=[("recycling-industry-magnets","Recycling & aggregates"),("food-industry-magnets","Food plants"),("plastics-industry-magnets","Plastics")]))
# 6 Liquid trap
P.append(dict(slug="liquid-trap-magnet", name="Liquid Line Magnetic Trap", short="Liquid traps",
 title="Liquid Line Magnetic Trap Malaysia | Arrowmatics",
 desc="In-line magnetic traps for liquids, sauces, pastes and slurries. Flanged or threaded, 150–300 mm, 5–9 rare-earth bars. Stainless. WhatsApp quote.",
 h1="Liquid-line magnetic traps", eyebrow="Pipelines · Liquids · Slurries",
 lead="A stainless trap fitted into the pipeline. Rare-earth bars inside catch iron fines from liquids, sauces, pastes and slurries, and lift out for cleaning.",
 imgs=[("real-liquid-trap-1.jpg","Stainless liquid-line magnetic trap with swing-bolt lid",1200,900)],
 kv=[("Fits","Pipelines carrying liquids, sauces, pastes and slurries"),("Connection","Flanged or threaded ends"),("Magnets","High-energy rare-earth bars, 1 inch diameter, waterproof"),("Construction","304 stainless; 316 on request"),("Lid","Quick-release; screw nuts or band clamp"),("Options","Easy-clean type on request"),("Pressure / temperature rating","Contact for spec")],
 tables=[("Flange fitting (CMtrap-F)","Dimensions in mm.",["Part No.","A","B","C","D=E","Bars"],
   [["CMtrap-F-150",150,50,150,300,5],["CMtrap-F-200A",200,50,200,350,7],["CMtrap-F-200B",200,75,200,350,7],["CMtrap-F-250A",250,50,250,400,9],["CMtrap-F-250B",250,75,250,400,9],["CMtrap-F-250C",250,100,250,400,9],["CMtrap-F-300A",300,50,300,450,9],["CMtrap-F-300B",300,75,300,450,9],["CMtrap-F-300C",300,100,300,450,9]]),
  ("Threaded fitting (CMtrap-T)","Dimensions in mm.",["Part No.","A","B","D=E","Bars"],
   [["CMtrap-T-150",150,50,300,5],["CMtrap-T-200A",200,50,350,7],["CMtrap-T-200B",200,75,350,7],["CMtrap-T-250A",250,50,400,9],["CMtrap-T-250B",250,75,400,9],["CMtrap-T-250C",250,100,400,9],["CMtrap-T-300A",300,50,450,9],["CMtrap-T-300B",300,75,450,9],["CMtrap-T-300C",300,100,450,9]])],
 faq=[("What can a liquid trap handle?","Liquids, sauces, syrups, pastes and slurries moving in a pipe. Tell us the viscosity and temperature so we can size it."),
      ("Flange or thread?","Either. Match your existing pipework; we make both."),
      ("How is it cleaned?","Open the quick-release lid and slide each magnet assembly out, then wipe off the iron."),
      ("What pressure can it take?","It depends on size and lid type. Ask for the rating for your line before ordering."),
      ("Can it be 316 stainless?","Yes, 316 is available on request for corrosive products or heavy washdown."),
      ("How many bars do I need?","Standard traps carry 5, 7 or 9 bars depending on size. Finer contamination may need more contact; we advise per product.")],
 related=["magnetic-bar","bullet-magnet","grate-magnet","drawer-magnet"],
 industries=[("food-industry-magnets","Food plants"),("chemicals-industry-magnets","Chemicals"),("pharma-cosmetics-magnets","Pharma & cosmetics")]))
# 7 Bar
P.append(dict(slug="magnetic-bar", name="Magnetic Filter Bar", short="Magnetic bars",
 title="Magnetic Bar Malaysia | Magnetic Filter Rods | Arrowmatics",
 desc="Stainless magnetic filter bars, round or square, 100–1500 mm. Ceramic (3,000+ G) or rare-earth (12,000+ G) cores. Fully seal welded. WhatsApp quote.",
 h1="Magnetic filter bars and rods", eyebrow="Round · Square · Fully seal welded",
 lead="The building block of grate, drawer and liquid-trap separators — or install it on its own in any solid, powder or liquid flow to catch fine iron.",
 imgs=[("real-bars-1.jpg","Stainless magnetic filter bars",600,580),("grate-magnet-four-bar-units-and-single-bar.jpg","Magnetic bars as single bars and four-bar units",1200,900),("magnet-bar-support.jpg","Magnetic bar with support",1200,900)],
 kv=[("Round diameters","0.5\", 0.75\", 0.875\", 1\", 1.25\", 1.5\", 1.75\", 2\", 3\", 4\" (1\" most common)"),("Lengths","3\" to 60\" standard; table below in mm"),("Square bars","25×25 and 50×50 mm; others on request"),("Casing","SS304 or SS316 tube, well polished"),("Core / field","Ceramic 8: typical peak above 3,000 G; rare-earth: typical peak above 12,000 G; 1,500–12,000 G to order"),("Ends","Fully seal welded; plain or tapped ends"),("Delivery","Most standard sizes 1–2 working days (confirm stock)")],
 tables=[("Round bars, Ø25 mm (CMbar-R)","Length in mm. Other lengths on request.",["Part No.","Length","Part No.","Length"],
   [["CMbar-R-100",100,"CMbar-R-600",600],["CMbar-R-150",150,"CMbar-R-650",650],["CMbar-R-200",200,"CMbar-R-700",700],["CMbar-R-250",250,"CMbar-R-750",750],["CMbar-R-300",300,"CMbar-R-800",800],["CMbar-R-350",350,"CMbar-R-850",850],["CMbar-R-400",400,"CMbar-R-900",900],["CMbar-R-450",450,"CMbar-R-950",950],["CMbar-R-500",500,"CMbar-R-1000",1000],["CMbar-R-550",550,"CMbar-R-1500",1500]]),
  ("Square bars (CMbar-S)","-01 = 25×25 mm, -02 = 50×50 mm. Length in mm.",["Length","25×25 part","50×50 part"],
   [[L,f"CMbar-S-{L}-01",f"CMbar-S-{L}-02"] for L in (100,200,300,400,500,600,700,800,900,1000,1500)])],
 faq=[("What is a magnetic filter bar?","A sealed stainless tube packed with magnets. Material flowing past it leaves its iron on the surface."),
      ("Ceramic or rare-earth?","Ceramic bars give a typical peak above 3,000 gauss and suit coarse tramp iron. Rare-earth bars give a typical peak above 12,000 gauss for fine iron."),
      ("Can I build my own separator with your bars?","Yes. Many customers fit our bars into their own grates, hoppers and tanks. Tapped ends make mounting easy."),
      ("Are the bars waterproof?","Yes. They are fully seal welded, so they suit wet product and washdown."),
      ("How fast can I get them?","Most standard sizes can be delivered in 1–2 working days, subject to stock. Ask us when you order."),
      ("Can you make a special length?","Yes. Give us the diameter, length, end type and core type.")],
 related=["grate-magnet","drawer-magnet","liquid-trap-magnet","neodymium-magnets"],
 industries=[("food-industry-magnets","Food plants"),("pharma-cosmetics-magnets","Pharma & cosmetics"),("chemicals-industry-magnets","Chemicals")]))
# 8 Neodymium
P.append(dict(slug="neodymium-magnets", name="Neodymium Magnets", short="Neodymium magnets",
 title="Neodymium Magnet Malaysia | NdFeB N35–N52, H, SH, UH, EH",
 desc="Neodymium (NdFeB) magnets in Malaysia: grades N35–N52 and M, H, SH, UH, EH up to 200°C. Discs, blocks, rings or to drawing. WhatsApp quote.",
 h1="Neodymium magnets, made to your size", eyebrow="NdFeB · Discs · Blocks · Rings",
 lead="The strongest permanent magnets you can buy. Pick the grade for strength and working temperature; we supply the shape and coating you need.",
 imgs=[("real-ndfeb-1.jpg","Neodymium NdFeB magnets",1000,750),("ndfeb-blocks.jpg","Neodymium block magnets",1200,900),("real-ndfeb-2.jpg","Neodymium disc magnets",1000,750)],
 kv=[("Shapes","Cylinder, block, ring; other shapes to your drawing"),("Grades","N35–N52, M, H, SH, UH and EH series (table)"),("Max working temp","80 °C (N) up to 200 °C (EH)"),("Coating","Contact for spec"),("Tolerance","Contact for spec"),("More detail","See also NdFeB page and SmCo for higher temperatures")],
 tables=[("NdFeB grade properties","Typical values. Br remanence, Hcb coercivity, Hcj intrinsic coercivity, (BH)max energy product.",["Grade","Br (kGs)","Br (T)","Hcb (kOe)","Hcj (kOe)","(BH)max (MGOe)","Max temp (°C)"],
   [r for r in [
    ["N35","11.7–12.1","1.17–1.21","11.0–11.5","12","33–35",80],["N38","12.2–12.6","1.22–1.26","11.0–11.6","12","36–38",80],["N40","12.6–12.9","1.26–1.29","11.0–11.6","12","36–38",80],["N42","13.0–13.3","1.30–1.33","11.0–11.6","12","40–42",80],["N45","13.3–13.7","1.33–1.37","11.0–11.6","12","43–45",80],["N48","13.6–14.2","1.36–1.42","11.0–11.6","12","45–48",80],["N50","14.1–14.5","1.41–1.45","11.0–11.4","11","48–50",70],["N52","14.4–14.8","1.44–1.48","10.5–11.4","11","49.5–52",70],
    ["N35M","11.7–12.1","1.17–1.21","11.2–11.5","14","33–35",100],["N38M","12.2–12.6","1.22–1.26","11.4–11.7","14","36–38",100],["N42M","13.0–13.3","1.30–1.33","11.4–11.9","14","40–42",100],["N48M","13.7–14.3","1.37–1.43","11.4–12.0","14","45–48",100],
    ["N35H","11.7–12.1","1.17–1.21","10.8–11.4","17","33–35",120],["N40H","12.6–12.9","1.26–1.29","11.4–11.9","17","38–40",120],["N44H","13.0–13.6","1.33–1.36","11.4–11.9","16","42–44",120],
    ["N35SH","11.7–12.1","1.17–1.21","10.8–11.4","20","33–35",150],["N40SH","12.6–12.9","1.26–1.29","11.4–11.9","20","38–40",150],["N42SH","13.0–13.3","1.30–1.33","11.4–11.9","19","40–42",140],
    ["N30UH","10.8–11.2","1.08–1.12","10.1–10.6","25","28–30",180],["N35UH","11.7–12.1","1.17–1.21","10.8–11.4","25","33–35",180],
    ["N30EH","10.8–11.2","1.08–1.12","10.1–10.6","30","28–30",200],["N35EH","11.7–12.1","1.17–1.21","10.8–11.4","30","33–35",200]]])],
 faq=[("Is neodymium the same as NdFeB?","Yes. NdFeB (neodymium-iron-boron) is the material; people search for it as neodymium or rare-earth magnets."),
      ("Which grade should I choose?","Higher numbers are stronger. The letter sets the temperature: N up to 80 °C, M 100 °C, H 120 °C, SH 150 °C, UH 180 °C, EH 200 °C."),
      ("Above 200 °C?","Use SmCo (samarium cobalt). See our SmCo page."),
      ("Can you make a custom size?","Yes. Send a drawing or the dimensions, grade, coating and quantity."),
      ("What coating do you use?","Coating depends on the job. Tell us the environment and we will confirm the coating at quotation."),
      ("Are they safe to handle?","Large neodymium magnets snap together hard and can pinch fingers or crack. Handle with care and keep them away from pacemakers and electronics.")],
 related=["magnetic-bar","grate-magnet","bullet-magnet","drawer-magnet"],
 industries=[("industries","All industries"),("plastics-industry-magnets","Plastics"),("food-industry-magnets","Food plants")],
 extra='<p>Also see the <a href="/ndfeb-magnets">NdFeB magnets overview</a> and <a href="/smco-magnets">SmCo magnets</a> for high-temperature work.</p>'))

NAMES = {p["slug"]: p["short"] for p in P}

def ld(o): return '  <script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + "\n  </script>\n"

def build(p):
    url = f"{BASE}{p['slug']}"
    img0 = p["imgs"][0]
    # No published prices or real reviews, so no schema.org Product (Google flags a Product
    # without offers/review/aggregateRating as an invalid item). Describe the page instead.
    imgs = [BASE+"images/"+i[0] for i in p["imgs"]]
    product = {"@context":"https://schema.org","@type":"ItemPage","name":p["name"],"url":url,"description":p["desc"],
       "inLanguage":"en-MY","primaryImageOfPage":{"@type":"ImageObject","url":imgs[0]},"image":imgs,
       "about":{"@type":"Thing","name":p["name"]},
       "isPartOf":{"@type":"WebSite","name":"Arrowmatics Magnets","url":"https://magnets.com.my/"},"publisher":PROVIDER}
    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
       {"@type":"ListItem","position":1,"name":"Home","item":BASE},
       {"@type":"ListItem","position":2,"name":"Magnetic Separators" if p["slug"]!="neodymium-magnets" else "Magnets","item":BASE+("magnetic-separators" if p["slug"]!="neodymium-magnets" else "ndfeb-magnets")},
       {"@type":"ListItem","position":3,"name":p["name"],"item":url}]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]}
    e = html.escape
    gallery = "".join(f'<figure><img src="images/{f}" alt="{e(a)}" loading="lazy" decoding="async" width="{w}" height="{h}"><figcaption>{e(a)}</figcaption></figure>' for f,a,w,h in p["imgs"][1:])
    tbls = "".join(f'<h3 style="margin-top:1.5rem;">{e(t)}</h3><p style="font-size:0.9rem;color:var(--text-muted);">{e(n)}</p>{table(hd,rows)}' for t,n,hd,rows in p["tables"])
    if not p["tables"]:
        tbls = '<p><strong>Dimensions and field strength: contact for spec.</strong> Each unit is calculated for your conveyor, so we do not publish a fixed size table.</p>'
    faqs = "".join(f'<details class="acc"><summary><h3>{e(q)}</h3></summary><div class="rm-body"><p>{e(a)}</p></div></details>' for q,a in p["faq"])
    rel = " · ".join(f'<a href="/{s}">{e(NAMES[s])}</a>' for s in p["related"])
    ind = " · ".join(f'<a href="/{s}">{e(n)}</a>' for s,n in p["industries"])
    quote = QUOTE.replace('pq-', p['slug'][:4]+'-q-').replace('data-context="plate-magnets"', f'data-context="{p["slug"]}"').replace('data-context="checklist-plate-magnets"', f'data-context="checklist-{p["slug"]}"').replace('pqc-', p['slug'][:4]+'-c-')
    wa_text = f"Hi%20Arrowmatics%20Magnets%20%E2%80%94%20I%20need%20a%20quote%20for%20a%20{p['name'].replace(' ','%20').replace('/','%2F')}."
    crumb_mid = ('<a href="/magnetic-separators">Separators</a>' if p["slug"]!="neodymium-magnets" else '<a href="/ndfeb-magnets">NdFeB</a>')
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Google tag (gtag.js) - Google Ads conversion measurement -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-1067610456"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','AW-1067610456');</script>
  <title>{e(p["title"])}</title>
  <meta name="description" content="{e(p["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{e(p["title"])}">
  <meta property="og:description" content="{e(p["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="product">
  <meta property="og:image" content="{BASE}images/{img0[0]}">
  <meta property="og:site_name" content="Arrowmatics Magnets">
  <meta property="og:locale" content="en_MY">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="css/styles.css?v=mk4">
{ld(product)}{ld(crumbs)}{ld(faq)}  <link rel="icon" type="image/png" href="images/favicon.png">
  <link rel="describedby" href="/llms.txt">
  <link rel="alternate" type="text/markdown" href="/{p["slug"]}.md">
</head>
<body>
{HEADER}
  <section class="ph">
    <div class="container ph-grid">
      <div class="ph-copy">
        <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · {crumb_mid} · <span>{e(p["short"])}</span></nav>
        <span class="hero-eyebrow">{e(p["eyebrow"])}</span>
        <h1>{e(p["h1"])}</h1>
        <p class="ph-lead">{e(p["lead"])}</p>
        <div class="ph-actions">
          <a class="btn btn-wa" href="https://wa.me/60122112522?text={wa_text}" target="_blank" rel="noopener">WhatsApp {WA}</a>
          <button type="button" class="btn btn-expert-hero" data-open-magnet-expert>Ask the Magnet Expert</button>
        </div>
      </div>
      <figure class="ph-photo">
        <img src="/images/{img0[0]}" alt="{e(img0[1])}" width="{img0[2]}" height="{img0[3]}" fetchpriority="high" decoding="async">
        <figcaption>{e(img0[1])}</figcaption>
      </figure>
    </div>
  </section>

  <main>
    <section class="section section-alt" id="specs">
      <div class="container">
        <div class="section-head"><span class="section-index">01 / Specification</span><h2>{e(p["short"])} at a glance</h2></div>
        {kv(p["kv"])}
        {tbls}
        <p style="font-size:0.85rem;color:var(--text-muted);margin-top:1rem;">Standard sizes are from our catalogue. Final size, field strength and stainless grade are confirmed in writing at quotation. Anything marked "contact for spec" depends on your application.</p>
        {p.get("extra","")}
      </div>
    </section>

    <section class="section" id="photos">
      <div class="container">
        <div class="section-head"><span class="section-index">02 / Photos</span><h2>Our {e(p["short"].lower())}</h2></div>
        <div class="photo-grid">{gallery}</div>
      </div>
    </section>

    <section class="section section-alt" id="where">
      <div class="container">
        <div class="section-head"><span class="section-index">03 / Where it fits</span><h2>Industries and related separators</h2></div>
        <p><strong>Industries:</strong> {ind}</p>
        <p><strong>Related products:</strong> {rel} · <a href="/plate-magnets">Plate magnets</a> · <a href="/magnetic-separators">All separators</a></p>
        <p>Not sure which type? Read <a href="/guide-which-magnetic-separator">Which magnetic separator do I need?</a> or <a href="/guide-what-to-send-for-a-magnet-quote">what to send for a quote</a>.</p>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="container" style="max-width:800px;">
        <div class="section-head"><span class="section-index">04 / FAQ</span><h2>{e(p["short"])}: common questions</h2></div>
        {faqs}
        <p style="margin-top:1.5rem;"><a href="/faq">More questions on the main FAQ →</a></p>
      </div>
    </section>

{quote}
    <section class="cta-band">
      <div class="container">
        <h2>Get a {e(p["short"].lower()[:-1] if p["short"].endswith("s") else p["short"].lower())} quote</h2>
        <p>Send the size, product, where it fits and quantity. A photo or sketch helps. Written B2B quote, no online prices.</p>
        <div class="hero-actions">
          <a class="btn btn-wa" href="https://wa.me/60122112522?text={wa_text}" target="_blank" rel="noopener">WhatsApp {WA}</a>
          <a class="btn btn-outline" href="mailto:arrowmatics@gmail.com?subject={p['name'].replace(' ','%20').replace('/','%2F')}%20enquiry">Email arrowmatics@gmail.com</a>
        </div>
      </div>
    </section>
  </main>

{FOOTER}'''
    (ROOT / f"{p['slug']}.html").write_text(out)
    md = [f"# {p['h1']}", "", p["lead"], "", "## Specification", ""] + [f"- **{k}:** {v}" for k,v in p["kv"]]
    for t,n,hd,rows in p["tables"]:
        md += ["", f"### {t}", "", n, "", "| " + " | ".join(hd) + " |", "|" + "---|"*len(hd)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    md += ["", "## FAQ", ""] + [f"**{q}** {a}" for q,a in p["faq"]] + ["", f"Quote: WhatsApp {WA} · {url}"]
    (ROOT / f"{p['slug']}.md").write_text("\n".join(md) + "\n")

for p in P: build(p)
print("built", [p["slug"] for p in P])
