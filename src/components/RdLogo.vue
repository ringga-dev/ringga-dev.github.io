<template>
  <div class="relative group cursor-pointer" :class="sizeClass">
    <!-- Animated Outer Ring -->
    <div class="absolute inset-0 rounded-full border-2 border-brand/10 scale-110 group-hover:scale-125 group-hover:border-brand/35 transition-all duration-700"></div>
    
    <img 
      src="/images/branding/logo-minimal.jpeg" 
      alt="Ringga Dev Logo" 
      @error="hasError = true"
      v-if="!hasError"
      class="w-full h-full object-cover relative z-10 rounded-full transition-all duration-500 group-hover:scale-110"
    />
    
    <!-- Fallback if logo-minimal.jpeg is missing -->
    <div 
      v-else
      class="w-full h-full relative z-10 rounded-full bg-brand/10 border border-brand/30 flex items-center justify-center text-brand font-heading font-black tracking-tighter transition-all duration-500 group-hover:scale-110"
      :class="textClass"
    >
      RD
    </div>
    
    <!-- Background Glow on Hover -->
    <div class="absolute inset-0 bg-brand/10 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const hasError = ref(false)

const props = defineProps({
  size: {
    type: String,
    default: 'md'
  }
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-10 h-10'
    case 'lg': return 'w-20 h-20'
    default: return 'w-14 h-14'
  }
})

const textClass = computed(() => {
  switch (props.size) {
    case 'sm': return 'text-sm'
    case 'lg': return 'text-2xl'
    default: return 'text-lg'
  }
})
</script>
