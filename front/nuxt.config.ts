export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  srcDir: "./src/",
  routeRules: {
    "/adsf/**": {
      ssr: false,
    },
  },
  modules: [
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
  ],
  runtimeConfig: {
    public: {
      baseUrl: process.env.API_URL || "http://localhost:8000",
    },
  },
});
