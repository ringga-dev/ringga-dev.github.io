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

      <!-- Glow border on hover -->
      <div class="gallery-card-glow"></div>
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
  @apply relative cursor-pointer rounded-2xl overflow-hidden;
  aspect-ratio: 4 / 3;
  animation: card-enter 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.gallery-card-inner {
  @apply relative w-full h-full overflow-hidden rounded-2xl transition-all duration-500;
  background: hsl(var(--surface-card) / 0.5);
  border: 1px solid hsl(var(--border-color) / 0.5);
}

.gallery-card:hover .gallery-card-inner {
  border-color: hsl(var(--brand-color) / 0.4);
  transform: translateY(-4px);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px hsl(var(--brand-color) / 0.1),
    0 0 40px hsl(var(--brand-color) / 0.06);
}

.gallery-card-image {
  @apply w-full h-full object-cover object-top transition-all duration-700 ease-out;
}

.gallery-card:hover .gallery-card-image {
  transform: scale(1.08);
  filter: brightness(0.85);
}

.gallery-card-overlay {
  @apply absolute inset-0 flex flex-col justify-end p-3 sm:p-4 opacity-0 transition-all duration-500;
  background: linear-gradient(
    to top,
    rgba(2, 8, 5, 0.92) 0%,
    rgba(2, 8, 5, 0.5) 40%,
    transparent 100%
  );
}

.gallery-card:hover .gallery-card-overlay {
  opacity: 1;
}

.gallery-zoom-icon {
  @apply absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 ease-out;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.12);
  border: 1px solid hsl(var(--brand-color) / 0.35);
  backdrop-filter: blur(12px);
  transform: translate(-50%, -50%) scale(0.7);
  opacity: 0;
}

.gallery-card:hover .gallery-zoom-icon {
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
}

.gallery-card-badge {
  @apply absolute top-3 left-3 text-[8px] sm:text-[9px] font-black uppercase tracking-[0.15em] px-2 py-0.5 rounded-md transition-all duration-500;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.12);
  border: 1px solid hsl(var(--brand-color) / 0.3);
  transform: translateY(-6px);
  opacity: 0;
}

.gallery-card:hover .gallery-card-badge {
  transform: translateY(0);
  opacity: 1;
}

.gallery-card-info {
  @apply transition-all duration-500 ease-out;
  transform: translateY(8px);
}

.gallery-card:hover .gallery-card-info {
  transform: translateY(0);
}

.gallery-card-title {
  @apply text-white text-xs sm:text-sm font-heading font-bold leading-tight;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.gallery-card-subtitle {
  @apply text-[8px] sm:text-[9px] font-black uppercase tracking-[0.15em] mt-1 flex items-center;
  color: hsl(var(--brand-light));
}

.gallery-card-glow {
  @apply absolute inset-0 pointer-events-none rounded-2xl opacity-0 transition-opacity duration-500;
  box-shadow: inset 0 0 30px hsl(var(--brand-color) / 0.06);
}

.gallery-card:hover .gallery-card-glow {
  opacity: 1;
}
</style>
