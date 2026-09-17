# Arrowmatics Magnets — magnets.com.my

GEO/SEO-ready static website for **Arrowmatics Magnets** (legal: Arrowmatics AI Sdn Bhd 1305806-W).

Magnetic separators, NdFeB rare-earth magnets, and lifting magnets for industry in Malaysia. Based in Shah Alam; supply Malaysia-wide.

## Structure

- `main-app/` — Cloudflare Pages **output directory** (HTML, CSS, robots, sitemap, llms)
- `worker/index.js` — minimal asset passthrough (no SPA rewrite)
- `wrangler.toml` — CF config (`not_found_handling = "404"`)
- `DEPLOY.md` — step-by-step Cloudflare Pages + DNS cutover

## Local preview

Open files under `main-app/` in a browser, or:

```bash
npx serve main-app
```

## Build / deploy

```bash
npm run build    # echo ok — static site, no compile step
npm run deploy   # optional: wrangler pages deploy
```

Or connect GitHub `bensonlok/arrowmatics-magnets` in Cloudflare Pages (see `DEPLOY.md`).

## Canonical

- Apex: https://magnets.com.my/
- www → apex redirect (documented in DEPLOY.md and `main-app/_redirects`)
