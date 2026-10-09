<template>
  <nav
    v-if="totalPages > 1"
    class="flex items-center justify-center gap-2 mt-12"
    style="animation-delay: 400ms"
    aria-label="Pagination"
  >
    <NuxtLink
      v-if="current > 1"
      :to="href(current - 1)"
      :aria-label="`Ke halaman ${current - 1}`"
      class="w-11 h-11 flex items-center justify-center rounded-xl border border-border bg-surface-elevated/40 text-muted hover:bg-surface-elevated/80 hover:text-main hover:border-brand/20 transition-all duration-300"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
    </NuxtLink>
    <span
      v-else
      aria-hidden="true"
      class="w-11 h-11 flex items-center justify-center rounded-xl border border-border bg-surface-elevated/40 text-muted/40"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
    </span>

    <div class="flex items-center gap-1">
      <template v-for="(page, idx) in visiblePages" :key="`${page}-${idx}`">
        <span v-if="page === '...'" class="w-8 text-center text-muted/60 select-none font-mono" aria-hidden="true">…</span>
        <NuxtLink
          v-else
          :to="href(page)"
          class="w-11 h-11 flex items-center justify-center rounded-xl text-sm font-semibold border transition-all duration-300"
          :class="page === current
            ? 'bg-brand text-brand-dark border-brand'
            : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border text-muted hover:text-main hover:border-brand/20'"
          :aria-current="page === current ? 'page' : undefined"
          :aria-label="`Halaman ${page}`"
        >
          {{ page }}
        </NuxtLink>
      </template>
    </div>

    <NuxtLink
      v-if="current < totalPages"
      :to="href(current + 1)"
      :aria-label="`Ke halaman ${current + 1}`"
      class="w-11 h-11 flex items-center justify-center rounded-xl border border-border bg-surface-elevated/40 text-muted hover:bg-surface-elevated/80 hover:text-main hover:border-brand/20 transition-all duration-300"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </NuxtLink>
    <span
      v-else
      aria-hidden="true"
      class="w-11 h-11 flex items-center justify-center rounded-xl border border-border bg-surface-elevated/40 text-muted/40"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </span>
  </nav>
</template>

<script setup>
/**
 * Pagination untuk static hosting (GitHub Pages).
 *
 * PENTING: pakai PATH segment (`/blog/page/2`), bukan query string
 * (`/blog?page=2`). GitHub Pages hanya menyajikan file statis, jadi
 * `?page=2` selalu menunjuk ke `blog/index.html` yang sama dan semua
 * halaman akan menampilkan page 1.
 */
import { computed } from 'vue'

const props = defineProps({
  /** Halaman aktif (1-based) */
  current: { type: Number, required: true },
  /** Total jumlah halaman */
  totalPages: { type: Number, required: true },
  /** Base path untuk halaman > 1, mis. "/blog" -> "/blog/page/2" */
  basePath: { type: String, required: true }
})

function href(page) {
  const base = props.basePath.replace(/\/+$/, '')
  return page <= 1 ? base : `${base}/page/${page}`
}

const visiblePages = computed(() => {
  const pages = []
  const cur = props.current
  const total = props.totalPages

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)
  if (cur > 3) pages.push('...')

  const start = Math.max(2, cur - 1)
  const end = Math.min(total - 1, cur + 1)
  for (let i = start; i <= end; i++) {
    if (i !== 1 && i !== total) pages.push(i)
  }

  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})
</script>
