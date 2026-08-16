import { readdirSync, readFileSync } from 'node:fs'
import { resolve, join } from 'node:path'
import { defineEventHandler } from 'h3'

// Static-safe RSS feed generated at build/prerender time
export default defineEventHandler(() => {
  const blogDir = resolve(process.cwd(), 'src/data/blog')
  const siteUrl = process.env.NUXT_PUBLIC_SITE_URL || 'https://ringgadev.com'
  const siteName = 'Ringga Dev'
  const email = 'ringga.dev@gmail.com'

  interface Post { slug: string; title: string; description: string; date: string; link: string }
  const posts: Post[] = []

  try {
    const files = readdirSync(blogDir).filter(f => f.endsWith('.md'))
    for (const f of files) {
      const raw = readFileSync(join(blogDir, f), 'utf-8')
      const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
      if (!fmMatch) continue
      const fm: Record<string, string> = {}
      fmMatch[1].split('\n').forEach(line => {
        const i = line.indexOf(':')
        if (i === -1) return
        fm[line.slice(0, i).trim()] = line.slice(i + 1).trim().replace(/^["']|["']$/g, '')
      })
      const slug = f.replace('.md', '')
      posts.push({
        slug,
        title: fm.title || slug,
        description: fm.description || '',
        date: fm.date || new Date().toISOString(),
        link: `${siteUrl}/blog/${slug}`
      })
    }
  } catch (e) {
    // no blog dir
  }

  posts.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
  const recent = posts.slice(0, 20)

  const items = recent.map(p => `    <item>\n      <title>${escapeXml(p.title)}</title>\n      <link>${p.link}</link>\n      <guid isPermaLink="true">${p.link}</guid>\n      <description>${escapeXml(p.description)}</description>\n      <pubDate>${new Date(p.date).toUTCString()}</pubDate>\n    </item>`).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n  <channel>\n    <title>${siteName}</title>\n    <link>${siteUrl}</link>\n    <atom:link href="${siteUrl}/feed.xml" rel="self" type="application/rss+xml" />\n    <description>${siteName} — Writings on mobile engineering, web dev, and security.</description>\n    <language>en-us</language>\n    <managingEditor>${email}</managingEditor>\n    <webMaster>${email}</webMaster>\n    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>\n${items}\n  </channel>\n</rss>\n`

  return new Response(xml, {
    headers: { 'content-type': 'application/rss+xml', 'cache-control': 'max-age=3600' }
  })
})

function escapeXml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}
