/**
 * POST /api/magnet-chat
 * Env: OPENROUTER_API_KEY, LLM_MODEL (default openrouter/free)
 * For photo/sketch vision: set LLM_MODEL to a multimodal model
 *   e.g. google/gemini-2.0-flash-001 or openai/gpt-4o-mini
 * Optional lead notify: LEAD_TELEGRAM_BOT_TOKEN, LEAD_TELEGRAM_CHAT_ID
 */
const MAX_DATA_URL = 900000;
const MAX_TEXT = 4000;

const BASE_SYSTEM = `You are Magnet Expert for Arrowmatics Magnets (www.magnets.com.my).
Company: Arrowmatics AI Sdn Bhd (1305806-W), Shah Alam, Selangor, Malaysia.
WhatsApp / mobile for human sales: +60 12-211 2522 (https://wa.me/60122112522). Office +603 5191 0299.
Email: arrowmatics@gmail.com / bensonlok@gmail.com.

VOICE (non-negotiable):
- Reply in a possible, positive tone to EVERY question. Never shut the door. If constrained, still guide a workable next step.
- Warm, concise, professional English. Use the visitor’s name when known.
- Assume many visitors are NEW to magnetic separators — guide patiently; never shame lack of technical knowledge.

PHOTO / SKETCH FIRST:
- Invite or welcome a machine photo or hand sketch (circle/point at the problem). This is the preferred start.
- When an image or PDF sketch is attached, describe what you see briefly, then recommend 1–2 application-fit options from OUR SITE RANGE only: magnetic separators (grate, bullet, drawer, pulley, plate / liquid trap), NdFeB (N35–N52), SmCo, or lifting magnets (~3:1 safety).
- Do NOT invent products, brands, or SKUs not on magnets.com.my. If the photo is unclear, ask one focused clarifying question and still give a best-guess family.
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

    const cleaned = normalizeMessages(
      Array.isArray(body.messages) ? body.messages.slice(-12) : []
    );
    if (!cleaned.length) {
      return json({ error: "No messages" }, 400, cors);
    }

    const hasVision = cleaned.some((m) => Array.isArray(m.content));
    const leadLine = `Visitor lead on file: name=${lead.name}; phone=${lead.phone || "—"}; email=${lead.email || "—"}.`;
    const model = (context.env.LLM_MODEL || "openrouter/free").trim();

    let reply = await callOpenRouter(key, model, BASE_SYSTEM + "\n" + leadLine, cleaned);
    if (reply.error && hasVision) {
      /* Fallback: strip images/files, keep text so chat still works on text-only models */
      const textOnly = cleaned.map((m) => ({
        role: m.role,
        content: typeof m.content === "string" ? m.content : contentToText(m.content),
      }));
      reply = await callOpenRouter(
        key,
        model,
        BASE_SYSTEM +
          "\n" +
          leadLine +
          "\nNote: visitor attached a photo/sketch but this model path is text-only; use their description and the attachment note.",
        textOnly
      );
    }
    if (reply.error) {
      return json({ error: reply.error }, 502, cors);
    }
    return json({ reply: reply.text || "(no reply)", lead_ok: true }, 200, cors);
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

async function callOpenRouter(key, model, system, messages) {
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
      max_tokens: 700,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = (data.error && data.error.message) || `LLM HTTP ${res.status}`;
    return { error: msg };
  }
  const text =
    (data.choices &&
      data.choices[0] &&
      data.choices[0].message &&
      data.choices[0].message.content) ||
    "";
  return { text: String(text).trim() };
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
        }
      }
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

async function notifyLead(env, lead, messages) {
  const token = (env.LEAD_TELEGRAM_BOT_TOKEN || "").trim();
  const chatId = (env.LEAD_TELEGRAM_CHAT_ID || "").trim();
  if (!token || !chatId) return;
  const firstMsg = Array.isArray(messages) && messages[0] ? messages[0] : null;
  let first = "";
  if (firstMsg) {
    if (typeof firstMsg.content === "string") first = firstMsg.content;
    else first = contentToText(firstMsg.content);
  }
  first = String(first).slice(0, 200);
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
