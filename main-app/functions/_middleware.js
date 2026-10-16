// Canonical host: 301 www.magnets.com.my (and any http) -> https://magnets.com.my (path + query kept).
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === "www.magnets.com.my" || (url.protocol === "http:" && url.hostname === "magnets.com.my")) {
    url.hostname = "magnets.com.my";
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
