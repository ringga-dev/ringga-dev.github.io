<template>
  <div 
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    class="glass-card group relative overflow-hidden rounded-[2.5rem] p-2 transition-all duration-500 hover:-translate-y-3 hover:shadow-2xl hover:shadow-brand/10 bg-surface-card border border-border"
  >
    <!-- Image/Video Media Section -->
    <NuxtLink :to="`/projects/${slug}`" class="relative overflow-hidden rounded-[2rem] aspect-[16/10] bg-surface-elevated border border-border z-10 block">
      <MediaLoader 
        :media="resolvedMedia" 
        :alt-text="title"
        :hover-play="true"
        :is-hovered="isHovered"
      />
      
      <!-- Overlay Badge -->
      <div class="absolute top-5 right-5 px-4 py-1.5 rounded-xl bg-surface/80 backdrop-blur-md border border-border text-brand text-[9px] font-black uppercase tracking-widest z-20">
        {{ category }}
      </div>
    </NuxtLink>
    
    <!-- Content Section -->
    <div class="p-8">
      <div class="flex items-center justify-between mb-4">
        <NuxtLink :to="`/projects/${slug}`" class="group/title">
          <h3 class="text-2xl font-heading font-black group-hover/title:text-brand transition-colors duration-300 leading-tight text-main">
            {{ title }}
          </h3>
        </NuxtLink>
        <div class="flex gap-3 relative z-20">
          <a 
            v-if="github" 
            :href="github" 
            target="_blank" 
            class="w-10 h-10 rounded-xl bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/35 transition-all transform hover:scale-110"
            aria-label="GitHub Repository"
          >
            <GithubIcon class="w-5 h-5" />
          </a>
          <a 
            v-if="link && link !== '#'" 
            :href="link" 
            target="_blank" 
            class="w-10 h-10 rounded-xl bg-surface-elevated border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/35 transition-all transform hover:scale-110"
            aria-label="Project Demo Link"
          >
            <ExternalLinkIcon class="w-5 h-5" />
          </a>
        </div>
      </div>
      
      <p class="text-muted text-sm leading-relaxed mb-8 line-clamp-2 font-medium">
        {{ description }}
      </p>
      
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="tag in tags" 
          :key="tag" 
          class="text-[9px] px-3 py-1.5 rounded-lg bg-surface-elevated text-main font-black uppercase tracking-widest border border-border transition-all duration-300 hover:border-brand/50 hover:text-brand"
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
