<template>
  <div class="glass-card group relative overflow-hidden rounded-[2rem] p-1.5 transition-all duration-500 hover:-translate-y-2">
    <div class="relative overflow-hidden rounded-[1.7rem] aspect-video">
      <img :src="image" :alt="title" class="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105" />
      <div class="absolute inset-0 bg-gradient-to-t from-[#020408]/90 via-[#020408]/20 to-transparent opacity-80 transition-opacity duration-500 group-hover:opacity-100"></div>
      
      <!-- Overlay Badge -->
      <div class="absolute top-4 right-4 px-3 py-1 rounded-full bg-[#00DC82]/20 backdrop-blur-md border border-[#00DC82]/30 text-[#00DC82] text-[10px] font-black uppercase tracking-wider">
        {{ category }}
      </div>
    </div>
    
    <div class="p-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-2xl font-black group-hover:text-[#00DC82] transition-colors duration-300 leading-tight">
          {{ title }}
        </h3>
        <div class="flex gap-4">
          <a v-if="github" :href="github" target="_blank" class="text-slate-400 hover:text-[#00DC82] transition-colors duration-300 transform hover:scale-110">
            <GithubIcon class="w-5 h-5" />
          </a>
          <a v-if="link" :href="link" target="_blank" class="text-slate-400 hover:text-[#00DC82] transition-colors duration-300 transform hover:scale-110">
            <ExternalLinkIcon class="w-5 h-5" />
          </a>
        </div>
      </div>
      
      <p class="text-slate-400 text-sm leading-relaxed mb-6 line-clamp-2 font-medium">
        {{ description }}
      </p>
      
      <div class="flex flex-wrap gap-2.5">
        <span v-for="tag in tags" :key="tag" class="text-[10px] px-3 py-1.5 rounded-lg bg-slate-900 text-[#00DC82] font-bold border border-slate-800 transition-all duration-300 hover:border-[#00DC82]/50">
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
