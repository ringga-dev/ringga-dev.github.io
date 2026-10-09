<template>
  <div class="relative" :class="sizeClass">
    <img
      src="/images/branding/logo-minimal.jpeg"
      alt="Ringga Dev Logo"
      @error="hasError = true"
      v-if="!hasError"
      class="w-full h-full object-cover rounded-full border border-border"
    />

    <!-- Fallback if logo-minimal.jpeg is missing -->
    <div
      v-else
      class="w-full h-full rounded-full bg-surface-card border border-border flex items-center justify-center text-brand font-display font-semibold tracking-tight"
      :class="textClass"
    >
      RD
    </div>
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
