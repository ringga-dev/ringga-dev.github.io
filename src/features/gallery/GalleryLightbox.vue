<template>
  <ClientOnly>
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-400 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-300 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="lightbox-overlay"
          @click.self="close"
          role="dialog"
          aria-modal="true"
          :aria-label="`Image viewer: ${currentItem?.title || ''}`"
        >
          <!-- Top Bar -->
          <div class="lightbox-topbar">
            <div class="flex items-center gap-3 min-w-0">
              <span class="lightbox-category-badge">
                {{ currentItem?.category }}
              </span>
              <h3 class="lightbox-title">
                {{ currentItem?.title }}
              </h3>
            </div>
            <div class="flex items-center gap-2">
              <!-- Counter pill -->
              <div class="lightbox-counter">
                {{ activeIndex + 1 }} / {{ totalItems }}
              </div>
              <button 
                @click="close" 
                class="lightbox-btn lightbox-close-btn"
                aria-label="Close lightbox"
              >
                <XIcon class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Navigation: Previous -->
          <button 
            @click.stop="prev" 
            class="lightbox-nav-btn lightbox-nav-prev"
            aria-label="Previous image"
          >
            <ChevronLeftIcon class="w-6 h-6" />
          </button>

          <!-- Main Image Container -->
          <div class="lightbox-image-container" @click.stop>
            <Transition
              :enter-active-class="imageEnterClass"
              :leave-active-class="imageLeaveClass"
              :enter-from-class="imageEnterFromClass"
              :leave-to-class="imageLeaveToClass"
              enter-to-class="opacity-100 translate-x-0 scale-100"
              leave-from-class="opacity-100 translate-x-0 scale-100"
              mode="out-in"
            >
              <div :key="currentItem?.id" class="lightbox-image-wrapper">
                <!-- Loading skeleton -->
                <div v-if="isImageLoading" class="lightbox-skeleton">
                  <div class="lightbox-skeleton-pulse"></div>
                </div>
                <img
                  v-if="currentItem"
                  :src="currentItem.image"
                  :alt="currentItem.title"
                  class="lightbox-image"
                  :class="{ 'opacity-0': isImageLoading }"
                  @load="onImageLoaded"
                  @error="onImageLoaded"
                  draggable="false"
                />
              </div>
            </Transition>
          </div>

          <!-- Navigation: Next -->
          <button 
            @click.stop="next" 
            class="lightbox-nav-btn lightbox-nav-next"
            aria-label="Next image"
          >
            <ChevronRightIcon class="w-6 h-6" />
          </button>

          <!-- Bottom Thumbnail Strip -->
          <div class="lightbox-thumbnail-strip" @click.stop>
            <div class="lightbox-thumbnail-track">
              <button
                v-for="(item, idx) in items"
                :key="item.id"
                @click="jumpTo(item.id)"
                class="lightbox-thumbnail"
                :class="{ 'lightbox-thumbnail-active': idx === activeIndex }"
                :aria-label="`View ${item.title}`"
              >
                <img 
                  :src="item.image" 
                  :alt="item.title"
                  class="w-full h-full object-cover object-top"
                  loading="lazy"
                  draggable="false"
                />
              </button>
            </div>
          </div>

          <!-- Touch swipe hint (mobile) -->
          <div class="lightbox-swipe-hint sm:hidden">
            <ChevronLeftIcon class="w-3 h-3 opacity-40" />
            <span>Swipe to navigate</span>
            <ChevronRightIcon class="w-3 h-3 opacity-40" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { XIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next'
import type { LightboxItem } from '~/composables/useLightbox'

const props = defineProps<{
  items: LightboxItem[]
  activeIndex: number
  isOpen: boolean
  currentItem: LightboxItem | null
  totalItems: number
  direction: 'next' | 'prev' | 'none'
}>()

const emit = defineEmits<{
  close: []
  next: []
  prev: []
  jumpTo: [id: number]
}>()

const close = () => emit('close')
const next = () => emit('next')
const prev = () => emit('prev')
const jumpTo = (id: number) => emit('jumpTo', id)

// Image loading state
const isImageLoading = ref(false)

watch(() => props.currentItem?.id, () => {
  isImageLoading.value = true
})

const onImageLoaded = () => {
  isImageLoading.value = false
}

// Directional transition classes
const imageEnterClass = computed(() => 'transition-all duration-350 ease-out')
const imageLeaveClass = computed(() => 'transition-all duration-200 ease-in')

const imageEnterFromClass = computed(() => {
  if (props.direction === 'next') return 'opacity-0 translate-x-8 scale-95'
  if (props.direction === 'prev') return 'opacity-0 -translate-x-8 scale-95'
  return 'opacity-0 scale-90'
})

const imageLeaveToClass = computed(() => {
  if (props.direction === 'next') return 'opacity-0 -translate-x-8 scale-95'
  if (props.direction === 'prev') return 'opacity-0 translate-x-8 scale-95'
  return 'opacity-0 scale-90'
})

// Touch/Swipe support
let touchStartX = 0
let touchStartY = 0
let isSwiping = false

const handleTouchStart = (e: TouchEvent) => {
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
  isSwiping = true
}

const handleTouchEnd = (e: TouchEvent) => {
  if (!isSwiping) return
  const deltaX = e.changedTouches[0].clientX - touchStartX
  const deltaY = e.changedTouches[0].clientY - touchStartY
  
  // Only respond to horizontal swipes (angle check)
  if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
    if (deltaX > 0) {
      prev()
    } else {
      next()
    }
  }
  isSwiping = false
}

onMounted(() => {
  document.addEventListener('touchstart', handleTouchStart, { passive: true })
  document.addEventListener('touchend', handleTouchEnd, { passive: true })
})

onUnmounted(() => {
  document.removeEventListener('touchstart', handleTouchStart)
  document.removeEventListener('touchend', handleTouchEnd)
})
</script>

<style scoped>
/*
 * LIGHTBOX STYLES
 * The overlay is ALWAYS dark regardless of light/dark mode.
 * All colors inside use FIXED dark-friendly values — NOT CSS variables
 * that change per theme — so buttons/badges stay visible in both modes.
 */

.lightbox-overlay {
  @apply fixed inset-0 z-[100] flex items-center justify-center select-none;
  /* Flat, near-opaque ink stock. No backdrop blur, no glow. */
  background: hsl(36 24% 5% / 0.97);
}

.lightbox-topbar {
  @apply absolute top-0 inset-x-0 px-4 sm:px-8 py-5 flex items-center justify-between z-30;
  border-bottom: 1.5px solid hsl(32 16% 22%);
}

.lightbox-category-badge {
  @apply inline-flex items-center font-mono text-[9px] font-bold uppercase tracking-[0.18em] px-2 py-1 shrink-0;
  color: hsl(var(--brand-light));
  border: 2px solid hsl(var(--brand-color));
  border-radius: 2px;
  transform: rotate(-2.5deg);
  box-shadow: 1px 1px 0 hsl(var(--brand-color) / 0.4);
}

.lightbox-title {
  @apply text-sm sm:text-base font-display font-bold leading-tight truncate;
  color: hsl(36 30% 92%);
  text-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.5);
}

.lightbox-counter {
  @apply font-mono text-[10px] font-bold uppercase tracking-[0.2em] px-3 py-1.5 hidden sm:block;
  color: hsl(32 14% 62%);
  border: 1.5px solid hsl(32 16% 26%);
  border-radius: 2px;
}

.lightbox-btn {
  @apply flex items-center justify-center transition-[transform,box-shadow,border-color,color] duration-150 cursor-pointer w-11 h-11;
  color: hsl(32 14% 62%);
  background: transparent;
  border: 1.5px solid hsl(32 16% 26%);
  border-radius: 2px;
}

.lightbox-btn:hover {
  color: hsl(var(--brand-light));
  border-color: hsl(var(--brand-color));
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0 hsl(var(--brand-color) / 0.6);
}

.lightbox-close-btn {
  @apply w-11 h-11;
  box-shadow: 2px 2px 0 hsl(32 16% 26% / 0.9);
}

.lightbox-nav-btn {
  @apply absolute top-1/2 w-12 h-12 z-20 hidden sm:flex;
  @apply flex items-center justify-center transition-[transform,box-shadow,border-color,color] duration-150 cursor-pointer;
  color: hsl(32 14% 62%);
  background: transparent;
  border: 1.5px solid hsl(32 16% 26%);
  border-radius: 2px;
  transform: translateY(-50%);
}

.lightbox-nav-btn:hover {
  color: hsl(var(--brand-light));
  border-color: hsl(var(--brand-color));
  transform: translate(-1px, -50%);
  box-shadow: 3px 3px 0 hsl(var(--brand-color) / 0.6);
}

.lightbox-nav-prev {
  @apply left-3 sm:left-6;
}

.lightbox-nav-next {
  @apply right-3 sm:right-6;
}

.lightbox-image-container {
  @apply relative flex items-center justify-center;
  max-width: calc(100vw - 2rem);
  max-height: calc(100vh - 12rem);
}

@media (min-width: 640px) {
  .lightbox-image-container {
    max-width: calc(100vw - 10rem);
    max-height: calc(100vh - 10rem);
  }
}

.lightbox-image-wrapper {
  @apply relative flex items-center justify-center;
}

.lightbox-image {
  @apply object-contain select-none pointer-events-none transition-opacity duration-300;
  max-width: calc(100vw - 2rem);
  max-height: calc(100vh - 12rem);
  border: 1.5px solid hsl(32 16% 22%);
  box-shadow: 6px 6px 0 hsl(var(--brand-color) / 0.35);
}

@media (min-width: 640px) {
  .lightbox-image {
    max-width: calc(100vw - 10rem);
    max-height: calc(100vh - 10rem);
  }
}

.lightbox-skeleton {
  @apply absolute inset-0 overflow-hidden;
  background: hsl(32 16% 12%);
  min-width: 300px;
  min-height: 200px;
}

/* Halftone sweep instead of a shimmer gradient: the riso screen. */
.lightbox-skeleton-pulse {
  @apply absolute inset-0;
  background-image: radial-gradient(
    hsl(32 16% 24%) 1.1px,
    transparent 1.3px
  );
  background-size: 7px 7px;
  animation: skeleton-sweep 1.5s steps(12, end) infinite;
}

@keyframes skeleton-sweep {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Thumbnail strip */
.lightbox-thumbnail-strip {
  @apply absolute bottom-14 sm:bottom-6 inset-x-0 z-20 flex justify-center px-4;
}

.lightbox-thumbnail-track {
  @apply flex gap-1.5 sm:gap-2 overflow-x-auto py-2 px-2 max-w-full;
  background: transparent;
  border: 1.5px solid hsl(32 16% 22%);
  border-radius: 2px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.lightbox-thumbnail-track::-webkit-scrollbar {
  display: none;
}

.lightbox-thumbnail {
  @apply w-10 h-8 sm:w-14 sm:h-10 overflow-hidden shrink-0 transition-[transform,box-shadow,opacity] duration-150 cursor-pointer;
  border: 1.5px solid transparent;
  border-radius: 2px;
  opacity: 0.4;
  filter: grayscale(0.6);
}

.lightbox-thumbnail:hover {
  opacity: 0.7;
  filter: grayscale(0.2);
  transform: translateY(-2px);
  box-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.5);
}

.lightbox-thumbnail-active {
  opacity: 1 !important;
  filter: grayscale(0) !important;
  border-color: hsl(var(--brand-color)) !important;
  box-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.8) !important;
}

/* Swipe hint */
.lightbox-swipe-hint {
  @apply absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center gap-2 font-mono text-[9px] uppercase tracking-widest z-20;
  color: hsl(32 14% 45%);
}

/* Transition utility classes */
.translate-x-8 {
  transform: translateX(2rem);
}
.-translate-x-8 {
  transform: translateX(-2rem);
}
.scale-95 {
  transform: scale(0.95);
}
.scale-90 {
  transform: scale(0.9);
}
</style>
