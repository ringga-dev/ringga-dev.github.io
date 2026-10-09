<template>
  <div 
    @click="$emit('select', item.id)"
    class="gallery-card group"
    :style="{ animationDelay: `${index * 60}ms` }"
    role="button"
    :aria-label="`View ${item.title} - ${item.category}`"
    tabindex="0"
    @keydown.enter="$emit('select', item.id)"
  >
    <div class="gallery-card-inner">
      <img 
        :src="item.image" 
        :alt="item.title"
        loading="lazy"
        class="gallery-card-image"
      />
      
      <!-- Hover Overlay -->
      <div class="gallery-card-overlay">
        <!-- Zoom Icon -->
        <div class="gallery-zoom-icon">
          <Maximize2Icon class="w-5 h-5" />
        </div>

        <!-- Category Badge -->
        <div class="gallery-card-badge">
          {{ item.category }}
        </div>

        <!-- Title Bar -->
        <div class="gallery-card-info">
          <h4 class="gallery-card-title">
            {{ item.title }}
          </h4>
          <p class="gallery-card-subtitle">
            <EyeIcon class="w-3 h-3 inline-block mr-1" />
            View Fullscreen
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { Maximize2Icon, EyeIcon } from 'lucide-vue-next'
import type { LightboxItem } from '~/composables/useLightbox'

defineProps<{
  item: LightboxItem
  index: number
}>()

defineEmits<{
  select: [id: number]
}>()
</script>

<style scoped>
.gallery-card {
  @apply relative cursor-pointer overflow-hidden;
  aspect-ratio: 4 / 3;
}

.gallery-card-inner {
  @apply relative w-full h-full overflow-hidden transition-colors duration-200;
  background: hsl(var(--surface-card) / 0.5);
  border: 1px solid hsl(var(--border-color) / 0.5);
}

.gallery-card:hover .gallery-card-inner {
  border-color: hsl(var(--brand-color) / 0.6);
}

.gallery-card-image {
  @apply w-full h-full object-cover object-top transition-all duration-700 ease-out;
}

.gallery-card:hover .gallery-card-image {
  filter: brightness(0.8);
}

.gallery-card-overlay {
  @apply absolute inset-0 flex flex-col justify-end p-3 sm:p-4 opacity-0 transition-opacity duration-300;
  background: linear-gradient(
    to top,
    hsl(var(--bg-color) / 0.95) 0%,
    hsl(var(--bg-color) / 0.5) 40%,
    transparent 100%
  );
}

.gallery-card:hover .gallery-card-overlay {
  opacity: 1;
}

.gallery-zoom-icon {
  @apply absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded flex items-center justify-center transition-opacity duration-200;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.12);
  border: 1px solid hsl(var(--brand-color) / 0.35);
  transform: translate(-50%, -50%);
  opacity: 0;
}

.gallery-card:hover .gallery-zoom-icon {
  opacity: 1;
}

.gallery-card-badge {
  @apply absolute top-3 left-3 text-[8px] sm:text-[9px] font-mono font-semibold uppercase tracking-[0.15em] px-2 py-0.5 rounded;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.12);
  border: 1px solid hsl(var(--brand-color) / 0.3);
  opacity: 0;
}

.gallery-card:hover .gallery-card-badge {
  opacity: 1;
}

.gallery-card-title {
  @apply text-white text-xs sm:text-sm font-display font-semibold leading-tight;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.gallery-card-subtitle {
  @apply text-[8px] sm:text-[9px] font-mono uppercase tracking-[0.15em] mt-1 flex items-center;
  color: hsl(var(--brand-light));
}
</style>
