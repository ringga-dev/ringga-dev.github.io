<template>
  <section :class="['py-16 md:py-24 relative', className]">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-brand/5 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-brand-light/5 rounded-full blur-[100px]"></div>
    </div>
    
    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  className?: string
}

defineProps<Props>()
</script>
