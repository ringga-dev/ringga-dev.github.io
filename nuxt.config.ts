import { resolve } from 'node:path'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  srcDir: 'src/',

  // Modules
  modules: ['@nuxtjs/tailwindcss', '@tresjs/nuxt'],

  // CSS
  css: ['~/assets/css/index.css'],

  // Static Site Generation for GitHub Pages
  ssr: true,
  
  // App configuration
  app: {
    baseURL: process.env.NUXT_APP_BASE_URL || '/',
    buildAssetsDir: '/_nuxt/',
    
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
        { name: 'robots', content: 'index, follow' }
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

  // Components auto-import
  components: [
    { path: '~/components', pathPrefix: false },
    { path: '~/features', pathPrefix: false }
  ],

  // Vite optimization for better performance
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules/vue') || id.includes('node_modules/pinia') || id.includes('vue-router')) {
              return 'vendor-vue'
            }
            if (id.includes('node_modules/three') || id.includes('@tresjs')) {
              return 'vendor-three'
            }
          }
        }
      }
    }
  },

  // Runtime config for environment variables
  runtimeConfig: {
    public: {
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'https://ringgadev.com',
      githubUrl: process.env.NUXT_PUBLIC_GITHUB_URL || '',
      analyticsId: process.env.NUXT_PUBLIC_ANALYTICS_ID || ''
    }
  },

  // Nitro configuration for static generation
  nitro: {
    prerender: {
      failOnError: false,
      routes: ['/']
    },
    output: {
      dir: 'dist'
    }
  },

  // TypeScript strict mode
  typescript: {
    strict: true,
    typeCheck: false
  },

  // Experimental features
  experimental: {
    viewTransition: true,
    payloadExtraction: true
  }
})
