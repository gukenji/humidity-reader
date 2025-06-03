import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0", // para que possa ser acessado por outros dispositivos
    port: 5173, // 👈 Garante que bate com o docker-compose
  },
});
