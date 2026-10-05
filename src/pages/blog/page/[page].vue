<template>
  <BlogListing :page="page" />
</template>

<script setup>
/**
 * Halaman 2+ untuk listing blog: /blog/page/2, /blog/page/3, ...
 *
 * Kenapa path segment dan bukan `?page=2`: GitHub Pages menyajikan file
 * statis, jadi `/blog?page=2` selalu menunjuk ke `blog/index.html` yang
 * sama dengan `/blog`. Path segment di-prerender jadi file terpisah
 * (blog/page/2/index.html) sehingga benar-benar bisa diakses.
 */
import { computed } from 'vue'
import globalData from '~/data/global.json'
import { collectBlogPosts } from '~/composables/useBlog'

const route = useRoute()

const BLOG_POSTS_PER_PAGE = 9
const totalPages = computed(() =>
  Math.max(1, Math.ceil(collectBlogPosts().length / BLOG_POSTS_PER_PAGE))
)

const page = computed(() => {
  const n = parseInt(route.params.page, 10)
  if (!Number.isFinite(n) || n < 2) return 1
  return Math.min(n, totalPages.value)
})

useHead(() => ({
  title: `Writings & Thoughts — Page ${page.value} | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: 'Explore my latest thoughts, tutorials, and insights on mobile engineering, clean architecture, and modern web development.' },
    { property: 'og:title', content: `Writings & Thoughts | ${globalData.siteName}` },
    { property: 'og:type', content: 'website' }
  ]
}))
</script>
