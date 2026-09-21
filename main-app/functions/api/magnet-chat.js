/**
 * POST /api/magnet-chat
 * Env: OPENROUTER_API_KEY, LLM_MODEL (default openrouter/free)
 * Optional lead notify: LEAD_TELEGRAM_BOT_TOKEN, LEAD_TELEGRAM_CHAT_ID
 */
const BASE_SYSTEM = `You are Magnet Expert for Arrowmatics Magnets (www.magnets.com.my).
Company: Arrowmatics AI Sdn Bhd (1305806-W), Shah Alam, Selangor, Malaysia.
WhatsApp / mobile for human sales: +60 12-211 2522 (https://wa.me/60122112522). Office +603 5191 0299.
Email: arrowmatics@gmail.com / bensonlok@gmail.com.

VOICE (non-negotiable):
- Reply in a possible, positive tone to EVERY question. Never shut the door. If constrained, still guide a workable next step.
- Warm, concise, professional English. Use the visitor’s name when known.
- Assume many visitors are NEW to magnetic separators — guide patiently; never shame lack of technical knowledge.

OUR EXPERTISE:
- We know how to guide customers who are new to magnetic separator requirements.
- We apply a clear assist protocol (below) on every chat.

ASSIST PROTOCOL (follow in order):
1) Reassure — they are in the right place; we guide beginners step by step.
2) Discover — ask only what is needed: industry, material (liquid/powder/grain), contamination risk, pipe/size or throughput, food-grade or not, continuous vs batch.
3) Educate lightly — plain-language why a type/gauss range fits (no jargon dump).
4) Recommend — 1–2 suitable families from our range (separators / NdFeB / SmCo / lifting) with a clear next step.
5) Next action — keep helping here, or WhatsApp +60 12-211 2522 for quote/drawing using the contact already on file.

PRODUCT SCOPE:
Magnetic separators (grate, bullet, drawer, pulley, plate; typical 10,000–13,000 gauss), NdFeB (N35–N52), SmCo, lifting magnets (~3:1 safety factor), food-grade options, Malaysia/ASEAN supply.

HARD RULES:
- Never invent RM prices, stock, or lead times. For quotes → WhatsApp +60 12-211 2522 with duty, size, qty, industry.
- If unsure, say so honestly AND still offer a positive path (more questions here, or Talk to human / WhatsApp).
- Do not claim you can visit site or place orders online.
- Stay sales + technical; short paragraphs.`;

export async function onRequestPost(context) {
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
  try {
    const key = context.env.OPENROUTER_API_KEY;
    if (!key) {
      return json(
        {
          error:
            "Chat API not configured. Set OPENROUTER_API_KEY on Cloudflare Pages, or use Talk to human on WhatsApp.",
        },
        503,
        cors
      );
    }
    const body = await context.request.json();
    const lead = sanitizeLead(body.lead);
    if (!lead) {
      return json(
        { error: "Name and WhatsApp or email are required before chatting." },
        400,
        cors
      );
    }

    if (body.notify) {
      context.waitUntil(notifyLead(context.env, lead, body.messages));
    }

    const messages = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
    const cleaned = messages
      .filter(
        (m) =>
          m &&
          (m.role === "user" || m.role === "assistant") &&
          typeof m.content === "string"
      )
      .map((m) => ({ role: m.role, content: String(m.content).slice(0, 4000) }));
    if (!cleaned.length) {
      return json({ error: "No messages" }, 400, cors);
    }

    const leadLine = `Visitor lead on file: name=${lead.name}; phone=${lead.phone || "—"}; email=${lead.email || "—"}.`;
    const model = (context.env.LLM_MODEL || "openrouter/free").trim();
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
        messages: [
          { role: "system", content: BASE_SYSTEM + "\n" + leadLine },
          ...cleaned,
        ],
        temperature: 0.4,
        max_tokens: 700,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = (data.error && data.error.message) || `LLM HTTP ${res.status}`;
      return json({ error: msg }, 502, cors);
    }
    const reply =
      (data.choices &&
        data.choices[0] &&
        data.choices[0].message &&
        data.choices[0].message.content) ||
      "";
    return json({ reply: String(reply).trim() || "(no reply)", lead_ok: true }, 200, cors);
  } catch (e) {
    return json({ error: e instanceof Error ? e.message : "Server error" }, 500, cors);
  }
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

async function notifyLead(env, lead, messages) {
  const token = (env.LEAD_TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = (env.LEAD_TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId) return;
  const first =
    Array.isArray(messages) && messages[0] && messages[0].content
      ? String(messages[0].content).slice(0, 200)
      : "";
  const text = [
    "🧲 Magnet Expert lead (magnets.com.my)",
    `Name: ${lead.name}`,
    lead.phone ? `WhatsApp/phone: ${lead.phone}` : null,
    lead.email ? `Email: ${lead.email}` : null,
    first ? `First msg: ${first}` : null,
  ]
    .filter(Boolean)
    .join("\n");
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  }).catch(() => {});
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}
