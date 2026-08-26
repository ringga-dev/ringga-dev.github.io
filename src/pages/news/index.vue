<template>
  <div class="min-h-screen pt-28 pb-20 relative overflow-hidden bg-surface">
    <!-- Immersive Background Orbs -->
    <div class="absolute top-[10%] left-[-10%] w-[30vw] h-[30vw] rounded-full blur-[120px] bg-brand/5 pointer-events-none"></div>
    <div class="absolute bottom-[20%] right-[-10%] w-[35vw] h-[35vw] rounded-full blur-[150px] bg-brand-light/5 pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <!-- Title & Header -->
      <div class="text-center mb-12 animate-reveal">
        <div class="inline-block px-3.5 py-1 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-mono mb-4 uppercase tracking-widest">
          News Feed
        </div>
        <h1 class="text-4xl md:text-6xl font-heading font-black tracking-tight leading-none mb-6">
          {{ newsData.title.split(' ')[0] }} <span class="text-gradient">{{ newsData.title.split(' ').slice(1).join(' ') }}</span>
        </h1>
        <p class="text-muted max-w-2xl mx-auto text-base md:text-lg font-medium leading-relaxed">
          {{ newsData.subtitle }}
        </p>
        <p class="text-muted/70 text-xs font-mono mt-4 flex items-center justify-center gap-1.5">
          <RefreshCw class="w-3.5 h-3.5 text-brand/70" />
          Diperbarui {{ formatDate(newsData.updatedAt) }}
        </p>
      </div>

      <!-- FEATURED NEWS -->
      <div v-if="newsData.items.length" class="mb-16 animate-reveal" style="animation-delay: 200ms">
        <h2 class="text-xs font-black uppercase tracking-widest text-muted mb-4 font-mono">Headline</h2>
        <NuxtLink
          :to="`/news/${featured.slug}`"
          class="glass-card overflow-hidden group border border-border/80 rounded-[2.5rem] grid grid-cols-1 lg:grid-cols-12 gap-0 lg:gap-8 hover:border-brand/40 shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1 block"
        >
          <div class="lg:col-span-7 relative aspect-video lg:aspect-auto min-h-[300px] overflow-hidden">
            <img
              :src="featured.image"
              :alt="featured.title"
              class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div class="absolute inset-0 bg-gradient-to-t lg:bg-gradient-to-r from-surface to-transparent opacity-80 lg:opacity-40"></div>
          </div>

          <div class="lg:col-span-5 p-8 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-6 flex-wrap">
              <span class="text-[9px] px-2.5 py-1 rounded-lg bg-brand/10 border border-brand/25 text-brand font-black uppercase tracking-wider font-mono">
                {{ featured.category }}
              </span>
              <span class="text-xs text-muted font-mono flex items-center gap-1.5">
                <Calendar class="w-3.5 h-3.5 text-brand/70" />
                {{ formatDate(featured.date) }}
              </span>
            </div>

            <h3 class="text-2xl md:text-3xl lg:text-4xl font-heading font-black text-main mb-4 leading-tight group-hover:text-brand transition-colors duration-300">
              {{ featured.title }}
            </h3>

            <p class="text-muted font-medium text-base mb-8 leading-relaxed line-clamp-3">
              {{ featured.excerpt }}
            </p>

            <div class="flex items-center justify-between border-t border-border/60 pt-6 mt-auto">
              <span class="text-xs font-bold text-main tracking-wide flex items-center gap-2">
                <Newspaper class="w-4 h-4 text-brand" />
                {{ featured.source }}
              </span>
              <div class="flex items-center text-brand text-xs font-black uppercase tracking-widest gap-1 group-hover:translate-x-1.5 transition-transform duration-300">
                Baca
                <ArrowRight class="w-4 h-4" />
              </div>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- NEWS GRID -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <NuxtLink
          v-for="(item, index) in gridItems"
          :key="item.slug"
          :to="`/news/${item.slug}`"
          class="glass-card overflow-hidden group hover:border-brand/40 border border-border/80 rounded-[2.2rem] flex flex-col h-full hover:shadow-2xl hover:shadow-brand/5 transition-all duration-500 hover:-translate-y-1.5 animate-reveal"
          :style="`animation-delay: ${150 + (index * 50)}ms`"
        >
          <div class="relative h-56 w-full overflow-hidden border-b border-border/40">
            <img
              :src="item.image"
              :alt="item.title"
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-surface-card to-transparent opacity-40"></div>
            <span class="absolute top-4 left-4 text-[8px] px-2.5 py-1 rounded-md bg-surface-card/80 backdrop-blur-md border border-border/30 text-brand font-black uppercase tracking-widest">
              {{ item.category }}
            </span>
          </div>

          <div class="p-6 md:p-8 flex flex-col flex-grow">
            <div class="flex items-center gap-3 text-[11px] text-muted font-mono mb-4">
              <span class="flex items-center gap-1">
                <Calendar class="w-3.5 h-3.5 text-brand/70" />
                {{ formatDate(item.date) }}
              </span>
            </div>

            <h3 class="text-xl font-heading font-black text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-300 line-clamp-2">
              {{ item.title }}
            </h3>

            <p class="text-muted text-sm leading-relaxed font-semibold mb-6 line-clamp-3">
              {{ item.excerpt }}
            </p>

            <div class="mt-auto pt-5 border-t border-border/40 flex items-center justify-between">
              <span class="text-xs font-bold text-muted flex items-center gap-2">
                <Newspaper class="w-4 h-4 text-brand/70" />
                {{ item.source }}
              </span>
              <span class="text-brand text-xs font-black uppercase tracking-wider flex items-center gap-0.5 group-hover:translate-x-1 transition-transform duration-300">
                Baca
                <ArrowRight class="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Calendar, ArrowRight, Newspaper, RefreshCw } from 'lucide-vue-next'
import newsData from '~/data/news.json'

useHead({
  title: `Berita | RINGGA DEV`,
  meta: [
    { name: 'description', content: newsData.subtitle }
  ]
})

const featured = computed(() => newsData.items[0] || null)
const gridItems = computed(() => newsData.items.slice(1))

const formatDate = (d) => {
  if (!d) return ''
  const dt = new Date(d)
  if (isNaN(dt)) return d
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
