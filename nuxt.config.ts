import { resolve } from 'node:path'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  srcDir: 'src/',
  
  modules: ['@nuxtjs/tailwindcss'],
  
  css: ['~/assets/css/index.css'],
  
  ssr: true,

  components: [
    { path: '~/components', pathPrefix: false },
    { path: '~/features', pathPrefix: false }
  ],

  app: {
    head: {
      htmlAttrs: {
        lang: 'en'
      },
      title: 'Ringga Dev | Professional Multi-Platform Engineer',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Premium Portfolio of Ringga Septia Pribadi - Expert Android & Web Developer with 3+ years experience.' },
        { name: 'theme-color', content: '#00DC82' },
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'Ringga Dev | Full-Stack Developer' },
        { property: 'og:description', content: 'Crafting premium Android & Web applications with performance and aesthetics in mind.' },
        { property: 'og:image', content: '/og-image.png' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:site', content: '@ringga_dev' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap' }
      ]
    },
    pageTransition: { name: 'page', mode: 'out-in' }
  },
})
