<template>
  <!-- Structural section wrapper. Riso treatment is opt-in per call site via
       className so the printed-page rhythm stays varied (RHYTHM 3): pass
       'halftone' for a dot field, or rely on the vermilion tick. -->
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
