/**
 * Minimal passthrough worker for Cloudflare assets.
 * Serves static files from main-app via the ASSETS binding.
 * Does NOT rewrite unknown paths to index.html — robots.txt,
 * sitemap.xml and llms.txt must remain plain text/xml.
 */
export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  },
};
