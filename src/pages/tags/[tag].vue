<template>
  <div class="min-h-screen pt-28 pb-20 relative overflow-hidden bg-surface">
    <div class="absolute top-[10%] left-[-10%] w-[30vw] h-[30vw] rounded-full blur-[120px] bg-brand/5 pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <!-- Header -->
      <div class="text-center mb-12 animate-reveal">
        <div class="inline-block px-3.5 py-1 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-mono mb-4 uppercase tracking-widest">
          Tag
        </div>
        <h1 class="text-4xl md:text-6xl font-heading font-black tracking-tight leading-none mb-6">
          #<span class="text-gradient">{{ decodedTag }}</span>
        </h1>
        <p class="text-muted max-w-2xl mx-auto text-base md:text-lg font-medium leading-relaxed">
          {{ posts.length }} article{{ posts.length === 1 ? '' : 's' }} tagged with "{{ decodedTag }}".
        </p>
        <NuxtLink to="/blog" class="inline-flex items-center gap-2 mt-6 text-xs font-black uppercase tracking-widest text-brand hover:text-brand-light transition-colors font-mono bg-surface-card/40 border border-brand/20 backdrop-blur-md px-4 py-2.5 rounded-xl hover:border-brand/40">
          <ArrowLeft class="w-4 h-4" /> All Articles
        </NuxtLink>
      </div>

      <!-- Grid -->
      <div v-if="posts.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <NuxtLink
          v-for="(post, index) in posts"
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
            </div>

            <h3 class="text-xl font-heading font-black text-main mb-3 leading-tight group-hover:text-brand transition-colors duration-300 line-clamp-2">
              {{ post.title }}
            </h3>

            <p class="text-muted text-sm leading-relaxed font-semibold mb-6 line-clamp-3">
              {{ post.description }}
            </p>

            <div class="mt-auto pt-5 border-t border-border/40 flex items-center justify-between">
              <span class="text-brand text-xs font-black uppercase tracking-wider flex items-center gap-0.5 group-hover:translate-x-1 transition-transform duration-300">
                Read
                <ArrowRight class="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Empty -->
      <div v-else class="glass-card max-w-xl mx-auto text-center py-16 px-8 border border-border rounded-[2.5rem]">
        <h3 class="text-xl font-heading font-black text-main mb-3">No Articles Found</h3>
        <p class="text-muted text-sm font-semibold">Tag "{{ decodedTag }}" has no posts.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowLeft, Calendar, BookOpen, ArrowRight } from 'lucide-vue-next'
import { useRoute } from '#imports'
import { collectBlogPosts, slugifyTag } from '~/composables/useBlog'

const route = useRoute()
const tagSlug = computed(() => route.params.tag)
const decodedTag = computed(() => {
  // best-effort human label: replace hyphens with spaces, title-ish
  return decodeURIComponent(tagSlug.value).replace(/-/g, ' ')
})

const posts = computed(() => {
  const slug = tagSlug.value
  return collectBlogPosts().filter(p =>
    p.tags.some(tag => slugifyTag(tag) === slug)
  )
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
  title: `#${decodedTag.value} | Tag | Ringga Dev`,
  meta: [
    { name: 'description', content: `Articles tagged with ${decodedTag.value} on Ringga Dev's blog.` },
    { property: 'og:title', content: `#${decodedTag.value} | Tag | Ringga Dev` },
    { property: 'og:type', content: 'website' }
  ]
})
</script>
