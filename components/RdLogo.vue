<template>
  <div class="relative group cursor-pointer" :class="sizeClass">
    <!-- Animated Outer Ring -->
    <div class="absolute inset-0 rounded-full border-2 border-brand/5 scale-110 group-hover:scale-125 group-hover:border-brand/20 transition-all duration-700"></div>
    
    <svg viewBox="0 0 100 100" class="w-full h-full relative z-10 overflow-visible">
      <defs>
        <linearGradient id="premiumGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#00DC82;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#36E4DA;stop-opacity:1" />
        </linearGradient>
        <filter id="premiumGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      <!-- Main Logo Path: RD Integrated Monogram -->
      <path 
        d="M32 28 V72 M32 28 H48 C58 28 58 48 48 48 H32 M48 48 L58 72 M62 28 V72 M62 28 H75 C88 28 88 72 75 72 H62" 
        fill="none" 
        stroke="url(#premiumGrad)" 
        stroke-width="7" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        filter="url(#premiumGlow)"
        class="transition-all duration-500 group-hover:stroke-white"
      />

      <!-- Vision Dots: Representing Multi-platform nodes -->
      <circle cx="32" cy="28" r="3" class="fill-white group-hover:fill-brand transition-colors" />
      <circle cx="58" cy="72" r="3" class="fill-white group-hover:fill-brand-light transition-colors" />
      <circle cx="62" cy="28" r="3" class="fill-white group-hover:fill-brand transition-colors" />
    </svg>

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
