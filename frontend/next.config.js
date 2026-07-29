/** @type {import('next').NextConfig} */
const nextConfig = {
  // NOTE: the previous rewrites() proxy has been removed.
  //
  // It was redundant: src/lib/api.ts calls the absolute API_BASE
  // (which already includes the "/api" prefix) directly via fetch, so the
  // proxy was never on the request path. Worse, when NEXT_PUBLIC_API_BASE
  // already contained "/api" (as .env.example ships it), the rewrite
  // doubled the prefix to ".../api/api/..." and 404'd. Removing it makes the
  // direct-fetch path the single source of truth.
};

module.exports = nextConfig;
