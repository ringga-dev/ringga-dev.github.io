<template>
  <div class="min-h-screen relative bg-surface text-main pb-24 transition-colors duration-500">
    <!-- Reading Progress Bar -->
    <div 
      class="fixed top-0 left-0 h-1 bg-brand z-[100] origin-left transition-transform duration-75"
      :style="`transform: scaleX(${scrollProgress}); width: 100%;`"
      aria-hidden="true"
    ></div>

    <div v-if="page" class="w-full">
      <!-- Immersive Header Banner Section -->
      <div class="relative h-[65vh] w-full overflow-hidden flex items-end">
        <!-- Background Cover Image -->
        <div class="absolute inset-0 z-0">
          <img 
            v-if="page.image" 
            :src="page.image" 
            :alt="page.title" 
            class="w-full h-full object-cover scale-105"
          />
          <div v-else class="w-full h-full bg-surface-elevated flex items-center justify-center">
            <BookOpen class="w-20 h-20 text-muted/30" />
          </div>
          <!-- Cinema Overlay Gradients -->
          <div class="absolute inset-0 bg-gradient-to-t from-surface via-surface/60 to-surface/80 z-10"></div>
          <div class="absolute inset-0 bg-surface/30 z-0"></div>
        </div>

        <!-- Float Nav Controls & Metadata -->
        <div class="max-w-7xl mx-auto w-full px-6 pb-12 relative z-20 animate-reveal">
          <!-- Back Link -->
          <NuxtLink 
            to="/blog" 
            class="inline-flex items-center gap-2 text-xs font-black uppercase tracking-widest text-brand hover:text-brand-light transition-colors mb-8 font-mono bg-surface-card/40 border border-brand/20 backdrop-blur-md px-4 py-2.5 rounded-xl hover:border-brand/40"
          >
            <ArrowLeft class="w-4 h-4" /> Back to Blog
          </NuxtLink>

          <div class="flex flex-wrap items-center gap-3 mb-6">
            <span class="text-[9px] px-2.5 py-1 rounded-md bg-brand/10 border border-brand/25 text-brand font-black uppercase tracking-wider font-mono">
              {{ page.category }}
            </span>
            <span class="text-xs text-muted font-mono flex items-center gap-1.5 ml-2">
              <Calendar class="w-3.5 h-3.5 text-brand/70" />
              {{ formatDate(page.date) }}
            </span>
            <span class="text-xs text-muted font-mono flex items-center gap-1.5 ml-2">
              <Clock class="w-3.5 h-3.5 text-brand/70" />
              {{ readingTime }} min read
            </span>
          </div>

          <!-- Tags -->
          <div v-if="page.tags && page.tags.length" class="flex flex-wrap gap-2 mb-6">
            <NuxtLink
              v-for="tag in page.tags"
              :key="tag"
              :to="`/tag/${slugifyTag(tag)}`"
              class="text-[10px] px-2.5 py-1 rounded-md bg-surface-card/60 border border-border text-muted hover:text-brand hover:border-brand/40 font-semibold transition-colors"
            >
              #{{ tag }}
            </NuxtLink>
          </div>

          <h1 class="text-3xl sm:text-5xl md:text-6xl font-heading font-black text-main leading-tight mb-4 max-w-4xl tracking-tight">
            {{ page.title }}
          </h1>

          <p class="text-base sm:text-lg md:text-xl text-muted font-medium max-w-3xl leading-relaxed">
            {{ page.description }}
          </p>
        </div>
      </div>

      <!-- MAIN CONTENT SYSTEM -->
      <div class="max-w-7xl mx-auto px-6 pt-12 relative z-20">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          <!-- ARTICLE BODY COLUMN (Col Span 8) -->
          <div class="lg:col-span-8 space-y-8 animate-reveal" style="animation-delay: 100ms">
            <!-- Article Wrapper with Event Delegation for copying code -->
            <div @click="handleArticleClick">
              <article 
                class="prose prose-brand max-w-none prose-h2:text-main prose-h3:text-main prose-p:leading-relaxed"
                v-html="renderedContent"
              ></article>
            </div>
          </div>

          <!-- STICKY SIDEBAR COLUMN (Col Span 4) -->
          <div class="lg:col-span-4 space-y-8 lg:sticky lg:top-24 animate-reveal" style="animation-delay: 200ms">
            
            <!-- Table of Contents Widget -->
            <div v-if="toc.length" class="glass-card p-6 md:p-8 rounded-[2rem] bg-surface-card border border-border">
              <h3 class="text-xs font-black uppercase tracking-widest text-muted border-b border-border/60 pb-3.5 mb-5 font-mono">
                On This Page
              </h3>
              <nav class="space-y-3 max-h-[40vh] overflow-y-auto pr-2">
                <a 
                  v-for="item in toc" 
                  :key="item.id" 
                  :href="`#${item.id}`"
                  class="block text-xs font-semibold leading-relaxed transition-all duration-300 hover:text-brand"
                  :class="[
                    item.level === 3 ? 'pl-4 text-muted/80' : 'text-muted',
                    activeHeading === item.id ? 'text-brand! font-black border-l-2 border-brand pl-2' : ''
                  ]"
                >
                  {{ item.text }}
                </a>
              </nav>
            </div>

            <!-- Author & Share Info -->
            <div class="glass-card p-6 md:p-8 rounded-[2rem] bg-surface-card border border-border space-y-6">
              <!-- Author Card -->
              <div>
                <h3 class="text-[10px] font-black uppercase tracking-widest text-muted mb-4 font-mono">Author</h3>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-brand/10 border border-brand/30 flex items-center justify-center text-brand font-black font-mono text-sm shadow-inner">
                    {{ page.author.charAt(0) }}
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-main leading-tight">{{ page.author }}</h4>
                    <p class="text-[10px] text-muted font-bold tracking-wide mt-0.5">Software Engineer</p>
                  </div>
                </div>
              </div>

              <!-- Share Buttons -->
              <div class="border-t border-border/50 pt-5">
                <h3 class="text-[10px] font-black uppercase tracking-widest text-muted mb-4 font-mono">Share Article</h3>
                <div class="flex flex-wrap gap-2.5">
                  <!-- Twitter/X -->
                  <a 
                    :href="twitterShareUrl" 
                    target="_blank"
                    class="w-9 h-9 rounded-xl bg-surface-elevated/40 hover:bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 transition-all duration-300 active:scale-90"
                    title="Share on Twitter / X"
                  >
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                  </a>
                  <!-- LinkedIn -->
                  <a 
                    :href="linkedinShareUrl" 
                    target="_blank"
                    class="w-9 h-9 rounded-xl bg-surface-elevated/40 hover:bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 transition-all duration-300 active:scale-90"
                    title="Share on LinkedIn"
                  >
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                  </a>
                  <!-- WhatsApp -->
                  <a 
                    :href="whatsappShareUrl" 
                    target="_blank"
                    class="w-9 h-9 rounded-xl bg-surface-elevated/40 hover:bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 transition-all duration-300 active:scale-90"
                    title="Share on WhatsApp"
                  >
                    <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.724-1.457L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.42 9.863-9.864.001-2.63-1.023-5.101-2.885-6.963C16.588 1.917 14.12 .891 11.5 .891 6.063.891 1.639 5.313 1.636 10.75c-.001 1.764.467 3.491 1.357 5.011l-.994 3.634 3.72-.975z"/></svg>
                  </a>
                  <!-- Copy Link -->
                  <button 
                    @click="copyLink"
                    class="w-9 h-9 rounded-xl bg-surface-elevated/40 hover:bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 transition-all duration-300 active:scale-90 cursor-pointer"
                    title="Copy Article URL"
                  >
                    <Check v-if="copiedLink" class="w-4 h-4 text-brand animate-pulse" />
                    <Link2 v-else class="w-4 h-4" />
                  </button>
                </div>
                <!-- Copy link confirmation toast -->
                <transition 
                  enter-active-class="transition duration-300 ease-out"
                  enter-from-class="opacity-0 translate-y-1"
                  enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-250 ease-in"
                  leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 translate-y-1"
                >
                  <div v-if="copiedLink" class="text-[10px] text-brand font-bold mt-2 bg-brand/5 border border-brand/10 p-2.5 rounded-xl flex items-center gap-1.5">
                    <Check class="w-3.5 h-3.5 shrink-0" /> Link copied to clipboard!
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </div>

        <!-- RECOMMENDED POSTS FOOTER SECTION -->
        <div v-if="recommendedPosts.length" class="mt-24 pt-16 border-t border-border/60 animate-reveal" style="animation-delay: 300ms">
          <h2 class="text-xs font-black uppercase tracking-widest text-muted mb-8 font-mono">Recommended Articles</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <NuxtLink 
              v-for="post in recommendedPosts" 
              :key="post.slug" 
              :to="post.path"
              class="glass-card overflow-hidden group hover:border-brand/40 border border-border/80 rounded-3xl grid grid-cols-1 sm:grid-cols-12 gap-0 sm:gap-6 p-4 hover:shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1 block"
            >
              <!-- Image (Col Span 5) -->
              <div class="sm:col-span-5 relative aspect-[16/10] sm:aspect-auto rounded-2xl overflow-hidden min-h-[140px]">
                <img 
                  v-if="post.image" 
                  :src="post.image" 
                  :alt="post.title"
                  class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                <div v-else class="absolute inset-0 bg-surface-elevated flex items-center justify-center">
                  <BookOpen class="w-10 h-10 text-muted/20" />
                </div>
              </div>

              <!-- Content (Col Span 7) -->
              <div class="sm:col-span-7 p-4 flex flex-col justify-center">
                <div class="flex items-center gap-2.5 mb-3 text-[10px] text-muted font-mono">
                  <span class="px-2 py-0.5 rounded bg-brand/10 border border-brand/20 text-brand font-black uppercase tracking-wider text-[8px]">{{ post.category }}</span>
                  <span>{{ formatDate(post.date) }}</span>
                </div>
                
                <h3 class="text-lg font-heading font-black text-main mb-2 leading-tight group-hover:text-brand transition-colors duration-300 line-clamp-2">
                  {{ post.title }}
                </h3>
                
                <p class="text-muted text-xs leading-relaxed font-semibold mb-4 line-clamp-2">
                  {{ post.description }}
                </p>

                <div class="text-brand text-xs font-black uppercase tracking-widest flex items-center gap-0.5 mt-auto group-hover:translate-x-1 transition-transform duration-300">
                  Read Article
                  <ArrowRight class="w-3.5 h-3.5" />
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ArrowLeft, Calendar, Clock, BookOpen, Link2, Check } from 'lucide-vue-next'
import { useRoute } from '#imports'
import globalData from '~/data/global.json'
import { slugifyTag } from '~/utils'

const route = useRoute()
const slug = route.params.slug

// Load all markdown files synchronously at build-time
const globbedPosts = import.meta.glob('../../data/blog/*.md', { query: '?raw', import: 'default', eager: true })

const page = computed(() => {
  // Find the file matching the slug
  const filepath = Object.keys(globbedPosts).find(path => path.endsWith(`${slug}.md`))
  if (!filepath) return null
  
  const rawContent = globbedPosts[filepath]
  
  // Parse frontmatter
  const fmRegex = /^---\r?\n([\s\S]*?)\r?\n---/
  const match = rawContent.match(fmRegex)
  let meta = {}
  let body = rawContent
  
  if (match) {
    const fmText = match[1]
    body = rawContent.replace(match[0], '').trim()
    
    fmText.split('\n').forEach(line => {
      const parts = line.split(':')
      if (parts.length >= 2) {
        const key = parts[0].trim()
        let val = parts.slice(1).join(':').trim()
        
        // Strip trailing comment if exists
        const commentIdx = val.lastIndexOf(' #')
        if (commentIdx !== -1) {
          val = val.substring(0, commentIdx).trim()
        }
        
        if (val.startsWith('"') && val.endsWith('"')) {
          val = val.substring(1, val.length - 1)
        } else if (val.startsWith("'") && val.endsWith("'")) {
          val = val.substring(1, val.length - 1)
        } else if (val.startsWith('[') && val.endsWith(']')) {
          try {
            val = JSON.parse(val.replace(/'/g, '"'))
          } catch (e) {
            val = val.replace(/[\[\]"]/g, '').split(',').map(s => s.trim())
          }
        }
        meta[key] = val
      }
    })
  }
  
  return {
    slug,
    title: meta.title || slug,
    description: meta.description || '',
    date: meta.date || '',
    image: meta.image || '',
    tags: meta.tags || [],
    author: meta.author || 'Ringga Dev',
    category: meta.category || 'Engineering',
    body
  }
})

// Scroll Progress Tracker
const scrollProgress = ref(0)
const updateScrollProgress = () => {
  if (!import.meta.client) return
  const totalHeight = document.documentElement.scrollHeight - window.innerHeight
  if (totalHeight === 0) {
    scrollProgress.value = 0
  } else {
    scrollProgress.value = window.scrollY / totalHeight
  }
}

// Share Links
const encodedUrl = computed(() => {
  if (!import.meta.client) return ''
  return encodeURIComponent(window.location.href)
})
const encodedTitle = computed(() => {
  return page.value ? encodeURIComponent(page.value.title) : ''
})
const twitterShareUrl = computed(() => `https://twitter.com/intent/tweet?url=${encodedUrl.value}&text=${encodedTitle.value}`)
const linkedinShareUrl = computed(() => `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl.value}`)
const whatsappShareUrl = computed(() => `https://api.whatsapp.com/send?text=${encodedTitle.value}%20${encodedUrl.value}`)

// Copy Link Handler
const copiedLink = ref(false)
const copyLink = () => {
  if (!import.meta.client) return
  navigator.clipboard.writeText(window.location.href)
  copiedLink.value = true
  setTimeout(() => {
    copiedLink.value = false
  }, 2500)
}

// Copy Code Block Handler (Delegation)
const handleArticleClick = (e) => {
  const copyBtn = e.target.closest('.copy-code-btn')
  if (copyBtn) {
    const codeWrapper = copyBtn.closest('.code-block-wrapper')
    const codeEl = codeWrapper ? codeWrapper.querySelector('code') : null
    
    if (codeEl) {
      navigator.clipboard.writeText(codeEl.innerText)
      
      const btnSpan = copyBtn.querySelector('span')
      const originalText = btnSpan.innerText
      btnSpan.innerText = 'Copied!'
      copyBtn.classList.add('text-brand')
      
      setTimeout(() => {
        btnSpan.innerText = originalText
        copyBtn.classList.remove('text-brand')
      }, 2000)
    }
  }
}

// Reading Time & Dynamic TOC
const readingTime = computed(() => {
  if (!page.value || !page.value.body) return 0
  const words = page.value.body.split(/\s+/).length
  return Math.ceil(words / 200)
})

const toc = computed(() => {
  if (!page.value || !page.value.body) return []
  
  const headings = []
  const lines = page.value.body.split('\n')
  
  lines.forEach(line => {
    const h2Match = line.match(/^##\s+(.*)$/)
    const h3Match = line.match(/^###\s+(.*)$/)
    
    if (h2Match) {
      const text = h2Match[1].trim()
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')
      headings.push({ level: 2, text, id })
    } else if (h3Match) {
      const text = h3Match[1].trim()
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')
      headings.push({ level: 3, text, id })
    }
  })
  
  return headings
})

// Highlight Active TOC Item on Scroll
const activeHeading = ref('')
let observer = null

// Recommended posts
const recommendedPosts = computed(() => {
  if (!page.value) return []
  const others = Object.entries(globbedPosts).map(([filepath, rawContent]) => {
    const otherSlug = filepath.split('/').pop().replace('.md', '')
    if (otherSlug === slug) return null
    
    // Parse basic frontmatter
    const fmRegex = /^---\r?\n([\s\S]*?)\r?\n---/
    const match = rawContent.match(fmRegex)
    let meta = {}
    if (match) {
      const fmText = match[1]
      fmText.split('\n').forEach(line => {
        const parts = line.split(':')
        if (parts.length >= 2) {
          const key = parts[0].trim()
          let val = parts.slice(1).join(':').trim()
          
          const commentIdx = val.lastIndexOf(' #')
          if (commentIdx !== -1) {
            val = val.substring(0, commentIdx).trim()
          }
          
          if (val.startsWith('"') && val.endsWith('"') || val.startsWith("'") && val.endsWith("'")) {
            val = val.substring(1, val.length - 1)
          }
          meta[key] = val
        }
      })
    }
    return {
      slug: otherSlug,
      path: `/blog/${otherSlug}`,
      title: meta.title || otherSlug,
      description: meta.description || '',
      date: meta.date || '',
      image: meta.image || '',
      category: meta.category || 'Engineering'
    }
  }).filter(Boolean)
  
  return others.slice(0, 2)
})

const renderedContent = computed(() => {
  if (!page.value || !page.value.body) return ''
  
  let html = page.value.body
  
  // Code blocks diekstrak dulu (placeholder) — isi kode tidak diproses regex lain
  // dan di-escape saat restore supaya tidak bisa mengeksekusi script
  const codeBlocks = []
  html = html.replace(/```(\w+)?([\s\S]*?)```/gim, (match, lang, code) => {
    codeBlocks.push({ lang: lang || '', code: code.trim() })
    return `\n@@CODEBLOCK_${codeBlocks.length - 1}@@\n`
  })
  
  // Headers with IDs
  html = html.replace(/^## (.*$)/gim, (match, title) => {
    const cleanTitle = title.trim()
    const id = cleanTitle.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')
    return `<h2 id="${id}" class="text-2xl font-bold mt-12 mb-6 border-b border-border pb-2 scroll-mt-24 text-main font-heading">${cleanTitle}</h2>`
  })
  
  html = html.replace(/^### (.*$)/gim, (match, title) => {
    const cleanTitle = title.trim()
    const id = cleanTitle.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-')
    return `<h3 id="${id}" class="text-xl font-bold mt-8 mb-4 scroll-mt-24 text-main font-heading">${cleanTitle}</h3>`
  })
  
  html = html.replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mt-12 mb-8 text-main font-heading">$1</h1>')
  
  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, '<blockquote class="border-l-4 border-brand pl-6 italic my-6 text-muted font-medium bg-brand/5 py-4 pr-4 rounded-r-xl border-t border-b border-r border-brand/10">$1</blockquote>')
  
  // Lists
  html = html.replace(/^\* (.*$)/gim, '<li class="ml-6 list-disc my-2 text-muted font-medium">$1</li>')
  html = html.replace(/^\- (.*$)/gim, '<li class="ml-6 list-disc my-2 text-muted font-medium">$1</li>')
  html = html.replace(/^\d+\. (.*$)/gim, '<li class="ml-6 list-decimal my-2 text-muted font-medium">$1</li>')
  
  // Bold & Italic
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-black text-main">$1</strong>')
  html = html.replace(/\*(.*?)\*/g, '<em class="italic text-muted">$1</em>')
  
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="bg-surface-elevated px-2 py-0.5 rounded text-sm border border-border font-mono text-brand font-bold">$1</code>')

  // Tables (GFM markdown tables -> HTML tables)
  html = html.replace(/^(\|[^\n]+\|)\n(\|[\-\t :|]+)\n((?:\|[^\n]+\|\n)*\|[^\n]+\|)/gm, (match, header, sep, body) => {
    const parseRow = (row) => row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim())
    const thead = parseRow(header).map(h => `<th>${h}</th>`).join('')
    const rows = body.trim().split('\n').map(row => `<tr>${parseRow(row).map(c => `<td>${c}</td>`).join('')}</tr>`).join('')
    return `<div class="overflow-x-auto my-8"><table class="w-full text-sm border-collapse"><thead><tr>${thead}</tr></thead><tbody>${rows}</tbody></table></div>`
  })

  // Paragraphs
  const paragraphs = html.split(/\n\s*\n/)
  html = paragraphs.map(p => {
    p = p.trim()
    if (!p) return ''
    if (p.startsWith('<h') || p.startsWith('<div') || p.startsWith('<pre') || p.startsWith('<blockquote') || p.startsWith('<li') || p.startsWith('@@CODEBLOCK_')) return p
    return `<p class="my-6 leading-relaxed text-muted font-medium text-base md:text-lg">${p}</p>`
  }).join('\n')

  // Sanitize — batasi eksekusi script dari konten markdown
  html = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<script[^>]*\/?>/gi, '')
    .replace(/<\/?(iframe|object|embed|link|style|meta|base|form|input|button|textarea|select|option|frame|frameset|applet|svg|math)[^>]*>/gi, '')
    .replace(/\son\w+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '')
    .replace(/(href|src|xlink:href)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, (m, attr, val) => {
      const v = val.replace(/^["']|["']$/g, '')
      return /^\s*javascript:/i.test(v) ? `${attr}="#"` : m
    })

  // Restore code blocks (HTML-escaped — isi kode tidak bisa dieksekusi)
  html = html.replace(/@@CODEBLOCK_(\d+)@@/g, (match, idx) => {
    const { lang, code } = codeBlocks[+idx] || { lang: '', code: '' }
    const displayLang = lang ? lang.toUpperCase() : 'CODE'
    const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
    return `
      <div class="code-block-wrapper relative group/code bg-surface-elevated/40 border border-border rounded-2xl my-8 overflow-hidden font-mono text-sm shadow-xl">
        <div class="flex items-center justify-between px-6 py-3 bg-surface-elevated border-b border-border/80 text-[10px] font-black text-muted uppercase tracking-widest">
          <span>${displayLang}</span>
          <button class="copy-code-btn hover:text-brand transition-colors flex items-center gap-1.5 opacity-60 hover:opacity-100 cursor-pointer text-[10px] font-black uppercase tracking-wider">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            <span>Copy Code</span>
          </button>
        </div>
        <pre class="p-6 overflow-auto text-muted max-h-[500px]"><code>${escaped}</code></pre>
      </div>
    `
  })

  return html
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

onMounted(() => {
  if (import.meta.client) {
    window.addEventListener('scroll', updateScrollProgress)
    
    // Setup IntersectionObserver for active TOC highlight
    const headingEls = document.querySelectorAll('h2[id], h3[id]')
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          activeHeading.value = entry.target.id
        }
      })
    }, { rootMargin: '-15% 0px -65% 0px' })
    
    headingEls.forEach(el => observer.observe(el))
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    window.removeEventListener('scroll', updateScrollProgress)
    if (observer) {
      observer.disconnect()
    }
  }
})
</script>

<style scoped>
/* Specific styling rules to override default prose values where needed */
:deep(article h2) {
  @apply scroll-mt-24;
}
:deep(article h3) {
  @apply scroll-mt-24;
}
:deep(article a) {
  @apply text-brand hover:text-brand-light underline transition-colors duration-300 font-bold;
}
</style>
