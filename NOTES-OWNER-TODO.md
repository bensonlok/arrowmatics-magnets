# Owner-needed items (magnets.com.my)

Nothing below is on the live site yet. Items marked **[OWNER]** need a fact or decision from Benson. No placeholder text is published in any page or schema.

## Conflicts to resolve first
- **[OWNER] WhatsApp number.** The task brief said WhatsApp +60 19-662 6522. Every page, schema block, llms file and the chat widget uses **+60 12-211 2522** (office +603 5191 0299). The 19-662 6522 number appears nowhere in the repo. Not added. Confirm which is correct.
- **[OWNER] Languages.** ContactPoint `availableLanguage` says English only; the Magnet Expert chat replies in English / 中文 / Bahasa Malaysia. Confirm what the humans reply in, then align the schema.

## sameAs profiles (schema Organization/LocalBusiness)
- [OWNER] Google Business Profile URL: `__GBP_URL__`
- [OWNER] LinkedIn company page URL: `__LINKEDIN_URL__`
- [OWNER] YouTube channel URL: `__YOUTUBE_URL__`
- Add to the `sameAs` array in `main-app/index.html` only once the profiles exist and carry the same name/address/phone.

## Evidence content (to make the site more trustworthy)
- [OWNER] Case notes: real jobs, anonymised if needed, with the customer's permission. Format: problem, product, what was supplied. No numbers unless measured. `__CASE_NOTE_1__`
- [OWNER] Gauss-meter reading photos: a photo of an actual reading on a real magnet, with the model and distance noted. `__GAUSS_PHOTO_1__`
- [OWNER] Years in business / company start date: `__YEARS__` (the About page deliberately states none).
- [OWNER] Team names and roles, only if you want them published: `__TEAM__`

## Identity
- [OWNER] Domain email (e.g. sales@magnets.com.my) to replace the two Gmail addresses: `__DOMAIN_EMAIL__`
- [RESOLVED 2026-10-03] Old trading name: owner decided the legal/business name is **Arrowmatics AI Sdn Bhd (1305806-W)**. The old name is not used anywhere on the site and is not an `alternateName`. Schema carries `legalName` "Arrowmatics AI Sdn Bhd" and `identifier` "1305806-W".

## Claims to keep as they are
- Arrowmatics is **not itself certified** to HACCP / ISO 22000. Pages say "for food plants working to HACCP / ISO 22000". Do not change unless a real certificate exists.
- Reply time is a target ("within 1–3 hours, Malaysia business hours"), not a guarantee. Confirm you can keep it.
- Wikimedia Commons CC photos need their attribution kept; see `IMAGE-CREDITS.md`.

## Infrastructure (Cloudflare / search)
- [OWNER] Cloudflare: turn on HSTS (SSL/TLS > Edge Certificates) after confirming the whole site is HTTPS.
- [OWNER] Google Search Console and Bing Webmaster: submit the new sitemap and request re-crawl for `/LiquidLineMagneticTrap.html` (now 301 to `/magnetic-separators.html#liquid-line-trap`) and the old `.htm` URLs.
- Pages are served without `.html` by Cloudflare (308); the canonical tags and sitemap still use `.html`. Consider switching both to the extensionless URL.

## Build scripts
`scripts/build_pages.py` regenerates the industries hub, 5 industry pages and About (plus `.md`). `scripts/components.py` holds the shared blocks. `rebuild_home.py` and `restructure_key_pages.py` are one-off transforms kept for reference; do not re-run them on the current files.

---
## Marketing-skills build (2026-10-03): items that need the owner

### Lead flow: environment variables (Cloudflare Pages > Settings > Environment variables)
- `LEAD_TELEGRAM_BOT_TOKEN` and `LEAD_TELEGRAM_CHAT_ID` (the same two the Magnet Expert chat already uses). **[OWNER] Confirm they are set.** If they are not set, `/api/lead` still validates and the page tells the visitor "we could not confirm delivery, please use WhatsApp/email", so no lead is silently lost, but you will not be notified of form submissions.
- Test mode: add `?leadtest=1` to any page URL; forms validate and show success but the server never sends anything. Live checks use this.
- The checklist "gate" is a soft gate: the PDF at `/downloads/Magnetic-Separator-Selection-Checklist.pdf` is a static file anyone can open. That is deliberate (no fake lock). Remove the direct link from `llms`/sitemap if you want it less discoverable (it is not listed there).
- No rate limiting or storage is built in (no database). Cloudflare WAF rate limiting on `/api/lead` is recommended: [OWNER] set one rule.

### Confirmations
- **[OWNER] WhatsApp number**: still +60 12-211 2522 everywhere. Single place to change the JS-side constant: `main-app/js/site-config.js`. Static HTML/schema/llms: run `python3 scripts/swap_whatsapp.py 60122112522 <new digits>` then review the diff. Do this only after you choose between +60 12-211 2522 and +60 19-662 6522.
- **[OWNER] Privacy notice** (`/privacy.html`): written to be PDPA-aware but it is a plain-language draft, not legal advice. Confirm the retention wording you want (currently none stated), the contact email, and have it reviewed if you wish.
- **[OWNER] Analytics**: nothing is installed. Hooks exist (`window.magnetsTrack`, DOM event `magnets:event`) for: cta_whatsapp, cta_call, cta_email, cta_expert, selector_use, form_start, form_submit, form_error, checklist_unlocked, checklist_download. To measure, enable **Cloudflare Web Analytics** (cookieless, no code change if proxied) or add Plausible; events forward automatically if `window.plausible`/`dataLayer`/`gtag` exist. If you add any tracker, update `/privacy.html`.
- **[OWNER] Photo size limit**: form photos are resized in the browser to about 1100 px; larger or failed uploads fall back to "send on WhatsApp".

### Trust section placeholders (NOT published; add only when real)
- Customer logos / permission-based case notes: `__CASE_NOTE_1__`, `__CASE_NOTE_2__`
- Gauss-meter reading photo with model and distance: `__GAUSS_PHOTO__`
- Years in business: `__YEARS__`
- Team names and photos: `__TEAM__`
- Google reviews widget or rating (only the real, current number): `__REVIEWS__`
- Typical lead times (pack says do NOT publish until confirmed): `__LEAD_TIME__`
- Which material documents Arrowmatics can actually supply for stainless: `__MATERIAL_DOCS__`
The live trust block shows only: registered company number and address, written quotes, reply target, honesty about certification.
