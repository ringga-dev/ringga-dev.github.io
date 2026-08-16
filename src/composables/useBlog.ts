/**
 * Client-safe blog helpers. Uses import.meta.glob which is valid in Vite/Vue
 * client context (NOT in Nitro server utils). Import from here in pages.
 */

export interface BlogPost {
  slug: string
  path: string
  title: string
  description: string
  date: string
  image: string
  tags: string[]
  author: string
  category: string
}

export function slugifyTag(tag: string): string {
  return tag
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

function parseFrontmatter(raw: string): { meta: Record<string, any>; body: string } {
  const fmRegex = /^---\r?\n([\s\S]*?)\r?\n---/
  const match = raw.match(fmRegex)
  if (!match) return { meta: {}, body: raw }

  const fmText = match[1]
  const body = raw.replace(match[0], '').trim()
  const meta: Record<string, any> = {}

  fmText.split('\n').forEach(line => {
    const parts = line.split(':')
    if (parts.length < 2) return
    const key = parts[0].trim()
    let val = parts.slice(1).join(':').trim()

    const commentIdx = val.lastIndexOf(' #')
    if (commentIdx !== -1) val = val.substring(0, commentIdx).trim()

    if (val.startsWith('"') && val.endsWith('"')) {
      val = val.substring(1, val.length - 1)
    } else if (val.startsWith("'") && val.endsWith("'")) {
      val = val.substring(1, val.length - 1)
    } else if (val.startsWith('[') && val.endsWith(']')) {
      try {
        val = JSON.parse(val.replace(/'/g, '"'))
      } catch (e) {
        val = val.replace(/[\[\]"]/g, '').split(',').map((s: string) => s.trim())
      }
    }
    meta[key] = val
  })

  return { meta, body }
}

export function collectBlogPosts(): BlogPost[] {
  const glob = import.meta.glob('~/data/blog/*.md', { query: '?raw', import: 'default', eager: true }) as Record<string, string>
  return Object.entries(glob).map(([filepath, raw]) => {
    const slug = filepath.split('/').pop()!.replace('.md', '')
    const { meta } = parseFrontmatter(raw)
    return {
      slug,
      path: `/blog/${slug}`,
      title: meta.title || slug,
      description: meta.description || '',
      date: meta.date || '',
      image: meta.image || '',
      tags: Array.isArray(meta.tags) ? meta.tags : [],
      author: meta.author || 'Ringga Dev',
      category: meta.category || 'Engineering'
    }
  }).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
}
