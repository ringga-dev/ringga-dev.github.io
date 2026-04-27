<template>
  <div class="glass-card group relative overflow-hidden rounded-[2.5rem] p-2 transition-all duration-500 hover:-translate-y-3 hover:shadow-2xl hover:shadow-brand/10">
    <!-- Image Section -->
    <div class="relative overflow-hidden rounded-[2rem] aspect-[16/10] bg-slate-900/50 border border-white/5">
      <!-- Shimmer Placeholder -->
      <div v-if="!imageLoaded" class="absolute inset-0 shimmer z-10"></div>
      
      <!-- Fallback UI -->
      <div v-if="imageError" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-900 text-slate-700">
        <BoxIcon class="w-12 h-12 mb-2 opacity-20" />
        <span class="text-[10px] font-black uppercase tracking-widest opacity-30">Preview Unavailable</span>
      </div>

      <img 
        :src="image" 
        :alt="title" 
        loading="lazy"
        @load="handleLoad"
        @error="handleError"
        class="object-cover w-full h-full transition-all duration-700 group-hover:scale-110" 
        :class="[imageLoaded && !imageError ? 'opacity-100' : 'opacity-0']"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-surface via-surface/40 to-transparent opacity-60 transition-opacity duration-500 group-hover:opacity-80"></div>
      
      <!-- Overlay Badge -->
      <div class="absolute top-5 right-5 px-4 py-1.5 rounded-xl bg-surface/80 backdrop-blur-md border border-white/10 text-brand text-[10px] font-black uppercase tracking-widest">
        {{ category }}
      </div>
    </div>
    
    <!-- Content Section -->
    <div class="p-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-2xl font-black group-hover:text-brand transition-colors duration-300 leading-tight">
          {{ title }}
        </h3>
        <div class="flex gap-3">
          <a v-if="github" :href="github" target="_blank" class="w-10 h-10 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-brand hover:border-brand/30 transition-all transform hover:scale-110">
            <GithubIcon class="w-5 h-5" />
          </a>
          <a v-if="link && link !== '#'" :href="link" target="_blank" class="w-10 h-10 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-brand hover:border-brand/30 transition-all transform hover:scale-110">
            <ExternalLinkIcon class="w-5 h-5" />
          </a>
        </div>
      </div>
      
      <p class="text-slate-400 text-sm leading-relaxed mb-8 line-clamp-2 font-medium">
        {{ description }}
      </p>
      
      <div class="flex flex-wrap gap-2">
        <span v-for="tag in tags" :key="tag" class="text-[9px] px-3 py-1.5 rounded-lg bg-white/5 text-slate-300 font-black uppercase tracking-widest border border-white/5 transition-all duration-300 hover:border-brand/50 hover:text-brand">
          {{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { GithubIcon, ExternalLinkIcon, BoxIcon } from 'lucide-vue-next'

const imageLoaded = ref(false)
const imageError = ref(false)

const handleLoad = () => {
  imageLoaded.value = true
}

const handleError = () => {
  imageError.value = true
  imageLoaded.value = true // Stop shimmer
}

onMounted(() => {
  // Check if already loaded (cached)
  const img = new Image()
  img.src = props.image
  if (img.complete) {
    handleLoad()
  }
})

const props = defineProps({
  title: String,
  description: String,
  image: String,
  category: String,
  tags: Array,
  github: String,
  link: String
})
</script>

