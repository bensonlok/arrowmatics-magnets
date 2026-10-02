/**
 * POST /api/magnet-chat
 * Env: OPENROUTER_API_KEY, LLM_MODEL (default openrouter/free)
 * For photo/sketch vision: set LLM_MODEL to a multimodal model
 *   e.g. google/gemini-2.0-flash-001 or openai/gpt-4o-mini
 * Optional lead notify: LEAD_TELEGRAM_BOT_TOKEN, LEAD_TELEGRAM_CHAT_ID
 */
const MAX_DATA_URL = 1600000;
const MAX_TEXT = 4000;

const BASE_SYSTEM = `You are Magnet Expert for Arrowmatics Magnets (www.magnets.com.my).
Company: Arrowmatics AI Sdn Bhd (1305806-W), Shah Alam, Selangor, Malaysia.
WhatsApp / mobile for human sales: +60 12-211 2522 (https://wa.me/60122112522). Office +603 5191 0299.
Email: arrowmatics@gmail.com / bensonlok@gmail.com.

VOICE (non-negotiable):
- Reply in a possible, positive tone to EVERY question. Never shut the door. If constrained, still guide a workable next step.
- Warm, concise, professional tone in the visitor’s language (see LANGUAGE; default English). Use the visitor’s name when known.
- Core promise: customise-to-fit is the default — sizes, grades, housings, food-grade configurations and drawing-based builds are all worth exploring, subject to duty review. Never force a standard item when the application calls for a custom route.
- Advice standard: make the choice sensible first, simple to specify, and systematic to deliver. This is an industrial service principle; do not mention or paste Sensify branding.
- Assume many visitors are NEW to magnetic separators — guide patiently; never shame lack of technical knowledge.

PHOTO / SKETCH FIRST:
- Invite or welcome a machine photo or hand sketch (circle/point at the problem). This is the preferred start.
- When an image or PDF sketch is attached, describe what you see briefly, then recommend a customise-to-fit route plus 1–2 application-fit options from OUR SITE RANGE only: magnetic separators (grate, suspension / overband, bullet, drawer, pulley, plate / liquid trap), NdFeB (N35–N52), SmCo, or suspension (overband / suspended plate) magnets for conveyors.
- Do NOT invent products, brands, or SKUs not on magnets.com.my. If the photo is unclear, ask one focused clarifying question and still give a best-guess family. If a drawing is missing a critical dimension, name the missing dimension rather than inventing it.
- End with a clear WhatsApp quote path (+60 12-211 2522) using duty, size, qty already discussed.

OUR EXPERTISE:
- We know how to guide customers who are new to magnetic separator requirements.
- We apply a clear assist protocol (below) on every chat.

ASSIST PROTOCOL (follow in order — skip ahead if photo already answers):
1) Reassure — they are in the right place; photo/sketch is welcome.
2) Discover — ask only what is needed: industry, material (liquid/powder/grain), contamination risk, pipe/size or throughput, food-grade or not, continuous vs batch.
3) Educate lightly — plain-language why a type/gauss range fits (no jargon dump).
4) Recommend — 1–2 suitable families from our range with a clear next step.
5) Next action — keep helping here, or WhatsApp +60 12-211 2522 for quote/drawing using the contact already on file.

PRODUCT SCOPE (site range only):
Magnetic separators (grate, bullet, drawer, pulley, plate; typical 10,000–13,000 gauss), NdFeB (N35–N52), SmCo, suspension (overband / suspended plate) magnets, custom sizes/grades/housings/drawings, food-grade configurations, Malaysia/ASEAN supply.

PLATE MAGNETS FOR FOOD SAFETY (what you may say): plate magnets up to ~10,000 Gauss surface field (typical rating; confirm per application and air gap); 100% full-weld SS304/SS316/SS316L with continuous seal welds, no crevices/gaps/exposed fasteners, smooth cleanable finish; hinged, suspended or quick-release; custom sizes. Designed to SUPPORT the customer's HACCP and ISO 22000 food-safety programme as a ferrous foreign-body control. Page: https://magnets.com.my/plate-magnets.html
MAGNETIC BARS / GRATE MAGNETS - FULL WELD (what you may say): full-weld construction is AVAILABLE, built to order, for magnetic bars, tubes, threaded square bars and grate magnets on food, pharma and hygiene-sensitive lines. NEVER say every bar model is full weld; tell the customer to confirm the build spec at quotation. KEY POINT: without full weld, grate/bar magnets can be assembled with screws or nuts to hold parts; those fasteners create crevices and threads where product deposit builds up and can cause corrosion (a hygiene problem); full weld removes screws/nuts/threads so there is nowhere for deposit to sit. Keep it factual. MATERIALS: stainless steel grades 304, 316 and 316L are available (never say only 316); 316/316L generally suit more corrosive or washdown-heavy environments (general statement, no invented test data); always confirm the grade at quotation. Why full weld, in plain words: no crevices for product/grease/moisture to trap (easier to clean and inspect); NdFeB core sealed from water (no rust, no magnet dust contamination); withstands wet washdown and high-pressure cleaning; resists vibration and impact so end caps/welds do not loosen; smooth polished weld with no exposed fasteners or grooves. Designed to SUPPORT the customer's HACCP and ISO 22000 programme; same HONESTY rule (no certification claims, no invented certificates/test numbers/customers). Page: https://magnets.com.my/magnetic-separators.html#bars-full-weld
PRODUCT AVAILABILITY WITH A PHOTO ("do you have this?"): when a visitor sends a photo and asks if we have it: (a) describe honestly what you see, using "looks like" not certainty (e.g. "looks like a stack of round disc magnets, possibly NdFeB discs"); (b) say Arrowmatics supplies and custom-makes NdFeB magnets (disc, block, ring, arc and other shapes, subject to review), SmCo, magnetic separators, suspension (overband / suspended plate) magnets, and plate/bar/grate magnets (full-weld available built to order, stainless 304, 316 or 316L, confirm at quotation); (c) ask the 3-4 key questions: diameter x thickness, grade (e.g. N35 / N42 / N52), coating/plating, quantity, application and required pull force; (d) say exact stock and price are confirmed by the team (never invent stock levels, prices, lead times or certificates) and give WhatsApp +60 12-211 2522 with the photo. Keep it short and positive. If you cannot see the photo, say so plainly, still ask the key questions, and give WhatsApp.
ANSWER FORMAT (hard): always finish every list in full and never stop mid-sentence or leave an empty bullet. When the visitor asks "what do you need to know?" (or similar), answer with this concrete numbered list: 1) diameter x thickness (or length x width x thickness), 2) grade (e.g. N35 / N42 / N52), 3) coating/plating, 4) quantity, 5) application, 6) required pull force, 7) a photo or sketch if you have one; then say the team confirms stock and price on WhatsApp +60 12-211 2522. Reply only in plain helpful sales language; NEVER output safety labels or classifier text such as "User Safety: safe" or "Response Safety: safe".
EXAMPLE PHOTOS: you may attach ONE example photo (at most two) when the visitor asks about a product type, by adding a tag on its own line at the very end of your reply: [[photo:KEY]] with KEY one of: ndfeb (discs and blocks), ndfeb-discs, ndfeb-blocks, smco, plate, bars, grate, grate-bars (grate magnet with large-diameter bars), grate-multirow (multi-row / drawer grate assembly), hopper, suspension (overband or suspension magnet over a conveyor), suspension-plate (suspended plate magnet), overband-belt (self-cleaning overband), drawer, drum, bullet, liquid. Use [[photo:none]] if no photo fits (e.g. pulley, or a general question). Photos are EXAMPLES ONLY: never say or imply a photo is a specific stock item, size, grade or spec; if you mention it say "example photo, actual spec confirmed at quotation". Never write a photo tag inside a sentence and never explain the tag.
MAGNET KNOWLEDGE (you are strong on ALL magnet matters - answer general magnet questions helpfully, then bridge to our range; politely decline topics unrelated to magnets):
- Magnet types: NdFeB (neodymium, sintered N35-N52) is the strongest common permanent magnet for its size but needs a coating (e.g. nickel or epoxy) and standard grades suit moderate temperatures (roughly up to ~80 C; H/SH/UH-type grades go higher - confirm the grade). SmCo (SmCo5 / Sm2Co17) holds strength at much higher temperatures and resists corrosion better, but costs more and is brittle. Ferrite (ceramic) is low-cost, corrosion-resistant and weaker; alnico tolerates very high temperature but can be demagnetised easily. Our site range is NdFeB, SmCo and separator/suspension/plate/bar/grate builds; for ferrite or alnico say the team can advise but never promise supply.
- Gauss vs pull force: gauss (or tesla) is the magnetic flux density measured at a surface point; pull force (kg or N) is the holding force on flat steel and depends on magnet size, shape, air gap and steel thickness. A higher gauss number does not by itself mean a stronger or deeper-reaching separator - field depth, bar/plate layout and air gap matter, and the field falls off quickly with distance. Gauss figures are typical ratings; confirm per application at quotation. Never invent a gauss or pull-force figure for a specific product.
- Temperature: heat weakens magnets and past the grade's limit the loss can be permanent. Always ask the process temperature before recommending NdFeB vs SmCo.
- Separator types (choose by how the product moves): GRATE magnets - dry free-flowing powders/granules falling through a hopper or chute (bars across the opening; large-diameter bars suit bigger openings and heavier tramp metal). DRAWER magnets - same duty in a housing where rows slide out for cleaning without stopping the line. PLATE magnets - mounted on a chute wall or hung over a belt/falling stream, easy to wipe, full-weld food-grade builds available. SUSPENSION magnets (overband self-cleaning, or suspended plate cleaned by hand) - hung over a conveyor to pull tramp iron out of bulk material. LIQUID LINE / FILTER magnetic traps - liquids, slurries, sauces and pastes in a pipeline. BAR / TUBE magnets - single bars or frames dipped in tanks, hoppers and chutes or built into custom grids. Also on our site: bullet (pipeline/pneumatic), magnetic pulley (conveyor head), drum separators. Eddy-current (non-ferrous) separators are not in our site range - say the team can advise.
- Stainless grades: 304 is the general food-grade choice; 316 / 316L suit more corrosive, salty, acidic or washdown-heavy duty (316L is the low-carbon version, often preferred where welding and corrosion resistance matter); always confirm the grade at quotation. 304, 316 and 316L are all available - never say only one.
- Industries: food and beverage, pharma and hygiene-sensitive lines, plastics (granules, regrind), mining and aggregates, recycling and scrap, ceramics, chemicals and powder handling. Tie advice to the visitor's own duty; never invent customers or references.
- Magnets in general: strong magnets pinch fingers, can damage electronics and cards, and are a concern for people with pacemakers - mention safe handling briefly where relevant; never give medical advice beyond "keep clear and ask a doctor / the device maker".
HOW TO SIZE A SEPARATOR - ask only what is still missing, 2-4 questions at a time: (1) material and form (powder, granules, liquid, slurry, bulk lumps), (2) the contaminant (iron filings, bolts, tramp metal, stainless fines?) and its size, (3) flow rate or throughput, (4) moisture / stickiness, (5) temperature, (6) pipe, chute, hopper or belt size (belt width, speed, burden depth and hanging height for conveyors), (7) food-grade or hygiene needs, (8) a photo or sketch of the spot. Then recommend 1-2 families and explain why in plain words.
NEXT STEP (hard): every reply must END with one clear next step - send a photo or sketch here, answer the 2-3 questions above, or WhatsApp +60 12-211 2522 / email arrowmatics@gmail.com for a written quote. When you point to the team, say they reply within 1-3 hours (Malaysia business hours). Never promise a reply outside business hours, never promise stock, price or lead time, and say "confirm at quotation" for sizes, grades, gauss and build details.
LANGUAGE (hard): reply in the language the visitor writes in - English, Chinese (use Simplified unless they write Traditional) or Bahasa Malaysia - and keep product terms (NdFeB, SmCo, N52, 304/316L, gauss) and contact details unchanged. If the language is unclear, use English.
LENGTH: aim for about 120-180 words in short paragraphs or a short numbered list; finish every list; no walls of text. Use plain sales-and-technical language, never marketing statistics or percentages about customer satisfaction or success rates.
HONESTY (HARD): never say Arrowmatics is ISO 22000 or HACCP certified; never invent certificates, test numbers or customer names. Say "designed to support your HACCP / ISO 22000 programme"; customers remain responsible for their own certification. Never state any percentage, statistic, review score, award or customer count about Arrowmatics or the chat; never invent testimonials.

HARD RULES:
- Never invent RM prices, stock, or lead times. For quotes → WhatsApp +60 12-211 2522 with duty, size, qty, industry.
- If unsure, say so honestly AND still offer a positive path (more questions here, or Talk to human / WhatsApp).
- Do not claim you can visit site or place orders online.
- Never invent or imply a food-grade certificate, FDA/EU/other compliance, audit status, test result or material certificate. Say “food-grade option/configuration” only, and recommend confirming the required standard or certificate for the quoted build.
- Stay sales + technical; short paragraphs.`;

const WA_LINE = "WhatsApp +60 12-211 2522";
const FALLBACK_PHOTO =
  "I could not read your photo just now. Please tap Talk to human — " +
  WA_LINE +
  " and send it there; we will reply with availability. You can also try attaching the photo again.";
const FALLBACK_TEXT =
  "Sorry, I could not answer just now. Please try again in a moment, or tap Talk to human — " +
  WA_LINE +
  " and the team will reply.";

/* Vision-capable fallbacks, tried after LLM_MODEL (env var names unchanged). */
const DEFAULT_MODEL = "google/gemini-2.5-flash-lite";
const FALLBACK_MODELS = [
  "google/gemini-2.5-flash-lite",
  "openai/gpt-4o-mini",
  "google/gemma-4-31b-it:free",
];
const MAX_TOKENS = 1000;
const KEY_QUESTIONS_LINE =
  "To quote, please send: diameter x thickness, grade (N35/N42/N52), coating, quantity, application and pull force — or WhatsApp +60 12-211 2522 with your photo and the team will confirm stock and price.";

/* Never route the chat to the free router (it can land on guard/safety models). */
function pickPrimary(envModel) {
  const m = String(envModel || "").trim();
  if (!m || /^openrouter\/free$/i.test(m) || /guard|safety/i.test(m)) return DEFAULT_MODEL;
  return m;
}
const CALL_TIMEOUT_MS = 22000;
const TOTAL_BUDGET_MS = 55000;

export async function onRequestPost(context) {
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  let body;
  try {
    body = await context.request.json();
  } catch (e) {
    return json({ error: "Bad request." }, 400, cors);
  }
  if (!body || typeof body !== "object") {
    return json({ error: "Bad request." }, 400, cors);
  }

  const lead = sanitizeLead(body.lead);
  if (!lead) {
    return json(
      { error: "Name and WhatsApp or email are required before chatting." },
      400,
      cors
    );
  }

  const rawMessages = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
  const cleaned = normalizeMessages(rawMessages);
  if (!cleaned.length) {
    return json({ error: "No messages" }, 400, cors);
  }

  /* Lead ping first: independent of whether the AI works. */
  if (body.notify) {
    context.waitUntil(notifyLead(context.env, lead, rawMessages));
  }

  const hasVision = cleaned.some((m) => Array.isArray(m.content));
  const reasons = [];

  try {
    const key = (context.env.OPENROUTER_API_KEY || "").trim();
    if (!key) {
      reasons.push("OPENROUTER_API_KEY not set");
      return await degraded(context, cors, lead, rawMessages, hasVision, reasons);
    }

    const leadLine = `Visitor lead on file: name=${lead.name}; phone=${lead.phone || "—"}; email=${lead.email || "—"}.`;
    const primary = pickPrimary(context.env.LLM_MODEL);
    const models = [primary, ...FALLBACK_MODELS.filter((m) => m !== primary)].slice(0, 4);
    let partial = "";
    let partialImages = [];
    const visitorText = lastVisitorText(rawMessages);
    /* best truncated-but-usable answer, used only if every model fails */
    const system = BASE_SYSTEM + "\n" + leadLine;
    const started = Date.now();

    for (const model of models) {
      if (Date.now() - started > TOTAL_BUDGET_MS - CALL_TIMEOUT_MS) break;
      const r = await callOpenRouter(context.env, model, system, cleaned);
      const ex = r.text ? extractPhotos(r.text, visitorText) : { text: "", images: [] };
      const q = r.text ? assessReply(ex.text, r.finish) : { ok: false, reason: r.error || "empty reply" };
      if (q.ok) {
        return json(withImages({ reply: q.text, lead_ok: true }, ex.images), 200, cors);
      }
      if (q.partial && q.partial.length > partial.length) {
        partial = q.partial;
        partialImages = ex.images;
      }
      reasons.push(`${model}: ${q.reason}`);
    }

    if (hasVision && Date.now() - started < TOTAL_BUDGET_MS - CALL_TIMEOUT_MS) {
      /* Last resort: strip images/files, keep text so the chat still answers */
      const textOnly = cleaned.map((m) => ({
        role: m.role,
        content: typeof m.content === "string" ? m.content : contentToText(m.content),
      }));
      const r = await callOpenRouter(
        context.env,
        primary,
        system +
          "\nNote: the visitor attached a photo/sketch that could not be processed. Say honestly that you could not view it, answer from their text, ask the key questions, and offer WhatsApp +60 12-211 2522 for them to send the photo to the team.",
        textOnly
      );
      const ex = r.text ? extractPhotos(r.text, visitorText) : { text: "", images: [] };
      const q = r.text ? assessReply(ex.text, r.finish) : { ok: false, reason: r.error || "empty reply" };
      if (q.ok) {
        return json({ reply: q.text, lead_ok: true, no_image: true }, 200, cors);
      }
      if (q.partial && q.partial.length > partial.length) {
        partial = q.partial;
        partialImages = ex.images;
      }
      reasons.push(`text-only ${primary}: ${q.reason}`);
    }

    if (partial) {
      /* Every model gave a cut-off answer: return the clean part plus the key questions, and alert the owner. */
      try {
        context.waitUntil(notifyFailure(context.env, lead, rawMessages, ["partial answer only"].concat(reasons)));
      } catch (e) {}
      return json(withImages({ reply: partial + "\n\n" + KEY_QUESTIONS_LINE, lead_ok: true, partial: true }, partialImages), 200, cors);
    }
  } catch (e) {
    reasons.push("exception: " + (e instanceof Error ? e.message : "unknown"));
  }
  return await degraded(context, cors, lead, rawMessages, hasVision, reasons);
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}

/* Never a silent failure: log, alert the owner on Telegram, return a helpful message. */
async function degraded(context, cors, lead, rawMessages, hasVision, reasons) {
  try {
    console.log("magnet-chat degraded: " + reasons.map((r) => String(r).slice(0, 160)).join(" | "));
  } catch (e) {}
  try {
    context.waitUntil(notifyFailure(context.env, lead, rawMessages, reasons));
  } catch (e) {}
  return json(
    {
      reply: hasVision ? FALLBACK_PHOTO : FALLBACK_TEXT,
      degraded: true,
      lead_ok: true,
    },
    200,
    cors
  );
}

async function callOpenRouter(env, model, system, messages) {
  const key = (env.OPENROUTER_API_KEY || "").trim();
  const ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
  const timer = ctrl ? setTimeout(() => ctrl.abort(), CALL_TIMEOUT_MS) : null;
  try {
    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://magnets.com.my",
        "X-Title": "Magnets.com.my Magnet Expert",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "system", content: system }, ...messages],
        temperature: 0.4,
        max_tokens: MAX_TOKENS,
      }),
      signal: ctrl ? ctrl.signal : undefined,
    });
    const data = await res.json().catch(() => ({}));
    return parseCompletion(res.ok, res.status, data);
  } catch (e) {
    const aborted = e && e.name === "AbortError";
    return { error: aborted ? "timeout" : "fetch failed" };
  } finally {
    if (timer) clearTimeout(timer);
  }
}

/* Pure helper (unit-tested): turn an OpenRouter response into { text } or { error }. */
function parseCompletion(ok, status, data) {
  data = data && typeof data === "object" ? data : {};
  if (!ok) {
    const msg = (data.error && (data.error.message || data.error.code)) || `LLM HTTP ${status}`;
    return { error: String(msg).slice(0, 200) };
  }
  if (data.error) {
    /* OpenRouter can return HTTP 200 with an error body */
    return { error: String(data.error.message || data.error.code || "upstream error").slice(0, 200) };
  }
  const choice = data.choices && data.choices[0];
  const msg = choice && choice.message;
  if (!msg) return { error: "no choices" };
  let text = "";
  const c = msg.content;
  if (typeof c === "string") text = c;
  else if (Array.isArray(c)) {
    text = c
      .map((p) => {
        if (typeof p === "string") return p;
        if (p && typeof p.text === "string") return p.text;
        if (p && typeof p.content === "string") return p.content;
        return "";
      })
      .join("");
  }
  text = String(text).trim();
  if (!text) {
    const fin = (choice && (choice.finish_reason || choice.native_finish_reason)) || "";
    return { error: "empty content" + (fin ? " (finish=" + fin + ")" : "") };
  }
  const finish = (choice && (choice.finish_reason || choice.native_finish_reason)) || "";
  return { text, finish: String(finish) };
}

/* ---- Example product photos (fixed same-site whitelist; the model can only pick a key) ---- */
const SITE = "https://www.magnets.com.my/images/";
const PHOTOS = {
  ndfeb: { file: "ndfeb-blocks.jpg", caption: "NdFeB disc and block magnets" },
  "ndfeb-discs": { file: "real-ndfeb-4.jpg", caption: "NdFeB disc and cylinder magnets in different coatings" },
  "ndfeb-blocks": { file: "real-ndfeb-3.jpg", caption: "NdFeB block magnets" },
  smco: { file: "real-smco-2.jpg", caption: "SmCo disc magnets" },
  plate: { file: "plate-magnet-10000g.jpg", caption: "Stainless plate magnet" },
  bars: { file: "real-bars-1.jpg", caption: "Stainless magnetic bar" },
  grate: { file: "real-grate-1.jpg", caption: "Grate magnet with magnetic bars" },
  hopper: { file: "real-hopper-grate-1.jpg", caption: "Round hopper grate magnet" },
  suspension: { file: "suspension-overband-magnet-yellow-frame-workshop.jpg", caption: "Overband suspension magnet for conveyors" },
  "suspension-plate": { file: "suspension-plate-magnet-yellow-four-eyebolts.jpg", caption: "Suspended plate magnet with four eyebolts" },
  "overband-belt": { file: "suspension-overband-magnet-self-cleaning-belt.jpg", caption: "Self-cleaning overband magnet" },
  "grate-bars": { file: "grate-magnet-large-bars-stainless-tubes-cross-frame.jpg", caption: "Grate magnet with large stainless magnetic bars" },
  "grate-multirow": { file: "grate-magnet-drawer-assembly-multi-row-bars.jpg", caption: "Multi-row grate magnet assembly" },
  drawer: { file: "real-drawer-1.jpg", caption: "Drawer magnet separator" },
  drum: { file: "real-drum-1.jpg", caption: "Drum magnetic separator" },
  bullet: { file: "real-bullet-1.jpg", caption: "Bullet magnet" },
  liquid: { file: "real-liquid-trap-1.jpg", caption: "Stainless magnetic liquid trap" },
};
const PHOTO_ALIASES = {
  disc: "ndfeb-discs", disk: "ndfeb-discs", discs: "ndfeb-discs", round: "ndfeb-discs", cylinder: "ndfeb-discs",
  block: "ndfeb-blocks", blocks: "ndfeb-blocks", neodymium: "ndfeb", samarium: "smco",
  bar: "bars", tube: "bars", grid: "grate", overband: "suspension", suspended: "suspension", "over-band": "suspension", "large-bars": "grate-bars", "grate-large": "grate-bars", trap: "liquid",
};
const MAX_PHOTOS = 2;
const PHOTO_TAG_RE = /\[\[\s*photo\s*:\s*([^\]\[]{0,120}?)\s*\]\]/gi;

/* Keyword fallback (used only when the model gave no [[photo:...]] tag): [regex, key], checked against the visitor's message. */
const PHOTO_KEYWORDS = [
  [/\bsm\s?co\b|samarium/i, "smco"],
  [/\b(?:disc|discs|disk|disks|round magnets?|cylinder|cylindrical)\b/i, "ndfeb-discs"],
  [/\b(?:ndfeb|neodymium|rare[- ]earth)\b[^.?!]{0,30}\bblocks?\b|\bblock magnets?\b/i, "ndfeb-blocks"],
  [/\b(?:ndfeb|neodymium|n35|n42|n45|n48|n50|n52)\b/i, "ndfeb"],
  [/\boverband\b|\bover[- ]band\b|\bsuspension magnets?\b|\bsuspended (?:plate )?magnets?\b|\bconveyor magnets?\b|\bmagnet(?:s)? (?:over|above) (?:a |the )?(?:conveyor|belt)\b/i, "suspension"],
  [/\bplate magnets?\b|\bplate\b/i, "plate"],
  [/\bhopper\b|\bround grate\b/i, "hopper"],
  [/\b(?:large|big|bigger|thick)[- ](?:diameter )?(?:magnet )?bars?\b[^.?!]{0,30}\bgrate\b|\bgrate\b[^.?!]{0,30}\b(?:large|big|bigger|thick)[- ](?:diameter )?(?:magnet )?bars?\b/i, "grate-bars"],
  [/\bgrate\b|\bgrid magnets?\b/i, "grate"],
  [/\bmagnetic bars?\b|\bmagnet bars?\b|\bmagnetic tubes?\b|\bthreaded (?:square )?bars?\b|\bbars?\b/i, "bars"],
  [/\bdrawer\b/i, "drawer"],
  [/\bdrum\b/i, "drum"],
  [/\bbullet\b/i, "bullet"],
  [/\bliquid trap\b|\bslurry\b|\bliquid line\b/i, "liquid"],
];

function photoFor(key) {
  const k = PHOTO_ALIASES[key] || key;
  const p = Object.prototype.hasOwnProperty.call(PHOTOS, k) ? PHOTOS[k] : null;
  return p ? { url: SITE + p.file, caption: p.caption } : null;
}

/* Pure helper (unit-tested): strip [[photo:x]] tags from a reply and return whitelisted images.
   [[photo:none]] suppresses photos. No tag -> keyword fallback on the visitor's message. */
function extractPhotos(replyText, visitorText) {
  const tags = [];
  let text = String(replyText || "").replace(PHOTO_TAG_RE, (m, k) => {
    tags.push(String(k).trim().toLowerCase());
    return "";
  });
  text = text.replace(/\[\[\s*photo[^\]]*$/i, "").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  const images = [];
  const seen = new Set();
  const add = (key) => {
    const p = photoFor(key);
    if (p && !seen.has(p.url) && images.length < MAX_PHOTOS) {
      seen.add(p.url);
      images.push(p);
    }
  };
  if (tags.includes("none")) return { text, images: [] };
  if (tags.length) {
    tags.forEach(add);
  } else {
    const scan = (t) => {
      const hits = [];
      for (const [re, key] of PHOTO_KEYWORDS) {
        const m = re.exec(String(t || ""));
        if (m) hits.push([m.index, key]);
      }
      let ks = hits.sort((a, b) => a[0] - b[0]).map((h) => h[1]);
      /* a specific NdFeB shape beats the generic NdFeB photo */
      if (ks.includes("ndfeb-discs") || ks.includes("ndfeb-blocks")) ks = ks.filter((k) => k !== "ndfeb");
      return ks;
    };
    let keys = scan(visitorText);
    /* Visitor sent only a photo / "do you have this?": look at what the reply talks about, but only when it is focused (<=2 product types) */
    if (!keys.length) {
      const fromReply = scan(text);
      if (fromReply.length && fromReply.length <= 2) keys = fromReply;
    }
    keys.forEach(add);
  }
  return { text, images };
}

function lastVisitorText(messages) {
  const l = lastUserText(messages);
  return String(l.text || "").replace(/\[Attached[^\]]*\]/g, "").slice(0, 1000);
}

/* Guard/safety classifier output (e.g. Llama Guard, Nemotron safety) is never a valid chat answer. */
const GUARD_RE = /^\s*(?:(?:user|response|assistant|prompt)\s+safety\s*:|(?:un)?safe\s*(?:\n|$))|\b(?:user|response)\s+safety\s*:\s*(?:safe|unsafe)\b|\bsafety\s*(?:categories|category)\s*:/i;

/* Remove dangling list markers / bold markers / list intros left at the end of a cut-off reply. */
function stripDangling(text) {
  let t = String(text || "").replace(/\s+$/, "");
  let changed = false;
  for (let i = 0; i < 20; i++) {
    const prev = t;
    /* bullet / numbered marker (optionally followed by bold markers) alone on the last line */
    t = t.replace(/\n[ \t]*(?:[-*•>]|\d{1,2}[.)])[ \t]*(?:\*{1,3}|_{1,3})?[ \t]*$/, "");
    /* bold/italic/bullet markers left dangling at the very end of the text ("...details? * **") */
    t = t.replace(/[ \t]+(?:[-•]|\*{1,3}|_{2,3})(?:[ \t]+(?:\*{1,3}|_{2,3}))*$/, "");
    t = t.replace(/^[ \t]*(?:[-*•>]|\*{1,3}|_{2,3})[ \t]*$/m, (m) => m).replace(/\s+$/, "");
    if (t === prev) break;
    changed = true;
  }
  /* a list intro ending with ":" and nothing after it */
  const beforeColon = t;
  t = t.replace(/[ \t]*:$/, "");
  if (t !== beforeColon) changed = true;
  return { text: t.replace(/\s+$/, ""), changed };
}

/* Pure helper (unit-tested): decide whether a model reply is fit to show the visitor. */
function assessReply(raw, finish) {
  const text = String(raw || "").trim();
  if (!text) return { ok: false, reason: "empty content" };
  if (GUARD_RE.test(text)) return { ok: false, reason: "guard/safety-classifier output" };
  const s = stripDangling(text);
  const plain = s.text.replace(/[\s*_#>\-•.:;,!?()[\]`~|]+/g, "");
  if (s.text.length < 15 || plain.length < 8) return { ok: false, reason: "too short / only symbols" };
  const cut = finish === "length" || finish === "max_tokens";
  if (s.changed || cut) {
    let partial = s.text;
    if (cut && !s.changed && !/[.!?)\]"'’”]$/.test(partial)) {
      /* cut mid-sentence: keep up to the last complete sentence/line */
      const k = Math.max(partial.lastIndexOf("\n"), partial.search(/[.!?][^.!?]*$/));
      if (k > 40) partial = partial.slice(0, k + (partial[k] === "\n" ? 0 : 1)).trim();
    }
    return {
      ok: false,
      reason: s.changed ? "truncated (dangling list marker)" : "truncated (finish_reason length)",
      partial: partial.length >= 30 ? partial : "",
    };
  }
  return { ok: true, text };
}

function normalizeMessages(messages) {
  const out = [];
  for (const m of messages) {
    if (!m || (m.role !== "user" && m.role !== "assistant")) continue;
    if (typeof m.content === "string") {
      const t = String(m.content).slice(0, MAX_TEXT);
      if (t) out.push({ role: m.role, content: t });
      continue;
    }
    if (!Array.isArray(m.content)) continue;
    const parts = [];
    let dropped = false;
    for (const part of m.content) {
      if (!part || typeof part !== "object") continue;
      if (part.type === "text" && typeof part.text === "string") {
        parts.push({ type: "text", text: String(part.text).slice(0, MAX_TEXT) });
      } else if (
        part.type === "image_url" &&
        part.image_url &&
        typeof part.image_url.url === "string"
      ) {
        const url = String(part.image_url.url);
        if (
          /^data:image\/(jpeg|jpg|png|webp);base64,/i.test(url) &&
          url.length <= MAX_DATA_URL
        ) {
          parts.push({ type: "image_url", image_url: { url } });
        } else {
          dropped = true;
        }
      } else if (part.type === "file" && part.file && typeof part.file === "object") {
        const fname = String(part.file.filename || "sketch.pdf").slice(0, 120);
        const data = String(part.file.file_data || "");
        if (
          /^data:application\/pdf;base64,/i.test(data) &&
          data.length <= MAX_DATA_URL
        ) {
          parts.push({
            type: "file",
            file: { filename: fname, file_data: data },
          });
        } else {
          dropped = true;
        }
      }
    }
    if (dropped) {
      parts.push({
        type: "text",
        text: "[Note: the visitor's attachment was too large or unsupported and could not be received. Say so honestly and ask them to resend a smaller photo or WhatsApp it to +60 12-211 2522.]",
      });
    }
    if (!parts.length) continue;
    /* Assistants should stay string; users may be multimodal */
    if (m.role === "assistant") {
      out.push({ role: "assistant", content: contentToText(parts).slice(0, MAX_TEXT) });
    } else {
      out.push({ role: "user", content: parts });
    }
  }
  return out;
}

function contentToText(content) {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content
    .map((p) => {
      if (!p) return "";
      if (p.type === "text") return p.text || "";
      if (p.type === "image_url") return "[Attached image]";
      if (p.type === "file")
        return "[Attached file: " + ((p.file && p.file.filename) || "file") + "]";
      return "";
    })
    .filter(Boolean)
    .join("\n");
}

function sanitizeLead(lead) {
  if (!lead || typeof lead !== "object") return null;
  const name = String(lead.name || "").trim().slice(0, 80);
  const phone = String(lead.phone || "").trim().slice(0, 40);
  const email = String(lead.email || "").trim().slice(0, 120);
  if (name.length < 2) return null;
  const phoneOk = phone.replace(/\s+/g, "").length >= 8;
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!phoneOk && !emailOk) return null;
  return { name, phone: phoneOk ? phone : "", email: emailOk ? email : "" };
}

function lastUserText(messages) {
  if (!Array.isArray(messages)) return { text: "", image: null };
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (!m || m.role !== "user") continue;
    let image = null;
    if (Array.isArray(m.content)) {
      for (const p of m.content) {
        if (p && p.type === "image_url" && p.image_url && typeof p.image_url.url === "string") {
          image = p.image_url.url;
        }
      }
    }
    return { text: contentToText(m.content), image };
  }
  return { text: "", image: null };
}

function leadLines(lead) {
  return [
    `Name: ${lead.name}`,
    lead.phone ? `WhatsApp/phone: ${lead.phone}` : null,
    lead.email ? `Email: ${lead.email}` : null,
  ].filter(Boolean);
}

async function telegramSend(env, text) {
  const token = (env.LEAD_TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = (env.LEAD_TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId) return false;
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text: String(text).slice(0, 3500) }),
  }).catch(() => {});
  return true;
}

async function telegramPhoto(env, dataUrl, caption) {
  const token = (env.LEAD_TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = (env.LEAD_TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId || !dataUrl) return;
  const m = /^data:(image\/(?:jpeg|jpg|png|webp));base64,(.+)$/i.exec(dataUrl);
  if (!m) return;
  try {
    const bin = atob(m[2]);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const form = new FormData();
    form.append("chat_id", chatId);
    form.append("caption", String(caption).slice(0, 900));
    form.append("photo", new Blob([bytes], { type: m[1] }), "visitor-photo.jpg");
    await fetch(`https://api.telegram.org/bot${token}/sendPhoto`, {
      method: "POST",
      body: form,
    }).catch(() => {});
  } catch (e) {}
}

async function notifyLead(env, lead, messages) {
  try {
    const firstMsg = Array.isArray(messages) && messages[0] ? messages[0] : null;
    let first = "";
    if (firstMsg) {
      if (typeof firstMsg.content === "string") first = firstMsg.content;
      else first = contentToText(firstMsg.content);
    }
    first = String(first).slice(0, 200);
    const text = [
      "🧲 Magnet Expert lead (magnets.com.my)",
      ...leadLines(lead),
      first ? `First msg: ${first}` : null,
    ]
      .filter(Boolean)
      .join("\n");
    await telegramSend(env, text);
  } catch (e) {}
}

/* AI could not answer: forward the visitor's enquiry (and photo) so the team can reply by WhatsApp. */
async function notifyFailure(env, lead, messages, reasons) {
  try {
    const last = lastUserText(messages);
    const text = [
      "⚠️ Magnet Expert AI could NOT answer — please reply to this visitor",
      ...leadLines(lead),
      last.text ? `Message: ${String(last.text).slice(0, 500)}` : null,
      last.image ? "(visitor attached a photo — sent below if possible)" : null,
      "Reason: " + reasons.map((r) => String(r).slice(0, 120)).join(" | ").slice(0, 600),
    ]
      .filter(Boolean)
      .join("\n");
    const sent = await telegramSend(env, text);
    if (sent && last.image) {
      await telegramPhoto(env, last.image, `Photo from ${lead.name}`);
    }
  } catch (e) {}
}

function withImages(obj, images) {
  if (Array.isArray(images) && images.length) obj.images = images.slice(0, MAX_PHOTOS);
  return obj;
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}

export { parseCompletion, assessReply, stripDangling, pickPrimary, extractPhotos, PHOTOS, BASE_SYSTEM };
