<template>
  <div class="min-h-screen relative bg-surface text-main pb-24 transition-colors duration-500">
    <div v-if="item" class="w-full">
      <!-- Immersive Header Banner -->
      <div class="relative h-[60vh] w-full overflow-hidden flex items-end">
        <div class="absolute inset-0 z-0">
          <img
            :src="item.image"
            :alt="item.title"
            class="w-full h-full object-cover scale-105"
          />
          <!-- Printed plate: flat paper block + halftone screen over the cover -->
          <div class="absolute inset-x-0 bottom-0 h-3/5 bg-surface z-10"></div>
          <div class="halftone absolute inset-x-0 bottom-0 h-3/5 z-10 opacity-60" aria-hidden="true"></div>
          <div class="absolute inset-0 bg-surface/20 z-0"></div>
        </div>

        <!-- Float Nav Controls & Metadata -->
        <div class="max-w-7xl mx-auto w-full px-6 pb-12 relative z-20">
          <!-- Back Link -->
          <NuxtLink
            to="/news"
            class="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-brand hover:text-brand-light transition-colors mb-8 font-mono bg-surface-card border-[1.5px] border-ink/60 px-4 py-2.5 rounded-sm shadow-[2px_2px_0_hsl(var(--brand-color)/0.35)] hover:shadow-[3px_3px_0_hsl(var(--brand-color)/0.8)]"
          >
            <ArrowLeft class="w-4 h-4" /> Kembali ke Berita
          </NuxtLink>

          <div class="flex flex-wrap items-center gap-3 mb-6">
            <span class="stamp">
              {{ item.category }}
            </span>
            <span class="text-xs text-muted font-mono flex items-center gap-1.5 ml-2">
              <Calendar class="w-3.5 h-3.5 text-brand/70" />
              {{ formatDate(item.date) }}
            </span>
            <span class="text-xs text-muted font-mono flex items-center gap-1.5 ml-2">
              <Newspaper class="w-3.5 h-3.5 text-brand/70" />
              {{ item.source }}
            </span>
          </div>

          <div v-if="item.tags && item.tags.length" class="flex flex-wrap gap-2 mb-6">
            <span
              v-for="tag in item.tags"
              :key="tag"
              class="text-[10px] px-2.5 py-1 rounded-sm bg-surface-card/60 border-[1.5px] border-ink/60 text-muted font-semibold font-mono"
            >
              #{{ tag }}
            </span>
          </div>

          <h1 class="text-3xl sm:text-5xl md:text-6xl font-display font-bold text-main leading-tight mb-4 max-w-4xl tracking-tight">
            {{ item.title }}
          </h1>

          <p class="text-base sm:text-lg md:text-xl text-muted font-medium max-w-3xl leading-relaxed">
            {{ item.excerpt }}
          </p>
        </div>
      </div>

      <!-- CONTENT -->
      <div class="max-w-4xl mx-auto px-6 pt-12 relative z-20">
        <article class="prose prose-brand max-w-none prose-h2:text-main prose-h3:text-main prose-p:leading-relaxed">
          <p class="text-lg leading-relaxed text-main/90 font-medium">
            {{ item.summary }}
          </p>

          <h2 class="mt-10 text-2xl font-display font-bold text-main">Fakta Kunci</h2>
          <ul class="mt-4 space-y-3">
            <li
              v-for="(fact, i) in item.keyFacts"
              :key="i"
              class="flex items-start gap-3 text-main/80"
            >
              <span class="mt-1 w-5 h-5 shrink-0 rounded-sm bg-surface-elevated border-[1.5px] border-ink/70 shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] flex items-center justify-center text-brand text-[10px] font-semibold font-mono">
                {{ i + 1 }}
              </span>
              <span class="leading-relaxed">{{ fact }}</span>
            </li>
          </ul>

          <div class="mt-12 riso-card p-6 md:p-8 bg-surface-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <p class="text-xs font-semibold uppercase tracking-widest text-muted font-mono mb-1">Sumber Berita</p>
              <p class="text-main font-bold">{{ item.source }}</p>
            </div>
            <a
              :href="item.sourceUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-primary flex items-center gap-2 py-3 px-6 text-xs font-semibold uppercase tracking-wider"
            >
              Baca Artikel Asli
              <ArrowUpRight class="w-4 h-4" />
            </a>
          </div>

          <p class="mt-6 text-xs text-muted/70 font-mono">
            Data dihimpun dari sumber berita terpercaya dan disajikan untuk tujuan informasi. Kunjungi tautan sumber untuk laporan lengkap.
          </p>
        </article>
      </div>
    </div>

    <!-- NOT FOUND -->
    <div v-else class="min-h-screen flex flex-col items-center justify-center text-center px-6">
      <div class="w-16 h-16 rounded-sm bg-surface-elevated/60 border-[1.5px] border-ink/60 shadow-[3px_3px_0_hsl(var(--brand-color)/0.6)] flex items-center justify-center mb-6 text-muted">
        <Newspaper class="w-8 h-8" />
      </div>
      <h3 class="text-xl font-display font-bold text-main mb-3">Berita Tidak Ditemukan</h3>
      <p class="text-muted text-sm font-semibold max-w-sm mx-auto mb-8">Berita yang Anda cari mungkin telah dipindahkan atau dihapus.</p>
      <NuxtLink to="/news" class="btn-secondary px-8 py-3.5 text-xs font-semibold uppercase tracking-wider">
        Kembali ke Berita
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Calendar, ArrowLeft, ArrowUpRight, Newspaper } from 'lucide-vue-next'
import newsData from '~/data/news.json'

const route = useRoute()
const item = computed(() =>
  newsData.items.find(n => n.slug === route.params.slug) || null
)

useHead(() => ({
  title: item.value ? `${item.value.title} | RINGGA DEV` : 'Berita | RINGGA DEV',
  meta: [
    { name: 'description', content: item.value ? item.value.excerpt : newsData.subtitle }
  ]
}))

const formatDate = (d) => {
  if (!d) return ''
  const dt = new Date(d)
  if (isNaN(dt)) return d
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
