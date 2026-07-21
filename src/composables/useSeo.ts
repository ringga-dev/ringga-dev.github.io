/**
 * SEO Helper for Nuxt pages
 * Emerald Zambrut Portfolio
 */

import type { Ref } from 'vue'

interface SeoOptions {
  title?: string
  description?: string
  image?: string
  type?: 'website' | 'article' | 'profile'
  publishedTime?: string
  modifiedTime?: string
  tags?: string[]
}

export function usePageSeo(options: SeoOptions = {}) {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl || 'https://ringgadev.com'
  
  const defaultTitle = 'Ringga Dev | Professional Multi-Platform Engineer'
  const defaultDescription = 'Premium Portfolio of Ringga Septia Pribadi - Expert Android & Web Developer with 3+ years experience.'
  const defaultImage = '/og-image.png'
  
  const title = options.title ? `${options.title} | Ringga Dev` : defaultTitle
  const description = options.description || defaultDescription
  const image = options.image || defaultImage
  const imageUrl = image.startsWith('http') ? image : `${siteUrl}${image}`
  
  const seoMeta = {
    title,
    meta: [
      // Basic Meta Tags
      { name: 'description', content: description },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'theme-color', content: '#00DC82' },
      
      // Open Graph / Facebook
      { property: 'og:type', content: options.type || 'website' },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: imageUrl },
      { property: 'og:url', content: siteUrl },
      { property: 'og:site_name', content: 'Ringga Dev' },
      
      // Twitter
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: imageUrl },
      { name: 'twitter:site', content: '@ringga_dev' },
      { name: 'twitter:creator', content: '@ringga_dev' },
      
      // Additional SEO
      { name: 'robots', content: 'index, follow' },
      { name: 'author', content: 'Ringga Septia Pribadi' },
      { name: 'keywords', content: 'Android Developer, Web Developer, Kotlin, Nuxt, Vue, Full Stack, Portfolio, Mobile Developer, Frontend, Backend' }
    ],
    link: [
      { rel: 'canonical', href: siteUrl }
    ]
  }
  
  // Add article-specific meta if type is article
  if (options.type === 'article') {
    if (options.publishedTime) {
      seoMeta.meta.push({ property: 'article:published_time', content: options.publishedTime })
    }
    if (options.modifiedTime) {
      seoMeta.meta.push({ property: 'article:modified_time', content: options.modifiedTime })
    }
    if (options.tags && options.tags.length > 0) {
      options.tags.forEach(tag => {
        seoMeta.meta.push({ property: 'article:tag', content: tag })
      })
    }
  }
  
  useHead(seoMeta)
  
  return seoMeta
}

/**
 * Generate structured data for JSON-LD
 */
export function useStructuredData(data: Record<string, any>) {
  useHead({
    script: [
      {
        type: 'application/ld+json',
        children: JSON.stringify(data)
      }
    ]
  })
}

/**
 * Person schema for about page
 */
export function usePersonSchema(person: {
  name: string
  jobTitle: string
  url: string
  sameAs: string[]
  image: string
}) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: person.name,
    jobTitle: person.jobTitle,
    url: person.url,
    image: person.image,
    sameAs: person.sameAs
  }
  
  useStructuredData(schema)
}

/**
 * Article schema for blog posts
 */
export function useArticleSchema(article: {
  headline: string
  description: string
  image: string
  datePublished: string
  dateModified: string
  author: {
    name: string
    url: string
  }
  url: string
}) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.headline,
    description: article.description,
    image: article.image,
    datePublished: article.datePublished,
    dateModified: article.dateModified,
    author: {
      '@type': 'Person',
      name: article.author.name,
      url: article.author.url
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': article.url
    }
  }
  
  useStructuredData(schema)
}
