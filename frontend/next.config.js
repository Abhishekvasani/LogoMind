/** @type {import('next').NextConfig} */

// Server-side backend base (used by rewrites below). On the server, 127.0.0.1
// is always reachable even when the browser guest is sandboxed and cannot hit
// the backend's loopback address directly.
const BACKEND = process.env.BACKEND_API_BASE || "http://127.0.0.1:8000/api";

const nextConfig = {
  // Proxy /api/* requests to the FastAPI backend, server-side. The frontend
  // client (src/lib/api.ts) calls the SAME-ORIGIN path "/api/...", so the
  // browser never needs to reach the backend host directly (which fails inside
  // sandboxed in-app browsers where the guest's loopback ≠ the host loopback).
  // This also removes CORS from the production path behind a single origin.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${BACKEND}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
