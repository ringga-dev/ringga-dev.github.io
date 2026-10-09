import { readdirSync, readFileSync } from 'node:fs'
// eslint-disable-next-line @typescript-eslint/no-duplicate-imports
import { readFileSync as readJsonSync } from 'node:fs'
import { resolve, join } from 'node:path'

// Enumerate semua blog posts supaya di-prerender semua (bukan cuma yang ke-crawl
// dari halaman 1 /blog — sebelumnya post di luar page 1 jadi 404)
const blogDir = resolve(process.cwd(), 'src/data/blog')
const blogFiles = readdirSync(blogDir).filter(f => f.endsWith('.md'))
const blogPostRoutes = blogFiles
  .map(f => `/blog/${f.replace(/\.md$/, '')}`)

// Collect all unique tags for /tag/[tag] prerendering
const tagSet = new Set<string>()
const slugify = (t: string) => t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
for (const f of blogFiles) {
  const raw = readFileSync(join(blogDir, f), 'utf-8')
  const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (!fmMatch) continue
  const tagLine = fmMatch[1].split('\n').find(l => l.trim().startsWith('tags:'))
  if (!tagLine) continue
  const val = tagLine.split(':').slice(1).join(':').trim().replace(/^\[|\]$/g, '')
  val.split(',').forEach(t => {
    const tag = t.trim().replace(/^["']|["']$/g, '')
    if (tag) tagSet.add(tag)
  })
}
const tagRoutes = Array.from(tagSet).map(t => `/tag/${slugify(t)}`)

// News routes (static data in src/data/news.json)
const newsRaw = readJsonSync(resolve(process.cwd(), 'src/data/news.json'), 'utf-8')
const newsSlugs = (JSON.parse(newsRaw).items || []).map((n: any) => `/news/${n.slug}`)
const newsRoutes = ['/news', ...newsSlugs]

// Harus sama dengan BLOG_POSTS_PER_PAGE di src/components/BlogListing.vue
// dan NEWS_PER_PAGE di src/components/NewsListing.vue
//
// PENTING: pakai PATH segment (`/blog/page/2`), bukan query string
// (`/blog?page=2`). GitHub Pages menyajikan file statis, jadi `?page=2`
// selalu menunjuk ke blog/index.html yang sama dan setiap halaman akan
// menampilkan page 1. Path segment di-prerender jadi file terpisah.
const POSTS_PER_PAGE = 9
const blogPageCount = Math.max(1, Math.ceil(blogPostRoutes.length / POSTS_PER_PAGE))
const blogIndexRoutes = [
  '/blog',
  ...Array.from({ length: blogPageCount - 1 }, (_, i) => `/blog/page/${i + 2}`)
]

const NEWS_PER_PAGE = 9
const newsPageCount = Math.max(1, Math.ceil(newsSlugs.length / NEWS_PER_PAGE))
const newsIndexRoutes = [
  '/news',
  ...Array.from({ length: newsPageCount - 1 }, (_, i) => `/news/page/${i + 2}`)
]

// Explicitly register the dynamic tag route so Nitro prerender can resolve it
// regardless of page-dir auto-scan quirks.
const tagPageFile = resolve(process.cwd(), 'src/pages/tags/[tag].vue')
function registerTagRoute(pages: any[]) {
  pages.push({
    name: 'tag-tag',
    path: '/tag/:tag',
    file: tagPageFile
  })
}

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  srcDir: 'src/',

  // Register the dynamic tag route explicitly
  hooks: {
    'pages:extend'(pages) {
      registerTagRoute(pages)
    }
  },

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
        { name: 'theme-color', content: '#F5F0E6' },
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
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap' }
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
      crawlLinks: true,
      failOnError: false,
      routes: ['/', '/sitemap.xml', '/feed.xml', ...blogIndexRoutes, ...blogPostRoutes, ...tagRoutes, ...newsRoutes, ...newsIndexRoutes]
    },
    routeRules: {
      '/tag/**': { prerender: true }
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
