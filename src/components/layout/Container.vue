<template>
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
