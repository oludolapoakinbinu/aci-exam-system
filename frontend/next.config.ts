import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  // API lives in Next.js route handlers (Netlify-compatible).
  // Optional local FastAPI: set USE_FASTAPI=1 when running uvicorn separately.
  async rewrites() {
    if (process.env.USE_FASTAPI === "1") {
      return [
        {
          source: "/api/:path*",
          destination: "http://127.0.0.1:8000/api/:path*",
        },
      ];
    }
    return [];
  },
};

export default nextConfig;
