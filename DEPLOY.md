# Deploy magnets.com.my to Cloudflare Pages

## Site settings (Cloudflare Pages)

1. Log in to Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
2. Select repository: **`bensonlok/arrowmatics-magnets`**.
3. Production branch: **`main`**.
4. Framework preset: **None**.
5. Build command: **leave empty** (or `npm run build` which only echoes ok).
6. Build output directory: **`main-app`**.
7. Root directory: repository root (where `main-app/` lives).
8. Save and deploy.

### Critical: not an SPA

Do **not** enable “Single-page application” / SPA fallback that serves `index.html` for all paths. Missing URLs must return **404**.

If using Wrangler locally or Workers assets:

- `wrangler.toml` sets `not_found_handling = "none" (null-body 404; never single-page-application)`.
- `worker/index.js` only passes through `env.ASSETS.fetch(request)` — it does **not** rewrite `robots.txt`, `sitemap.xml`, or `llms.txt` to HTML.

After deploy, verify:

- https://magnets.com.my/robots.txt → plain text
- https://magnets.com.my/sitemap.xml → XML
- https://magnets.com.my/llms.txt → plain text
- https://magnets.com.my/no-such-page → 404 (not homepage HTML)

## Custom domains & DNS

### Canonical rule

- **Primary (canonical):** `https://magnets.com.my/` (apex)
- **www must redirect** to apex: `https://www.magnets.com.my/*` → `https://magnets.com.my/:splat` (301)

### Attach domains in Pages

1. Pages project → **Custom domains**.
2. Add `magnets.com.my` and `www.magnets.com.my`.
3. Follow Cloudflare’s DNS instructions (usually CNAME for www to the Pages hostname; apex via CNAME flattening or A/AAAA as Cloudflare shows).

### Replace Exabytes / old Apache hosting

Exabytes currently hosts a bot-walled Apache site. To cut over:

1. In the domain registrar / Exabytes DNS panel, **remove or replace** existing A/CNAME records that point to the old Apache host.
2. Point **magnets.com.my** and **www.magnets.com.my** to the Cloudflare Pages target (as shown when you add Custom domains).
3. Prefer managing DNS **in Cloudflare** (nameservers at CF) so apex + www + redirects stay consistent.
4. Wait for DNS TTL to expire; confirm apex serves the new Pages deploy.

### www → apex redirect

Configure one of:

1. **Cloudflare Bulk Redirects / Redirect Rules** (recommended):  
   `https://www.magnets.com.my/*` → `https://magnets.com.my/$1` (301, preserve path).
2. Or rely on Pages/`_redirects` in `main-app/_redirects` where supported.

HTML canonical tags and `sitemap.xml` use **apex only** (`https://magnets.com.my/...`).

## Post-deploy checklist

1. **Google Search Console** — property `https://magnets.com.my/` → submit `https://magnets.com.my/sitemap.xml`.
2. **Bing Webmaster Tools** — submit the same sitemap.
3. **Google Business Profile** — set website to `https://magnets.com.my/` (apex).
4. Spot-check NAP on every page footer: Shah Alam address, +60 12-211 2522, +603 5191 0299, arrowmatics@gmail.com.
5. WhatsApp FAB → `https://wa.me/60122112522`.

## Optional CLI deploy

```bash
npm install
npm run deploy
# or: npx wrangler pages deploy main-app --project-name=magnets-com-my
```

Do not force-push or change DNS without owner approval. This repo is written locally; push to GitHub is handled separately.
