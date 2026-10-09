<template>
  <!-- Structural width wrapper. Keep it clean: no rounding, no shadows.
       Page rhythm is set by the sections that use it. -->
  <div :class="['max-w-7xl mx-auto px-6', className]">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  className?: string
}

defineProps<Props>()
</script>
