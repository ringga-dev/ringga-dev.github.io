<template>
  <div
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    class="riso-card group relative overflow-hidden"
  >
    <!-- Image/Video Media Section -->
    <NuxtLink :to="`/projects/${slug}`" class="relative overflow-hidden aspect-[16/10] bg-surface-elevated border-b border-ink/70 block">
      <MediaLoader
        :media="resolvedMedia"
        :alt-text="title"
        :hover-play="true"
        :is-hovered="isHovered"
      />

      <!-- Category: printed plate label, rotated slightly -->
      <span class="absolute top-3 left-3 z-20 font-mono text-[10px] uppercase tracking-[0.18em] text-paper bg-ink px-2 py-1 rotate-stamp-l inline-block">
        {{ category }}
      </span>
    </NuxtLink>

    <!-- Content Section -->
    <div class="p-6">
      <div class="flex items-start justify-between gap-4 mb-3">
        <NuxtLink :to="`/projects/${slug}`" class="group/title">
          <h3 class="text-xl font-display font-bold group-hover/title:text-brand transition-colors duration-150 leading-tight text-main">
            {{ title }}
          </h3>
        </NuxtLink>
        <div class="flex gap-2 relative z-20 shrink-0">
          <a
            v-if="github"
            :href="github"
            target="_blank"
            rel="noopener"
            class="w-9 h-9 rounded-sm border-[1.5px] border-ink/70 flex items-center justify-center text-muted hover:text-brand hover:border-brand transition-colors"
            aria-label="GitHub Repository"
          >
            <GithubIcon class="w-4 h-4" />
          </a>
          <a
            v-if="link && link !== '#'"
            :href="link"
            target="_blank"
            rel="noopener"
            class="w-9 h-9 rounded-sm border-[1.5px] border-ink/70 flex items-center justify-center text-muted hover:text-brand hover:border-brand transition-colors"
            aria-label="Project Demo Link"
          >
            <ExternalLinkIcon class="w-4 h-4" />
          </a>
        </div>
      </div>

      <p class="text-muted text-sm leading-relaxed mb-6 line-clamp-2 font-serif">
        {{ description }}
      </p>

      <div class="flex flex-wrap gap-2">
        <span
          v-for="tag in tags"
          :key="tag"
          class="font-mono text-[10px] uppercase tracking-[0.1em] px-2.5 py-1 border-[1.5px] border-ink/60 text-muted bg-paper/40"
        >
          {{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { GithubIcon, ExternalLinkIcon } from 'lucide-vue-next'

const isHovered = ref(false)

const props = defineProps({
  title: String,
  slug: String,
  description: String,
  image: String,
  category: String,
  tags: Array,
  github: String,
  link: String,
  media: Object
})

const resolvedMedia = computed(() => {
  // If there's an explicit media object in json, use it, else fallback to standard cover image
  return props.media || { type: 'image', src: props.image || '/images/hero/hero-bg-1.png' }
})
</script>
