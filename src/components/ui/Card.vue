<template>
  <div
    :class="[
      'riso-card relative overflow-hidden',
      className
    ]"
  >
    <!-- Content -->
    <div class="relative z-10">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  className?: string
}

defineProps<Props>()
</script>
