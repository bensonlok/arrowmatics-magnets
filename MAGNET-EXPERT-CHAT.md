# Magnet Expert chat (magnets.com.my)

## What
- Floating **Magnet Expert** sales/technical chat
- **Talk to human** → WhatsApp +60 12-211 2522

## Cloudflare Pages env
Set on project `magnets-com-my`:
- `OPENROUTER_API_KEY` = (secret)
- `LLM_MODEL` = `openrouter/free` (optional)

## Files
- `functions/api/magnet-chat.js` → `POST /api/magnet-chat`
- `main-app/js/magnet-expert-chat.js`
- `main-app/css/magnet-expert-chat.css`
- Injected on home + product/FAQ pages

After merge, redeploy Pages and confirm env vars.

## Tone & proprietary knowledge
- Live reply brain: `functions/api/magnet-chat.js` → `BASE_SYSTEM`
- Editable company brief: `MAGNET-EXPERT-KNOWLEDGE.md` (edit, then ask Github to sync into `BASE_SYSTEM`)
- How to teach the bot proprietary facts: paste in chat to Github, or edit `MAGNET-EXPERT-KNOWLEDGE.md`, then say “sync Magnet Expert knowledge”
