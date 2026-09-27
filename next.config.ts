import type { NextConfig } from "next";

// Fully static export: the whole site is one prerendered page, so it can be hosted anywhere
// (Netlify drag and drop, Netlify Git builds, or Vercel). Security headers live in public/_headers.
const nextConfig: NextConfig = {
  output: "export",
  poweredByHeader: false,
  images: { unoptimized: true },
  trailingSlash: false,
};

export default nextConfig;
