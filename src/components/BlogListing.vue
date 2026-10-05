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
          {{ isFirstPage ? 'Writings & Thoughts' : `Writings & Thoughts` }}
        </h1>
        <p class="text-muted max-w-2xl mx-auto text-base md:text-lg font-medium leading-relaxed">
          {{ isFirstPage ? 'Exploring advanced mobile engineering, clean architecture, cross-platform systems, and high-performance web development.' : `Page ${page} of ${totalPages}` }}
        </p>
      </div>

      <!-- Controls Panel (Search & Category Filters) -->
      <div v-if="isFirstPage" class="glass-card p-4 rounded-3xl mb-12 border border-border shadow-xl flex flex-col md:flex-row gap-4 items-center justify-between animate-reveal" style="animation-delay: 100ms">
        <div class="relative w-full md:w-80 group">
          <Search class="absolute left-4 top-3.5 w-4 h-4 text-muted group-focus-within:text-brand transition-colors" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search articles, tags..."
            class="w-full pl-11 pr-4 py-3 bg-surface-elevated/40 hover:bg-surface-elevated/60 focus:bg-surface-elevated border border-border focus:border-brand/50 rounded-2xl text-sm font-semibold placeholder:text-muted/60 text-main outline-none transition-all duration-300"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-4 top-3.5 text-muted hover:text-brand transition-colors"
          >
            <X class="w-4 h-4" />
          </button>
        </div>

        <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
          <button
            v-for="cat in categories"
            :key="cat"
            @click="selectedCategory = cat"
            class="px-4 py-2.5 rounded-xl text-xs font-black uppercase tracking-wider whitespace-nowrap transition-all duration-300 cursor-pointer active:scale-95 border"
            :class="selectedCategory === cat
              ? 'bg-brand text-brand-dark border-brand shadow-lg shadow-brand/10'
              : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border text-muted hover:text-main hover:border-brand/20'"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- FEATURED POST (halaman 1 saja) -->
      <div v-if="featuredPost" class="mb-16 animate-reveal" style="animation-delay: 200ms">
        <h2 class="text-xs font-black uppercase tracking-widest text-muted mb-4 font-mono">Featured Article</h2>
        <NuxtLink
          :to="featuredPost.path"
          class="glass-card overflow-hidden group border border-border/80 rounded-[2.5rem] grid grid-cols-1 lg:grid-cols-12 gap-0 lg:gap-8 hover:border-brand/40 shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1 block"
        >
          <div class="lg:col-span-7 relative aspect-video lg:aspect-auto min-h-[300px] overflow-hidden">
            <img
              v-if="featuredPost.image"
              :src="featuredPost.image"
              :alt="featuredPost.title"
              class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div v-else class="absolute inset-0 bg-surface-elevated flex items-center justify-center">
              <BookOpen class="w-16 h-16 text-muted/30" />
            </div>
            <div class="absolute inset-0 bg-gradient-to-t lg:bg-gradient-to-r from-surface to-transparent opacity-80 lg:opacity-40"></div>
          </div>

          <div class="lg:col-span-5 p-8 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-6 flex-wrap">
              <span class="text-[9px] px-2.5 py-1 rounded-lg bg-brand/10 border border-brand/25 text-brand font-black uppercase tracking-wider font-mono">
                {{ featuredPost.category }}
              </span>
              <span class="text-xs text-muted font-mono flex items-center gap-1.5">
                <Calendar class="w-3.5 h-3.5 text-brand/70" />
                {{ formatDate(featuredPost.date) }}
              </span>
              <span class="text-xs text-muted font-mono flex items-center gap-1.5">
                <Clock class="w-3.5 h-3.5 text-brand/70" />
                {{ featuredPost.readTime }} min read
              </span>
            </div>

            <h3 class="text-2xl md:text-3xl lg:text-4xl font-heading font-black text-main mb-4 leading-tight group-hover:text-brand transition-colors duration-300">
              {{ featuredPost.title }}
            </h3>

            <p class="text-muted font-medium text-base mb-8 leading-relaxed line-clamp-3">
              {{ featuredPost.description }}
            </p>

            <div class="flex items-center justify-between border-t border-border/60 pt-6 mt-auto">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-brand/10 border border-brand/30 flex items-center justify-center text-brand font-black font-mono text-xs shadow-inner">
                  {{ featuredPost.author.charAt(0) }}
                </div>
                <span class="text-xs font-bold text-main tracking-wide">{{ featuredPost.author }}</span>
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
      <div v-if="gridPosts.length" class="space-y-6">
        <h2 v-if="featuredPost" class="text-xs font-black uppercase tracking-widest text-muted mb-4 font-mono">All Articles</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <NuxtLink
            v-for="(post, index) in gridPosts"
            :key="post.slug"
            :to="post.path"
            class="glass-card overflow-hidden group hover:border-brand/40 border border-border/80 rounded-[2.2rem] flex flex-col h-full hover:shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1.5 animate-reveal"
            :style="`animation-delay: ${150 + (index * 50)}ms`"
          >
            <div class="relative h-56 w-full overflow-hidden border-b border-border/40">
              <img
                v-if="post.image"
                :src="post.image"
                :alt="post.title"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div v-else class="w-full h-full bg-surface-elevated flex items-center justify-center">
                <BookOpen class="w-12 h-12 text-muted/20" />
              </div>
              <div class="absolute inset-0 bg-gradient-to-t from-surface-card to-transparent opacity-40"></div>

              <span class="absolute top-4 left-4 text-[8px] px-2.5 py-1 rounded-md bg-surface-card/80 backdrop-blur-md border border-border/30 text-brand font-black uppercase tracking-widest">
                {{ post.category }}
              </span>
            </div>

            <div class="p-6 md:p-8 flex flex-col flex-grow">
              <div class="flex items-center gap-3 text-[11px] text-muted font-mono mb-4">
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

              <h3 class="text-xl font-heading font-black text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-300 line-clamp-2">
                {{ post.title }}
              </h3>

              <p class="text-muted text-sm leading-relaxed font-semibold mb-6 line-clamp-3">
                {{ post.description }}
              </p>

              <div class="mt-auto pt-5 border-t border-border/40 flex items-center justify-between">
                <span class="text-xs font-bold text-muted flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-surface-elevated flex items-center justify-center text-[10px] text-brand border border-border font-mono">{{ post.author.charAt(0) }}</span>
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
      <Pagination
        v-if="gridPosts.length"
        :current="page"
        :total-pages="totalPages"
        base-path="/blog"
        class="mt-12"
      />

      <!-- EMPTY STATE -->
      <div v-else class="glass-card max-w-xl mx-auto text-center py-16 px-8 border border-border rounded-[2.5rem] shadow-2xl animate-reveal">
        <div class="w-16 h-16 rounded-full bg-surface-elevated/60 border border-border flex items-center justify-center mx-auto mb-6 text-muted/60">
          <Search class="w-8 h-8" />
        </div>
        <h3 class="text-xl font-heading font-black text-main mb-3">No Articles Found</h3>
        <p class="text-muted text-sm font-semibold max-w-sm mx-auto mb-8 leading-relaxed">
          <template v-if="isFirstPage">
            We couldn't find any articles matching "{{ searchQuery }}" or listed under the selected category.
          </template>
          <template v-else>
            Halaman {{ page }} tidak punya artikel. Kembali ke
            <NuxtLink to="/blog" class="text-brand font-bold underline">daftar semua artikel</NuxtLink>.
          </template>
        </p>
        <NuxtLink v-if="!isFirstPage" to="/blog" class="btn-secondary px-8 py-3.5 text-xs font-black uppercase tracking-wider inline-block">
          Back to Blog
        </NuxtLink>
        <button
          v-else
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
import { ref, computed, watch, onMounted } from 'vue'
import { Search, Calendar, Clock, ArrowRight, BookOpen, X } from 'lucide-vue-next'
import globalData from '~/data/global.json'
import { collectBlogPosts } from '~/composables/useBlog'

/**
 * Halaman 1-based. `/blog` mengoper 1, `/blog/page/N` mengoper N.
 * Slice/filter dihitung dari `page`, bukan dari state router, supaya
 * hasil prerender untuk tiap path identik dengan yang dirender client.
 */
const props = defineProps({
  page: { type: Number, default: 1 }
})

const page = computed(() => Math.max(1, props.page || 1))
const isFirstPage = computed(() => page.value === 1)

const posts = collectBlogPosts()

// Harus sama dengan BLOG_POSTS_PER_PAGE di nuxt.config.ts
const BLOG_POSTS_PER_PAGE = 9

const searchQuery = ref('')
const selectedCategory = ref('All')

const categories = computed(() => ['All', ...new Set(posts.map(p => p.category).filter(Boolean))])

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
  if (!isFirstPage.value) return null
  if (searchQuery.value || selectedCategory.value !== 'All') return null
  return posts[0] || null
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredPosts.value.length / BLOG_POSTS_PER_PAGE)))

const paginatedPosts = computed(() => {
  const start = (page.value - 1) * BLOG_POSTS_PER_PAGE
  return filteredPosts.value.slice(start, start + BLOG_POSTS_PER_PAGE)
})

const gridPosts = computed(() => {
  if (featuredPost.value) {
    return paginatedPosts.value.filter(p => p.slug !== featuredPost.value.slug)
  }
  return paginatedPosts.value
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'All'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

useHead({
  title: isFirstPage.value
    ? `Writings & Thoughts | ${globalData.siteName}`
    : `Writings & Thoughts — Page ${page.value} | ${globalData.siteName}`,
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
      if (entry.isIntersecting) entry.target.classList.add('reveal-active')
    })
  }, { threshold: 0.05 })

  document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el))
})
</script>

<style scoped>
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
