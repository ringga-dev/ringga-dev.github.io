<template>
  <div
    :class="[
      'relative overflow-hidden rounded-2xl transition-all duration-500',
      'bg-surface border border-border',
      'hover:border-brand/30 hover:shadow-xl hover:shadow-brand/5',
      'group',
      className
    ]"
  >
    <!-- Spotlight effect -->
    <div
      ref="spotlightRef"
      class="pointer-events-none absolute -inset-px opacity-0 transition-opacity duration-300 group-hover:opacity-100"
      style="background: radial-gradient(600px circle at var(--x) var(--y), rgba(0, 220, 132, 0.1), transparent 40%)"
    ></div>
    
    <!-- Content -->
    <div class="relative z-10">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  className?: string
}

defineProps<Props>()

const spotlightRef = ref<HTMLElement | null>(null)

const handleMouseMove = (event: MouseEvent) => {
  if (!spotlightRef.value) return
  
  const rect = spotlightRef.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  spotlightRef.value.style.setProperty('--x', `${x}px`)
  spotlightRef.value.style.setProperty('--y', `${y}px`)
}
</script>

<style scoped>
.group:hover .pointer-events-none {
  opacity: 1;
}
</style>
