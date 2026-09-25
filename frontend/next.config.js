const API_HOST = process.env.NEXT_PUBLIC_API_HOST || "http://localhost:8000";

const nextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${API_HOST}/api/:path*` }];
  },
};
module.exports = nextConfig;
