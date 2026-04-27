<template>
  <div class="relative group cursor-pointer" :class="sizeClass">
    <!-- Animated Outer Ring -->
    <div class="absolute inset-0 rounded-full border-2 border-brand/5 scale-110 group-hover:scale-125 group-hover:border-brand/20 transition-all duration-700"></div>
    
    <img 
      src="/images/branding/logo-minimal.jpeg" 
      alt="Ringga Dev Logo" 
      class="w-full h-full object-contain relative z-10 rounded-full transition-all duration-500 group-hover:scale-110"
    />
    <!-- Background Glow on Hover -->
    <div class="absolute inset-0 bg-brand/10 rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md'
  }
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-8 h-8'
    case 'lg': return 'w-20 h-20'
    default: return 'w-14 h-14'
  }
})
</script>
