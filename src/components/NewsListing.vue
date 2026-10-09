<template>
  <div class="min-h-screen pt-28 pb-20 bg-surface">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Title & Header -->
      <div class="mb-12 border-b border-border pb-8">
        <span class="stamp">News Feed</span>
        <h1 class="text-4xl md:text-6xl font-display font-bold tracking-tight leading-none mt-4 mb-4 text-main riso-ghost">
          {{ newsData.title }}
        </h1>
        <p class="text-muted max-w-2xl text-base md:text-lg font-serif leading-relaxed">
          {{ newsData.subtitle }}
        </p>
        <p class="text-muted font-mono text-xs mt-4 flex items-center gap-1.5">
          <RefreshCw class="w-3.5 h-3.5 text-brand" />
          Diperbarui {{ formatDate(newsData.updatedAt) }}
        </p>
      </div>

      <!-- HEADLINE (halaman 1 saja) -->
      <div v-if="featured" class="mb-14">
        <h2 class="font-mono text-xs uppercase tracking-[0.25em] text-muted mb-4">Headline</h2>
        <NuxtLink
          :to="`/news/${featured.slug}`"
          class="riso-card group grid grid-cols-1 lg:grid-cols-12 gap-0 lg:gap-8 block"
        >
          <div class="lg:col-span-7 relative aspect-video lg:aspect-auto min-h-[280px] overflow-hidden">
            <img
              :src="featured.image"
              :alt="featured.title"
              fetchpriority="high"
              decoding="async"
              class="absolute inset-0 w-full h-full object-cover"
            />
          </div>

          <div class="lg:col-span-5 p-8 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-5 flex-wrap">
              <span class="stamp">
                {{ featured.category }}
              </span>
              <span class="font-mono text-xs text-muted flex items-center gap-1.5">
                <Calendar class="w-3.5 h-3.5 text-brand" />
                {{ formatDate(featured.date) }}
              </span>
            </div>

            <h3 class="text-2xl md:text-3xl font-display font-bold text-main mb-4 leading-tight group-hover:text-brand transition-colors duration-150">
              {{ featured.title }}
            </h3>

            <p class="text-muted font-serif text-base mb-6 leading-relaxed line-clamp-3">
              {{ featured.excerpt }}
            </p>

            <div class="flex items-center justify-between border-t border-border pt-5 mt-auto">
              <span class="font-mono text-xs text-main flex items-center gap-2">
                <Newspaper class="w-4 h-4 text-brand" />
                {{ featured.source }}
              </span>
              <span class="text-brand font-mono text-xs uppercase tracking-wider flex items-center gap-1">
                Baca
                <ArrowRight class="w-4 h-4" />
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- NEWS GRID -->
      <div v-if="paginatedItems.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <NuxtLink
          v-for="(item, idx) in paginatedItems"
          :key="item.slug"
          :to="`/news/${item.slug}`"
          class="group flex flex-col h-full"
          :class="idx % 2 === 0 ? 'riso-card' : 'riso-card-2'"
        >
          <div class="relative h-52 w-full overflow-hidden border-b-[1.5px] border-ink/40">
            <img
              :src="item.image"
              :alt="item.title"
              loading="lazy"
              decoding="async"
              class="w-full h-full object-cover"
            />
            <span class="absolute top-3 left-3 font-mono text-[10px] uppercase tracking-[0.15em] px-2 py-1 bg-ink text-paper border-[1.5px] border-paper rounded-sm">
              {{ item.category }}
            </span>
          </div>

          <div class="p-6 flex flex-col flex-grow">
            <div class="flex items-center gap-3 font-mono text-[11px] text-muted mb-3">
              <span class="flex items-center gap-1">
                <Calendar class="w-3.5 h-3.5 text-brand" />
                {{ formatDate(item.date) }}
              </span>
            </div>

            <h3 class="text-xl font-display font-bold text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-150 line-clamp-2">
              {{ item.title }}
            </h3>

            <p class="text-muted text-sm leading-relaxed font-serif mb-5 line-clamp-3">
              {{ item.excerpt }}
            </p>

            <div class="mt-auto pt-4 border-t border-border flex items-center justify-between">
              <span class="font-mono text-xs text-muted flex items-center gap-2">
                <Newspaper class="w-4 h-4 text-brand" />
                {{ item.source }}
              </span>
              <span class="text-brand font-mono text-xs uppercase tracking-wider flex items-center gap-1">
                Baca
                <ArrowRight class="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- PAGINATION -->
      <Pagination
        v-if="paginatedItems.length"
        :current="page"
        :total-pages="totalPages"
        base-path="/news"
        class="mt-12"
      />

      <!-- EMPTY STATE -->
      <div v-if="!paginatedItems.length" class="riso-card max-w-xl mx-auto text-center py-16 px-8">
        <Newspaper class="w-12 h-12 text-brand mx-auto mb-5" />
        <h3 class="text-xl font-display font-bold text-main mb-3">
          {{ newsData.items.length ? 'Halaman tidak tersedia' : 'Belum ada berita' }}
        </h3>
        <p class="text-muted text-sm font-serif leading-relaxed mb-6">
          <template v-if="newsData.items.length">
            Halaman {{ page }} tidak punya berita. Kembali ke
            <NuxtLink to="/news" class="text-brand underline">berita terbaru</NuxtLink>.
          </template>
          <template v-else>
            Feed berita akan terisi otomatis setelah pipeline harian berjalan.
          </template>
        </p>
        <NuxtLink v-if="newsData.items.length" to="/news" class="btn-secondary px-7 py-3 font-mono text-xs uppercase tracking-[0.15em] inline-block">
          Back to News
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Calendar, ArrowRight, Newspaper, RefreshCw } from 'lucide-vue-next'
import newsData from '~/data/news.json'

/**
 * Halaman 1-based. `/news` mengoper 1, `/news/page/N` mengoper N.
 * Pakai path segment, bukan `?page=N`: GitHub Pages menyajikan file statis,
 * jadi `?page=2` selalu menunjuk ke news/index.html yang sama.
 */
const props = defineProps({
  page: { type: Number, default: 1 }
})

const page = computed(() => Math.max(1, props.page || 1))
const isFirstPage = computed(() => page.value === 1)

// Harus sama dengan NEWS_PER_PAGE di nuxt.config.ts
const NEWS_PER_PAGE = 9

const totalPages = computed(() => Math.max(1, Math.ceil(newsData.items.length / NEWS_PER_PAGE)))

// Headline hanya di halaman 1; item pertama halaman 1 jadi headline,
// jadi grid halaman 1 mulai dari index 1 (bukan 0).
const featured = computed(() => (isFirstPage.value ? newsData.items[0] || null : null))

const paginatedItems = computed(() => {
  const raw = newsData.items.slice((page.value - 1) * NEWS_PER_PAGE, page.value * NEWS_PER_PAGE)
  return isFirstPage.value ? raw.slice(1) : raw
})

const formatDate = (d) => {
  if (!d) return ''
  const dt = new Date(d)
  if (isNaN(dt)) return d
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}

useHead({
  title: isFirstPage.value
    ? `Berita | RINGGA DEV`
    : `Berita | Halaman ${page.value} | RINGGA DEV`,
  meta: [
    { name: 'description', content: newsData.subtitle }
  ]
})
</script>
