# Magnet Expert chat (magnets.com.my)

## What
- Floating **Magnet Expert** sales/technical chat
- Layout: messages LEFT; **RIGHT COLUMN** for photo/sketch upload + preview + tip
- Accepts **JPG / PNG / WebP** (client-compressed) and small **PDF** sketches
- Uploads go to `POST /api/magnet-chat` as OpenRouter multimodal content (image_url / file)
- **Talk to human** → WhatsApp +60 12-211 2522
- Lead gate: name + WhatsApp **or** email before chat (unchanged)

## Cloudflare Pages env
Set on project `magnets-com-my` (Settings → Environment variables):

| Var | Required | Notes |
|-----|----------|--------|
| `OPENROUTER_API_KEY` | **Yes** | OpenRouter secret |
| `LLM_MODEL` | Recommended | Default `openrouter/free`. For **photo/sketch vision**, set a multimodal model e.g. `google/gemini-2.0-flash-001` or `openai/gpt-4o-mini`. If the model rejects images, the API falls back to text-only with an attachment note. |
| `LEAD_TELEGRAM_BOT_TOKEN` | Optional | Lead notify |
| `LEAD_TELEGRAM_CHAT_ID` | Optional | Lead notify |

## Size limits
- Client resizes images to max edge 1280px, JPEG ~0.72 quality
- API rejects data URLs over ~900k characters (~650KB)
- PDF sketches capped ~700KB on the client

## Files
- `functions/api/magnet-chat.js` → `POST /api/magnet-chat` (also mirrored under `main-app/functions/api/`)
- `main-app/js/magnet-expert-chat.js`
- `main-app/css/magnet-expert-chat.css`
- Homepage **Easy as 1-2-3** section `#easy-123` + HowTo schema
- Injected on home + product/FAQ pages (`?v=photo123` cache-bust)

After push to `main`, Cloudflare Pages redeploys. Confirm env vars, then spot-check:
- https://magnets.com.my/#easy-123
- Open Magnet Expert → upload panel on the right (stacked on mobile)
- Schema/NAP/`llms.txt` unchanged in intent

## Tone & proprietary knowledge
- Live reply brain: `functions/api/magnet-chat.js` → `BASE_SYSTEM`
- Editable company brief: `MAGNET-EXPERT-KNOWLEDGE.md` (edit, then ask to sync into `BASE_SYSTEM`)
