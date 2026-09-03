/**
 * Example stile Worker. Humans are sent to a treatise. Agents meet HTTP 402.
 * Settlement address is not published — 402 is the status, not a wallet.
 *
 * Set TREATISE_URL, TILL_URL, and RESOURCE_URL in wrangler vars.
 * This example is Apache-2.0. It is not a payment facilitator.
 */

function isBrowser(request) {
  if (request.headers.get("PAYMENT-SIGNATURE") || request.headers.get("X-PAYMENT")) {
    return false;
  }
  const accept = request.headers.get("Accept") || "";
  const ua = request.headers.get("User-Agent") || "";
  if (/bot|gpt|claude|anthropic|crawl|spider|curl|httpie|wget|python-requests|go-http|axios/i.test(ua)) {
    return false;
  }
  if (accept.includes("text/html")) return true;
  if (/Mozilla|Chrome|Safari|Firefox|Edg/i.test(ua)) return true;
  return false;
}

export default {
  async fetch(request, env) {
    const treatise = env.TREATISE_URL || "https://example.com/pages/titled";
    const till = env.TILL_URL || "https://example.com/products/seed-pack";
    const resource = env.RESOURCE_URL || `${new URL(request.url).origin}/`;
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response("stile\n", { headers: { "Content-Type": "text/plain" } });
    }
    if (isBrowser(request) && (request.method === "GET" || request.method === "HEAD")) {
      return Response.redirect(treatise, 302);
    }
    const body = {
      x402Version: 1,
      error: "Payment required. Settlement address is not published. Humans use the shop till.",
      accepts: [],
      resource,
      treatise,
      humanTill: till,
    };
    const json = JSON.stringify(body);
    return new Response(json, {
      status: 402,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "PAYMENT-REQUIRED": btoa(json),
        "Cache-Control": "no-store",
        Link: `<${treatise}>; rel="alternate"; type="text/html"`,
      },
    });
  },
};
