export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      const key = decodeURIComponent(url.pathname.replace(/^\/r2\//, ""));
      const obj = await env.FITSAGA_CACHE.get(key);
      if (!obj) return new Response("not found: " + key, { status: 404 });
      return new Response(obj.body, {
        headers: {
          "Content-Type": obj.httpMetadata?.contentType || "image/webp",
          "Cache-Control": "public, max-age=31536000, immutable",
        },
      });
    } catch (e) {
      return new Response("err: " + String(e).slice(0, 120), { status: 500 });
    }
  }
};
