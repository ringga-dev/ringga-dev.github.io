import { readdirSync, readFileSync } from 'node:fs'
import { resolve, join } from 'node:path'
import { defineEventHandler } from 'h3'

// Static-safe: reads blog markdown at build/prerender time and emits sitemap.xml
export default defineEventHandler(() => {
  const blogDir = resolve(process.cwd(), 'src/data/blog')
  const siteUrl = process.env.NUXT_PUBLIC_SITE_URL || 'https://ringgadev.com'

  // Static page routes
  const staticRoutes = ['', '/blog', '/projects', '/about', '/gallery', '/contact']

  // Parse blog posts + tags
  const posts: Array<{ path: string; date: string }> = []
  const tagSet = new Set<string>()
  try {
    const files = readdirSync(blogDir).filter(f => f.endsWith('.md'))
    for (const f of files) {
      const raw = readFileSync(join(blogDir, f), 'utf-8')
      const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
      const slug = f.replace('.md', '')
      posts.push({ path: `/blog/${slug}`, date: '' })
      if (fmMatch) {
        const tagLine = fmMatch[1].split('\n').find(l => l.trim().startsWith('tags:'))
        if (tagLine) {
          const val = tagLine.split(':').slice(1).join(':').trim().replace(/^\[|\]$/g, '')
          val.split(',').forEach(t => {
            const tag = t.trim().replace(/^["']|["']$/g, '')
            if (tag) tagSet.add(tag.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''))
          })
        }
        const line = fmMatch[1].split('\n').find(l => l.trim().startsWith('date:'))
        if (line) posts[posts.length - 1].date = line.split(':').slice(1).join(':').trim().replace(/"/g, '')
      }
    }
  } catch (e) {
    // no blog dir — skip
  }

  const tagRoutes = Array.from(tagSet).map(slug => ({ path: `/tag/${slug}`, date: '' }))

  const allRoutes = [
    ...staticRoutes.map(p => ({ path: p || '/', date: '' })),
    ...posts,
    ...tagRoutes
  ]

  const urls = allRoutes.map(r => {
    const loc = `${siteUrl}${r.path}`
    const lastmod = r.date
      ? `    <lastmod>${r.date}</lastmod>\n`
      : ''
    return `  <url>\n    <loc>${loc}</loc>\n${lastmod}    <changefreq>weekly</changefreq>\n    <priority>${r.path === '/' ? '1.0' : '0.8'}</priority>\n  </url>`
  }).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`

  return new Response(xml, {
    headers: { 'content-type': 'application/xml', 'cache-control': 'max-age=3600' }
  })
})
