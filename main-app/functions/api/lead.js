/**
 * POST /api/lead  — lightweight lead capture for magnets.com.my
 *
 * Kinds: "quote" (name + WhatsApp/email + message, optional photo) and
 *        "checklist" (name + email, optional WhatsApp).
 *
 * Delivery: the owner's existing private Telegram alert channel
 *   (env LEAD_TELEGRAM_BOT_TOKEN + LEAD_TELEGRAM_CHAT_ID — same vars as the Magnet Expert chat).
 * If those are not configured the endpoint still validates and answers
 *   { ok: true, delivered: false } so the page can show the WhatsApp / email fallback.
 *
 * Nothing is stored. Nothing is sent to the visitor. Nothing is sent anywhere
 * unless the visitor submits the form with consent ticked.
 * Test mode: { test: true } validates only and never sends (used for live checks).
 */
const ALLOWED_ORIGINS = [
  /^https:\/\/(www\.)?magnets\.com\.my$/i,
  /^https:\/\/[a-z0-9-]+\.pages\.dev$/i,
  /^http:\/\/localhost(:\d+)?$/i,
];
const MAX_BODY = 1_200_000; // ~0.9 MB photo as base64 + text

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

const clean = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f\u007f]+/g, " ").replace(/\s+/g, " ").trim().slice(0, n);
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE_RE = /^\+?[0-9][0-9\s\-()]{6,18}[0-9]$/;

export function validateLead(body) {
  if (!body || typeof body !== "object") return { error: "Bad request." };
  if (body.website) return { honeypot: true }; // bots fill hidden field
  const kind = body.kind === "checklist" ? "checklist" : body.kind === "quote" ? "quote" : "";
  if (!kind) return { error: "Unknown form." };
  const name = clean(body.name, 80);
  const email = clean(body.email, 120);
  const phone = clean(body.phone, 30);
  const message = clean(body.message, 600);
  if (!name) return { error: "Please enter your name." };
  if (body.consent !== true) return { error: "Please tick the consent box so we may reply." };
  if (email && !EMAIL_RE.test(email)) return { error: "That email address does not look right." };
  if (phone && !PHONE_RE.test(phone)) return { error: "That phone number does not look right." };
  if (kind === "checklist" && !email) return { error: "Please enter your email." };
  if (kind === "quote" && !email && !phone) return { error: "Please give a WhatsApp number or email." };
  if (kind === "quote" && message.length < 5) return { error: "Please tell us briefly what you need." };
  const photo = typeof body.photo === "string" && /^data:image\/(jpeg|jpg|png|webp);base64,/i.test(body.photo) && body.photo.length < 900_000 ? body.photo : "";
  return { lead: { kind, name, email, phone, message, photo, page: clean(body.page, 120), context: clean(body.context, 60) } };
}

function summary(l) {
  return [
    l.kind === "quote" ? "📩 Quote request (magnets.com.my)" : "📄 Checklist download (magnets.com.my)",
    `Name: ${l.name}`,
    l.phone ? `WhatsApp/phone: ${l.phone}` : null,
    l.email ? `Email: ${l.email}` : null,
    l.message ? `Message: ${l.message}` : null,
    l.page ? `Page: ${l.page}${l.context ? " · " + l.context : ""}` : null,
    "Consent: ticked on form",
  ].filter(Boolean).join("\n");
}

async function tg(env, method, payload, isForm) {
  const token = (env.LEAD_TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = (env.LEAD_TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId) return false;
  try {
    if (isForm) payload.append("chat_id", chatId);
    const res = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
      method: "POST",
      headers: isForm ? undefined : { "Content-Type": "application/json" },
      body: isForm ? payload : JSON.stringify({ chat_id: chatId, ...payload }),
    });
    return res.ok;
  } catch (e) {
    return false;
  }
}

function configured(env) {
  return !!((env.LEAD_TELEGRAM_BOT_TOKEN || "").trim() && (env.LEAD_TELEGRAM_CHAT_ID || "").trim());
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const origin = request.headers.get("Origin");
  if (origin && !ALLOWED_ORIGINS.some((re) => re.test(origin))) return json({ ok: false, error: "Not allowed." }, 403);
  const len = parseInt(request.headers.get("Content-Length") || "0", 10);
  if (len > MAX_BODY) return json({ ok: false, error: "Photo is too large. Please send it on WhatsApp instead." }, 413);
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ ok: false, error: "Bad request." }, 400);
  }
  const v = validateLead(body);
  if (v.honeypot) return json({ ok: true, delivered: false, test: false }); // silently drop bots
  if (v.error) return json({ ok: false, error: v.error }, 400);
  const lead = v.lead;

  if (body.test === true) {
    // validate-only: never sends anything
    return json({ ok: true, test: true, delivered: false, channelConfigured: configured(env) });
  }
  if (!configured(env)) return json({ ok: true, delivered: false, channelConfigured: false });

  let delivered = await tg(env, "sendMessage", { text: summary(lead).slice(0, 3500) });
  if (delivered && lead.photo) {
    const m = /^data:(image\/(?:jpeg|jpg|png|webp));base64,(.+)$/i.exec(lead.photo);
    if (m) {
      try {
        const bin = atob(m[2]);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        const form = new FormData();
        form.append("caption", `Photo from ${lead.name}`.slice(0, 200));
        form.append("photo", new Blob([bytes], { type: m[1] }), "enquiry-photo.jpg");
        await tg(env, "sendPhoto", form, true);
      } catch (e) {}
    }
  }
  return json({ ok: true, delivered });
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: { Allow: "POST, OPTIONS" } });
}
