<template>
  <div class="mb-10 md:mb-14" :class="[centered ? 'text-center' : 'text-left']">
    <!-- Editorial eyebrow: mono label, no pill, no glow, no border. -->
    <div v-if="badge" class="eyebrow mb-3">
      {{ badge }}
    </div>
    <h2 class="mb-4 text-main max-w-3xl" :class="[centered ? 'mx-auto' : '']">
      <slot name="title"></slot>
    </h2>
    <div
      v-if="description"
      class="text-muted text-base md:text-lg leading-relaxed max-w-2xl font-serif"
      :class="[centered ? 'mx-auto' : '']"
    >
      {{ description }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  badge: String,
  description: String,
  centered: {
    type: Boolean,
    default: false
  }
})
</script>
