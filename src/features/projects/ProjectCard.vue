<template>
  <div
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    class="glass-card group relative overflow-hidden transition-colors duration-200 hover:border-brand/50"
  >
    <!-- Image/Video Media Section -->
    <NuxtLink :to="`/projects/${slug}`" class="relative overflow-hidden aspect-[16/10] bg-surface-elevated border-b border-border block">
      <MediaLoader
        :media="resolvedMedia"
        :alt-text="title"
        :hover-play="true"
        :is-hovered="isHovered"
      />

      <!-- Category label (mono, top-left) -->
      <div class="absolute top-3 left-3 font-mono text-[10px] uppercase tracking-[0.2em] text-paper bg-ink/80 px-2 py-1 z-20">
        {{ category }}
      </div>
    </NuxtLink>

    <!-- Content Section -->
    <div class="p-6">
      <div class="flex items-start justify-between gap-4 mb-3">
        <NuxtLink :to="`/projects/${slug}`" class="group/title">
          <h3 class="text-xl font-display font-semibold group-hover/title:text-brand transition-colors duration-200 leading-tight text-main">
            {{ title }}
          </h3>
        </NuxtLink>
        <div class="flex gap-2 relative z-20 shrink-0">
          <a
            v-if="github"
            :href="github"
            target="_blank"
            rel="noopener"
            class="w-9 h-9 rounded border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand transition-colors"
            aria-label="GitHub Repository"
          >
            <GithubIcon class="w-4 h-4" />
          </a>
          <a
            v-if="link && link !== '#'"
            :href="link"
            target="_blank"
            rel="noopener"
            class="w-9 h-9 rounded border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand transition-colors"
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
          class="font-mono text-[10px] uppercase tracking-[0.1em] px-2.5 py-1 border border-border text-muted"
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
