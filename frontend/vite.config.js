import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig } from "vite";
// AOEN frontend dev server. Proxies /api to the FastAPI backend so the browser
// never talks to external services directly and no keys reach the client (§37).
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: { "@": path.resolve(__dirname, "src") },
    },
    server: {
        port: 5173,
        proxy: {
            "/api": {
                target: "http://localhost:8000",
                changeOrigin: true,
            },
        },
    },
});
