<template>
  <section :class="['py-16 md:py-24 relative', className]">
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
