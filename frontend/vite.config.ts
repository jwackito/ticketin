import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub Pages serves this project site under /ticketin/, so production builds
// must use that base. The dev server stays at / for local development.
export default defineConfig(({ command }) => ({
  base: command === "build" ? "/ticketin/" : "/",
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000,
  },
}));
