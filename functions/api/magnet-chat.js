/**
 * Cloudflare Pages Function: POST /api/magnet-chat
 * Env: OPENROUTER_API_KEY (required), LLM_MODEL (optional, default openrouter/free)
 */
const SYSTEM = `You are Magnet Expert for Arrowmatics Magnets (www.magnets.com.my).
Company: Arrowmatics AI Sdn Bhd (1305806-W), Shah Alam, Selangor, Malaysia.
WhatsApp / mobile for human sales: +60 12-211 2522 (https://wa.me/60122112522). Office +603 5191 0299.
Email: arrowmatics@gmail.com / bensonlok@gmail.com.

You help industrial buyers with: magnetic separators (grate, bullet, drawer, pulley, plate; typical 10,000–13,000 gauss), NdFeB (N35–N52), SmCo, lifting magnets (~3:1 safety factor), food-grade options, Malaysia/ASEAN supply.

Rules:
- Sales + technical, concise, professional EN.
- Never invent RM prices or stock. For quotes, urge WhatsApp +60 12-211 2522 with duty, size, qty, industry.
- If unsure, say so and offer Talk to human / WhatsApp.
- Do not claim you can visit site or place orders online.`;

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
    const messages = Array.isArray(body.messages) ? body.messages.slice(-12) : [];
    const cleaned = messages
      .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
      .map((m) => ({ role: m.role, content: String(m.content).slice(0, 4000) }));
    if (!cleaned.length) {
      return json({ error: "No messages" }, 400, cors);
    }

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
        messages: [{ role: "system", content: SYSTEM }, ...cleaned],
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
    return json({ reply: String(reply).trim() || "(no reply)" }, 200, cors);
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

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}
