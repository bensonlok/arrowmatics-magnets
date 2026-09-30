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
- Injected on home + product/FAQ pages (`?v=sss-custom-20260926` cache-bust)

After push to `main`, Cloudflare Pages redeploys. Confirm env vars, then spot-check:
- https://magnets.com.my/#easy-123
- Open Magnet Expert → upload panel on the right (stacked on mobile)
- Schema/NAP/`llms.txt` unchanged in intent

## Tone & proprietary knowledge
- Live reply brain: `functions/api/magnet-chat.js` → `BASE_SYSTEM`
- Editable company brief: `MAGNET-EXPERT-KNOWLEDGE.md` (edit, then ask to sync into `BASE_SYSTEM`)


## Reliability (never a silent failure)
- `main-app/functions/api/magnet-chat.js` is the copy Cloudflare deploys (root `functions/` is a mirror).
- Model order: `LLM_MODEL` (default `openrouter/free`), then vision-capable fallbacks (`google/gemini-2.5-flash-lite`, `openai/gpt-4o-mini`), then a text-only retry. Empty/array/error responses are parsed safely.
- If everything fails the visitor still gets a helpful WhatsApp message, and (if Telegram env vars are set) the owner receives a "AI could NOT answer" alert with the visitor's message and photo.
- Browser resizes photos to <=1280px JPEG before upload; only the newest image is sent upstream.
- `openrouter/free` is never used for chat (code substitutes `google/gemini-2.5-flash-lite`, even if `LLM_MODEL` is set to it). Replies that look like guard/safety-classifier output, are too short, or are cut off (finish_reason length / dangling `* **` bullets) are rejected and the next model is tried. Tests: `node tests/magnet-chat.test.mjs`.

## Example photos
- `magnet-chat.js` has a fixed `PHOTOS` whitelist (files under `main-app/images/`, served as `https://www.magnets.com.my/images/...`). The model may end its reply with `[[photo:KEY]]`; the server strips the tag (also malformed/unknown ones), maps it to whitelisted photos (max 2) and returns `images: [{url, caption}]`. If the model gives no tag, a keyword fallback looks at the visitor's message (then, if focused, at the reply). `[[photo:none]]` suppresses photos.
- Frontend renders same-site `/images/` thumbnails only (tap = full size in new tab) with the note "Example photo — actual spec confirmed at quotation". Tests: `node tests/magnet-chat.test.mjs`.

| Key | File |
|---|---|
| ndfeb | ndfeb-blocks.jpg (discs + blocks) |
| ndfeb-discs | real-ndfeb-4.jpg |
| ndfeb-blocks | real-ndfeb-3.jpg |
| smco | real-smco-2.jpg |
| plate | plate-magnet-10000g.jpg |
| bars | real-bars-1.jpg |
| grate | real-grate-1.jpg |
| hopper | real-hopper-grate-1.jpg |
| lifting | real-lifting-1.jpg |
| drawer | real-drawer-1.jpg |
| drum | real-drum-1.jpg |
| bullet | real-bullet-1.jpg |
| liquid | real-liquid-trap-1.jpg |
