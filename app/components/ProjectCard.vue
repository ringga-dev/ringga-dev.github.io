<template>
  <div class="glass-card group relative overflow-hidden rounded-3xl p-1">
    <div class="relative overflow-hidden rounded-[22px] aspect-video">
      <img :src="image" :alt="title" class="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110" />
      <div class="absolute inset-0 bg-gradient-to-t from-[#030014] via-transparent to-transparent opacity-60"></div>
    </div>
    
    <div class="p-6">
      <div class="flex items-center justify-between mb-2">
        <span class="text-[10px] font-bold uppercase tracking-widest text-purple-400">{{ category }}</span>
        <div class="flex gap-2">
          <a v-if="github" :href="github" target="_blank" class="text-white/40 hover:text-white transition-colors">
            <GithubIcon class="w-4 h-4" />
          </a>
          <a v-if="link" :href="link" target="_blank" class="text-white/40 hover:text-white transition-colors">
            <ExternalLinkIcon class="w-4 h-4" />
          </a>
        </div>
      </div>
      
      <h3 class="text-xl font-bold mb-2 group-hover:text-purple-400 transition-colors">{{ title }}</h3>
      <p class="text-white/50 text-sm line-clamp-2 mb-4">{{ description }}</p>
      
      <div class="flex flex-wrap gap-2">
        <span v-for="tag in tags" :key="tag" class="text-[10px] px-2 py-1 rounded-md bg-white/5 text-white/60 border border-white/5">
          {{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { GithubIcon, ExternalLinkIcon } from 'lucide-vue-next'

defineProps({
  title: String,
  description: String,
  image: String,
  category: String,
  tags: Array,
  github: String,
  link: String
})
</script>
