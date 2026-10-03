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
- [OWNER] Old trading name "Arrowmatics Engineering Trading": add as schema `alternateName` ONLY if you confirm it is the same business. **Not added anywhere.**

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
