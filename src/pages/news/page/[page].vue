<template>
  <NewsListing :page="page" />
</template>

<script setup>
/**
 * Halaman 2+ untuk listing berita: /news/page/2, /news/page/3, ...
 *
 * Path segment, bukan `?page=2` — GitHub Pages menyajikan file statis,
 * jadi query string selalu menunjuk ke news/index.html yang sama.
 */
import { computed } from 'vue'
import newsData from '~/data/news.json'

const route = useRoute()

const NEWS_PER_PAGE = 9
const totalPages = computed(() =>
  Math.max(1, Math.ceil(newsData.items.length / NEWS_PER_PAGE))
)

const page = computed(() => {
  const n = parseInt(route.params.page, 10)
  if (!Number.isFinite(n) || n < 2) return 1
  return Math.min(n, totalPages.value)
})

useHead(() => ({
  title: `Berita — Halaman ${page.value} | RINGGA DEV`,
  meta: [{ name: 'description', content: newsData.subtitle }]
}))
</script>
