// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/index.css'],
  app: {
    head: {
      title: 'Ringga Dev | Portfolio',
      meta: [
        { name: 'description', content: 'Premium Portfolio of Ringga Dev' }
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap' }
      ]
    }
  },
  future: {
    compatibilityVersion: 4,
  }
})
