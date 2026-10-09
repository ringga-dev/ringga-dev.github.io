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
    <div
      class="gallery-card-inner w-full h-full overflow-hidden"
      :class="index % 2 === 1 ? 'riso-card-2' : 'riso-card'"
    >
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
  @apply relative cursor-pointer;
  aspect-ratio: 4 / 3;
}

.gallery-card-inner {
  @apply relative;
}

/* Keyboard focus reads as a printed plate edge: vermilion, offset. */
.gallery-card:focus-visible {
  outline: none;
}

.gallery-card:focus-visible .gallery-card-inner {
  outline: 2px solid hsl(var(--brand-color));
  outline-offset: 3px;
}

.gallery-card-image {
  @apply w-full h-full object-cover object-top transition-[filter] duration-150;
}

.gallery-card:hover .gallery-card-image {
  filter: brightness(0.82) contrast(1.05);
}

/* Flat ink wash on hover. No gradient scrim, no glow. */
.gallery-card-overlay {
  @apply absolute inset-0 flex flex-col justify-end p-3 sm:p-4 opacity-0 transition-opacity duration-150;
  background: hsl(var(--text-main) / 0.55);
}

.gallery-card:hover .gallery-card-overlay,
.gallery-card:focus-visible .gallery-card-overlay {
  opacity: 1;
}

/* Icon box: square, ink hairline, tiny hard offset shadow. */
.gallery-zoom-icon {
  @apply absolute top-1/2 left-1/2 w-12 h-12 rounded-sm flex items-center justify-center opacity-0 transition-opacity duration-150;
  color: hsl(var(--text-main));
  background: hsl(var(--bg-color));
  border: 1.5px solid hsl(var(--text-main));
  box-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.6);
  transform: translate(-50%, -50%);
}

.gallery-card:hover .gallery-zoom-icon,
.gallery-card:focus-visible .gallery-zoom-icon {
  opacity: 1;
}

/* Category label: rotated rubber stamp, square corners, hard shadow. */
.gallery-card-badge {
  @apply absolute top-3 left-3 font-mono text-[9px] font-bold uppercase tracking-[0.18em] px-2 py-1 opacity-0 transition-opacity duration-150;
  color: hsl(var(--text-main));
  background: hsl(var(--bg-color));
  border: 2px solid hsl(var(--text-main));
  border-radius: 2px;
  transform: rotate(-2.5deg);
  box-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.55);
}

.gallery-card:hover .gallery-card-badge,
.gallery-card:focus-visible .gallery-card-badge {
  opacity: 1;
}

/* Title bar: solid ink block, paper text, vermilion misregister ghost. */
.gallery-card-info {
  @apply p-2.5;
  background: hsl(var(--text-main));
  border: 1.5px solid hsl(var(--bg-color));
}

.gallery-card-title {
  @apply text-xs sm:text-sm font-display font-bold leading-tight;
  color: hsl(var(--bg-color));
  text-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.75);
}

.gallery-card-subtitle {
  @apply text-[8px] sm:text-[9px] font-mono uppercase tracking-[0.15em] mt-1 flex items-center;
  color: hsl(var(--brand-light));
}
</style>
