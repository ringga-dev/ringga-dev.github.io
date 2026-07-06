<template>
  <div class="min-h-screen pt-28 pb-20 relative overflow-hidden bg-surface">
    <!-- Immersive Background Orbs -->
    <div class="absolute top-[10%] left-[-10%] w-[30vw] h-[30vw] rounded-full blur-[120px] bg-brand/5 pointer-events-none"></div>
    <div class="absolute bottom-[20%] right-[-10%] w-[35vw] h-[35vw] rounded-full blur-[150px] bg-brand-light/5 pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <!-- Title & Header -->
      <div class="text-center mb-16 animate-reveal">
        <div class="inline-block px-3.5 py-1 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-mono mb-4 uppercase tracking-widest">
          Knowledge Base
        </div>
        <h1 class="text-4xl md:text-6xl font-heading font-black tracking-tight leading-none mb-6">
          Writings & <span class="text-gradient">Thoughts</span>
        </h1>
        <p class="text-text-muted max-w-2xl mx-auto text-base md:text-lg font-medium leading-relaxed">
          Exploring advanced mobile engineering, clean architecture, cross-platform systems, and high-performance web development.
        </p>
      </div>

      <!-- Controls Panel (Search & Category Filters) -->
      <div class="glass-card p-4 rounded-3xl mb-12 border border-border-color shadow-xl flex flex-col md:flex-row gap-4 items-center justify-between animate-reveal" style="animation-delay: 100ms">
        <!-- Search input -->
        <div class="relative w-full md:w-80 group">
          <Search class="absolute left-4 top-3.5 w-4 h-4 text-text-muted group-focus-within:text-brand transition-colors" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search articles, tags..." 
            class="w-full pl-11 pr-4 py-3 bg-surface-elevated/40 hover:bg-surface-elevated/60 focus:bg-surface-elevated border border-border-color focus:border-brand/50 rounded-2xl text-sm font-semibold placeholder:text-text-muted/60 text-text-main outline-none transition-all duration-300"
          />
          <button 
            v-if="searchQuery" 
            @click="searchQuery = ''" 
            class="absolute right-4 top-3.5 text-text-muted hover:text-brand transition-colors"
          >
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Categories horizontal list -->
        <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="selectedCategory = cat"
            class="px-4 py-2.5 rounded-xl text-xs font-black uppercase tracking-wider whitespace-nowrap transition-all duration-300 cursor-pointer active:scale-95 border"
            :class="selectedCategory === cat 
              ? 'bg-brand text-slate-950 border-brand shadow-lg shadow-brand/10' 
              : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border-color text-text-muted hover:text-text-main hover:border-brand/20'"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- FEATURED POST (Shown only when not filtering/searching) -->
      <div v-if="featuredPost" class="mb-16 animate-reveal" style="animation-delay: 200ms">
        <h2 class="text-xs font-black uppercase tracking-widest text-text-muted mb-4 font-mono">Featured Article</h2>
        <NuxtLink 
          :to="featuredPost.path"
          class="glass-card overflow-hidden group border border-border-color/80 rounded-[2.5rem] grid grid-cols-1 lg:grid-cols-12 gap-0 lg:gap-8 hover:border-brand/40 shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1 block"
        >
          <!-- Cover -->
          <div class="lg:col-span-7 relative aspect-video lg:aspect-auto min-h-[300px] overflow-hidden">
            <img 
              v-if="featuredPost.image" 
              :src="featuredPost.image" 
              :alt="featuredPost.title"
              class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div v-else class="absolute inset-0 bg-surface-elevated flex items-center justify-center">
              <BookOpen class="w-16 h-16 text-text-muted/30" />
            </div>
            <!-- Gradient Overlay -->
            <div class="absolute inset-0 bg-gradient-to-t lg:bg-gradient-to-r from-surface to-transparent opacity-80 lg:opacity-40"></div>
          </div>

          <!-- Content -->
          <div class="lg:col-span-5 p-8 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-6 flex-wrap">
              <span class="text-[9px] px-2.5 py-1 rounded-lg bg-brand/10 border border-brand/25 text-brand font-black uppercase tracking-wider font-mono">
                {{ featuredPost.category }}
              </span>
              <span class="text-xs text-text-muted font-mono flex items-center gap-1.5">
                <Calendar class="w-3.5 h-3.5 text-brand/70" />
                {{ formatDate(featuredPost.date) }}
              </span>
              <span class="text-xs text-text-muted font-mono flex items-center gap-1.5">
                <Clock class="w-3.5 h-3.5 text-brand/70" />
                {{ featuredPost.readTime }} min read
              </span>
            </div>

            <h3 class="text-2xl md:text-3xl lg:text-4xl font-heading font-black text-text-main mb-4 leading-tight group-hover:text-brand transition-colors duration-300">
              {{ featuredPost.title }}
            </h3>
            
            <p class="text-text-muted font-medium text-base mb-8 leading-relaxed line-clamp-3">
              {{ featuredPost.description }}
            </p>

            <div class="flex items-center justify-between border-t border-border-color/60 pt-6 mt-auto">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-brand/10 border border-brand/30 flex items-center justify-center text-brand font-black font-mono text-xs shadow-inner">
                  {{ featuredPost.author.charAt(0) }}
                </div>
                <span class="text-xs font-bold text-text-main tracking-wide">{{ featuredPost.author }}</span>
              </div>

              <div class="flex items-center text-brand text-xs font-black uppercase tracking-widest gap-1 group-hover:translate-x-1.5 transition-transform duration-300">
                Read Article
                <ArrowRight class="w-4 h-4" />
              </div>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- ARTICLES GRID -->
      <div v-if="filteredPosts.length" class="space-y-6">
        <h2 v-if="featuredPost" class="text-xs font-black uppercase tracking-widest text-text-muted mb-4 font-mono">All Articles</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <NuxtLink 
            v-for="(post, index) in gridPosts" 
            :key="post.slug" 
            :to="post.path"
            class="glass-card overflow-hidden group hover:border-brand/40 border border-border-color/80 rounded-[2.2rem] flex flex-col h-full hover:shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1.5 animate-reveal"
            :style="`animation-delay: ${150 + (index * 50)}ms`"
          >
            <!-- Card Image -->
            <div class="relative h-56 w-full overflow-hidden border-b border-border-color/40">
              <img 
                v-if="post.image" 
                :src="post.image" 
                :alt="post.title"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div v-else class="w-full h-full bg-surface-elevated flex items-center justify-center">
                <BookOpen class="w-12 h-12 text-text-muted/20" />
              </div>
              <div class="absolute inset-0 bg-gradient-to-t from-surface-card to-transparent opacity-40"></div>
              
              <!-- Floating Badge -->
              <span class="absolute top-4 left-4 text-[8px] px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-md border border-white/10 text-brand font-black uppercase tracking-widest">
                {{ post.category }}
              </span>
            </div>

            <!-- Card Content -->
            <div class="p-6 md:p-8 flex flex-col flex-grow">
              <div class="flex items-center gap-3 text-[11px] text-text-muted font-mono mb-4">
                <span class="flex items-center gap-1">
                  <Calendar class="w-3.5 h-3.5 text-brand/70" />
                  {{ formatDate(post.date) }}
                </span>
                <span class="w-1 h-1 rounded-full bg-border-color"></span>
                <span class="flex items-center gap-1">
                  <Clock class="w-3.5 h-3.5 text-brand/70" />
                  {{ post.readTime }} min
                </span>
              </div>
              
              <h3 class="text-xl font-heading font-black text-text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-300 line-clamp-2">
                {{ post.title }}
              </h3>
              
              <p class="text-text-muted text-sm leading-relaxed font-semibold mb-6 line-clamp-3">
                {{ post.description }}
              </p>
              
              <!-- Footer info -->
              <div class="mt-auto pt-5 border-t border-border-color/40 flex items-center justify-between">
                <span class="text-xs font-bold text-text-muted flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-surface-elevated flex items-center justify-center text-[10px] text-brand border border-border-color font-mono">{{ post.author.charAt(0) }}</span>
                  {{ post.author }}
                </span>
                
                <span class="text-brand text-xs font-black uppercase tracking-wider flex items-center gap-0.5 group-hover:translate-x-1 transition-transform duration-300">
                  Read
                  <ArrowRight class="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- PAGINATION -->
      <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-10 animate-reveal" style="animation-delay: 400ms">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="px-4 py-2.5 rounded-xl text-sm font-black uppercase tracking-wider transition-all duration-300 cursor-pointer active:scale-95 border disabled:opacity-50 disabled:cursor-not-allowed"
          :class="currentPage === 1 ? 'bg-surface-elevated/40 border-border-color text-text-muted' : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border-color text-text-muted hover:text-text-main hover:border-brand/20'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide w-4 h-4 lucide-chevron-left"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        
        <div class="flex items-center gap-1">
          <button 
            v-for="page in visiblePages" 
            :key="page"
            @click="currentPage = page"
            class="w-10 h-10 rounded-xl text-sm font-black transition-all duration-300 cursor-pointer active:scale-95 border"
            :class="currentPage === page ? 'bg-brand text-slate-950 border-brand shadow-lg shadow-brand/10' : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border-color text-text-muted hover:text-text-main hover:border-brand/20'"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="px-4 py-2.5 rounded-xl text-sm font-black uppercase tracking-wider transition-all duration-300 cursor-pointer active:scale-95 border disabled:opacity-50 disabled:cursor-not-allowed"
          :class="currentPage === totalPages ? 'bg-surface-elevated/40 border-border-color text-text-muted' : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border-color text-text-muted hover:text-text-main hover:border-brand/20'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide w-4 h-4 lucide-chevron-right"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      </div>

      <!-- PAGINATION -->
      <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-12 animate-reveal">
        <button 
          @click="currentPage = Math.max(1, currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider border transition-all duration-300 cursor-pointer active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          :class="currentPage === 1 
            ? 'bg-surface-elevated/40 border-border-color text-text-muted' 
            : 'bg-surface-elevated/40 hover:bg-brand/10 border-border-color hover:border-brand/30 text-text-main'"
        >
          <ArrowLeft class="w-4 h-4" />
        </button>
        
        <template v-for="page in visiblePages" :key="page">
          <button 
            v-if="page === '...'"
            class="px-3 py-2 text-xs font-black uppercase tracking-wider text-text-muted cursor-default"
            disabled
          >
            ...
          </button>
          <button 
            v-else
            @click="currentPage = page"
            class="w-10 h-10 rounded-xl text-xs font-black uppercase tracking-wider transition-all duration-300 cursor-pointer active:scale-95 border"
            :class="currentPage === page 
              ? 'bg-brand text-slate-950 border-brand shadow-lg shadow-brand/20' 
              : 'bg-surface-elevated/40 hover:bg-brand/10 border-border-color hover:border-brand/30 text-text-main'"
          >
            {{ page }}
          </button>
        </template>
        
        <button 
          @click="currentPage = Math.min(totalPages, currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider border transition-all duration-300 cursor-pointer active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          :class="currentPage === totalPages 
            ? 'bg-surface-elevated/40 border-border-color text-text-muted' 
            : 'bg-surface-elevated/40 hover:bg-brand/10 border-border-color hover:border-brand/30 text-text-main'"
        >
          <ArrowRight class="w-4 h-4" />
        </button>
      </div>

      <!-- EMPTY STATE -->
      <div v-else class="glass-card max-w-xl mx-auto text-center py-16 px-8 border border-border-color rounded-[2.5rem] shadow-2xl animate-reveal">
        <div class="w-16 h-16 rounded-full bg-surface-elevated/60 border border-border-color flex items-center justify-center mx-auto mb-6 text-text-muted/60">
          <Search class="w-8 h-8" />
        </div>
        <h3 class="text-xl font-heading font-black text-text-main mb-3">No Articles Found</h3>
        <p class="text-text-muted text-sm font-semibold max-w-sm mx-auto mb-8 leading-relaxed">
          We couldn't find any articles matching "{{ searchQuery }}" or listed under the selected category.
        </p>
        <button 
          @click="resetFilters" 
          class="btn-secondary px-8 py-3.5 text-xs font-black uppercase tracking-wider"
        >
          Reset Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Calendar, Clock, ArrowRight, BookOpen, X, ArrowLeft } from 'lucide-vue-next'
import globalData from '~/data/global.json'

// Load all markdown files synchronously at build-time using Vite's glob import
const globbedPosts = import.meta.glob('../../data/blog/*.md', { query: '?raw', import: 'default', eager: true })

const posts = Object.entries(globbedPosts).map(([filepath, rawContent]) => {
  const slug = filepath.split('/').pop().replace('.md', '')
  
  // Parse frontmatter
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
  
  // simple read time estimate
  const wordCount = rawContent.split(/\s+/).length
  const readTime = Math.ceil(wordCount / 200)
  
  return {
    slug,
    path: `/blog/${slug}`,
    title: meta.title || slug,
    description: meta.description || '',
    date: meta.date || '',
    image: meta.image || '',
    tags: meta.tags || [],
    author: meta.author || 'Ringga Dev',
    category: meta.category || 'Engineering',
    readTime
  }
}).sort((a, b) => new Date(b.date) - new Date(a.date))

// Filter states
const searchQuery = ref('')
const selectedCategory = ref('All')

const categories = computed(() => {
  const list = posts.map(p => p.category).filter(Boolean)
  return ['All', ...new Set(list)]
})

const filteredPosts = computed(() => {
  return posts.filter(post => {
    const matchesCategory = selectedCategory.value === 'All' || post.category === selectedCategory.value
    const matchesSearch = !searchQuery.value || 
      post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
      post.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      post.tags.some(t => t.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesCategory && matchesSearch
  })
})

const featuredPost = computed(() => {
  if (searchQuery.value || selectedCategory.value !== 'All') return null
  return posts[0] || null
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'All'
  currentPage.value = 1
}

// Pagination
const postsPerPage = 5
const currentPage = ref(1)

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / postsPerPage))

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage
  const end = start + postsPerPage
  return filteredPosts.value.slice(start, end)
})

const gridPosts = computed(() => {
  if (featuredPost.value) {
    return paginatedPosts.value.filter(p => p.slug !== featuredPost.value.slug)
  }
  return paginatedPosts.value
})

const visiblePages = computed(() => {
  const pages = []
  const current = currentPage.value
  const total = totalPages.value
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    
    for (let i = start; i <= end; i++) {
      if (i !== 1 && i !== total) pages.push(i)
    }
    
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  
  return pages
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

useHead({
  title: `Writings & Thoughts | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: 'Explore my latest thoughts, tutorials, and insights on mobile engineering, clean architecture, and modern web development.' },
    { property: 'og:title', content: `Writings & Thoughts | ${globalData.siteName}` },
    { property: 'og:description', content: 'Explore my latest thoughts, tutorials, and insights on mobile engineering, clean architecture, and modern web development.' },
    { property: 'og:image', content: globalData.seo.ogImage },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' }
  ]
})

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-active')
      }
    })
  }, { threshold: 0.05 })

  document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el))
})
</script>

<style scoped>
/* Hide scrollbar for Chrome, Safari and Opera */
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
/* Hide scrollbar for IE, Edge and Firefox */
.scrollbar-none {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>
