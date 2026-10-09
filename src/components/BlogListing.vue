<template>
  <div class="min-h-screen pt-28 pb-20 bg-surface">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Title & Header -->
      <div class="mb-10 border-b border-border pb-8">
        <span class="stamp">Knowledge Base</span>
        <h1 class="text-4xl md:text-6xl font-display font-bold tracking-tight leading-none mt-4 mb-4 text-main riso-ghost">
          Writings &amp; Thoughts
        </h1>
        <p class="text-muted max-w-2xl text-base md:text-lg font-serif leading-relaxed">
          {{ isFirstPage ? 'Advanced mobile engineering, clean architecture, cross-platform systems, and high-performance web development.' : `Page ${page} of ${totalPages}` }}
        </p>
      </div>

      <!-- Controls Panel (Search & Category Filters) -->
      <div v-if="isFirstPage" class="mb-10 flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <div class="relative w-full md:w-80">
          <Search class="absolute left-3 top-3.5 w-4 h-4 text-muted" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search articles, tags..."
            class="w-full pl-10 pr-10 py-3 bg-surface border-[1.5px] border-ink/60 focus:border-brand rounded-sm text-sm font-serif placeholder:text-muted text-main outline-none transition-colors duration-150"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-3 top-3.5 text-muted hover:text-brand transition-colors duration-150"
            aria-label="Clear search"
          >
            <X class="w-4 h-4" />
          </button>
        </div>

        <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
          <button
            v-for="cat in categories"
            :key="cat"
            @click="selectedCategory = cat"
            class="px-3.5 py-2 font-mono text-xs uppercase tracking-[0.1em] whitespace-nowrap rounded-sm transition-[transform,box-shadow,border-color,background-color] duration-150 cursor-pointer border-[1.5px]"
            :class="selectedCategory === cat
              ? 'bg-brand text-white border-ink shadow-riso-ink -translate-y-0.5'
              : 'bg-transparent border-ink/60 text-muted hover:text-brand hover:border-brand hover:shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] hover:-translate-y-0.5'"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- FEATURED POST (halaman 1 saja) -->
      <div v-if="featuredPost" class="mb-14">
        <h2 class="font-mono text-xs uppercase tracking-[0.25em] text-muted mb-4">Featured Article</h2>
        <NuxtLink
          :to="featuredPost.path"
          class="riso-card group grid grid-cols-1 lg:grid-cols-12 gap-0 lg:gap-8 block"
        >
          <div class="lg:col-span-7 relative aspect-video lg:aspect-auto min-h-[280px] overflow-hidden">
            <img
              v-if="featuredPost.image"
              :src="featuredPost.image"
              :alt="featuredPost.title"
              fetchpriority="high"
              decoding="async"
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div v-else class="absolute inset-0 bg-surface-elevated halftone flex items-center justify-center">
              <BookOpen class="w-14 h-14 text-brand" />
            </div>
          </div>

          <div class="lg:col-span-5 p-8 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-5 flex-wrap">
              <span class="stamp">
                {{ featuredPost.category }}
              </span>
              <span class="font-mono text-xs text-muted flex items-center gap-1.5">
                <Calendar class="w-3.5 h-3.5 text-brand" />
                {{ formatDate(featuredPost.date) }}
              </span>
              <span class="font-mono text-xs text-muted flex items-center gap-1.5">
                <Clock class="w-3.5 h-3.5 text-brand" />
                {{ featuredPost.readTime }} min
              </span>
            </div>

            <h3 class="text-2xl md:text-3xl font-display font-bold text-main mb-4 leading-tight group-hover:text-brand transition-colors duration-150">
              {{ featuredPost.title }}
            </h3>

            <p class="text-muted font-serif text-base mb-6 leading-relaxed line-clamp-3">
              {{ featuredPost.description }}
            </p>

            <div class="flex items-center justify-between border-t border-border pt-5 mt-auto">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-sm bg-surface-elevated border-[1.5px] border-ink/60 shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] flex items-center justify-center text-brand font-mono text-xs font-bold">
                  {{ featuredPost.author.charAt(0) }}
                </div>
                <span class="font-mono text-xs text-main">{{ featuredPost.author }}</span>
              </div>

              <span class="text-brand font-mono text-xs uppercase tracking-wider flex items-center gap-1">
                Read
                <ArrowRight class="w-4 h-4" />
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- ARTICLES GRID -->
      <div v-if="gridPosts.length">
        <h2 v-if="featuredPost" class="font-mono text-xs uppercase tracking-[0.25em] text-muted mb-4">All Articles</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <NuxtLink
            v-for="(post, idx) in gridPosts"
            :key="post.slug"
            :to="post.path"
            class="group flex flex-col h-full"
            :class="idx % 2 === 0 ? 'riso-card' : 'riso-card-2'"
          >
            <div class="relative h-52 w-full overflow-hidden border-b-[1.5px] border-ink/40">
              <img
                v-if="post.image"
                :src="post.image"
                :alt="post.title"
                loading="lazy"
                decoding="async"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full bg-surface-elevated halftone flex items-center justify-center">
                <BookOpen class="w-10 h-10 text-brand" />
              </div>

              <span class="absolute top-3 left-3 font-mono text-[10px] uppercase tracking-[0.15em] px-2 py-1 bg-ink text-paper border-[1.5px] border-paper rounded-sm">
                {{ post.category }}
              </span>
            </div>

            <div class="p-6 flex flex-col flex-grow">
              <div class="flex items-center gap-3 font-mono text-[11px] text-muted mb-3">
                <span class="flex items-center gap-1">
                  <Calendar class="w-3.5 h-3.5 text-brand" />
                  {{ formatDate(post.date) }}
                </span>
                <span class="w-1 h-1 bg-ink/40"></span>
                <span class="flex items-center gap-1">
                  <Clock class="w-3.5 h-3.5 text-brand" />
                  {{ post.readTime }} min
                </span>
              </div>

              <h3 class="text-xl font-display font-bold text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-150 line-clamp-2">
                {{ post.title }}
              </h3>

              <p class="text-muted text-sm leading-relaxed font-serif mb-5 line-clamp-3">
                {{ post.description }}
              </p>

              <div class="mt-auto pt-4 border-t border-border flex items-center justify-between">
                <span class="font-mono text-xs text-muted flex items-center gap-2">
                  <span class="w-6 h-6 rounded-sm bg-surface-elevated flex items-center justify-center text-[10px] text-brand border-[1.5px] border-ink/60 font-mono font-bold">{{ post.author.charAt(0) }}</span>
                  {{ post.author }}
                </span>

                <span class="text-brand font-mono text-xs uppercase tracking-wider flex items-center gap-1">
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
      <div v-else class="riso-card max-w-xl mx-auto text-center py-16 px-8">
        <div class="w-14 h-14 rounded-sm bg-surface-elevated border-[1.5px] border-ink/60 shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] flex items-center justify-center mx-auto mb-5 text-brand">
          <Search class="w-6 h-6" />
        </div>
        <h3 class="text-xl font-display font-bold text-main mb-3">No Articles Found</h3>
        <p class="text-muted text-sm font-serif max-w-sm mx-auto mb-6 leading-relaxed">
          <template v-if="isFirstPage">
            No articles match "{{ searchQuery }}" or the selected category.
          </template>
          <template v-else>
            Halaman {{ page }} tidak punya artikel. Kembali ke
            <NuxtLink to="/blog" class="text-brand underline">daftar semua artikel</NuxtLink>.
          </template>
        </p>
        <NuxtLink v-if="!isFirstPage" to="/blog" class="btn-secondary px-7 py-3 font-mono text-xs uppercase tracking-[0.15em] inline-block">
          Back to Blog
        </NuxtLink>
        <button
          v-else
          @click="resetFilters"
          class="btn-secondary px-7 py-3 font-mono text-xs uppercase tracking-[0.15em]"
        >
          Reset Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
    : `Writings & Thoughts | Page ${page.value} | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: 'Explore my latest thoughts, tutorials, and insights on mobile engineering, clean architecture, and modern web development.' },
    { property: 'og:title', content: `Writings & Thoughts | ${globalData.siteName}` },
    { property: 'og:description', content: 'Explore my latest thoughts, tutorials, and insights on mobile engineering, clean architecture, and modern web development.' },
    { property: 'og:image', content: globalData.seo.ogImage },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' }
  ]
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
