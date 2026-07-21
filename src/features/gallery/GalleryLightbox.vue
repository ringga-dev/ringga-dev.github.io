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
          <!-- Ambient glow based on brand color -->
          <div class="lightbox-ambient-glow"></div>

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
  background: rgba(2, 6, 4, 0.97);
  backdrop-filter: blur(40px) saturate(0.6);
}

.lightbox-ambient-glow {
  @apply absolute inset-0 pointer-events-none;
  background: 
    radial-gradient(ellipse 60% 40% at 50% 50%, hsl(var(--brand-color) / 0.05) 0%, transparent 70%),
    radial-gradient(ellipse 80% 60% at 30% 80%, hsl(var(--brand-light) / 0.025) 0%, transparent 50%);
}

.lightbox-topbar {
  @apply absolute top-0 inset-x-0 px-4 sm:px-8 py-5 flex items-center justify-between z-30;
  background: linear-gradient(to bottom, rgba(2, 6, 4, 0.9) 0%, transparent 100%);
}

.lightbox-category-badge {
  @apply text-[9px] font-black uppercase tracking-[0.15em] px-3 py-1 rounded-lg shrink-0;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.1);
  border: 1px solid hsl(var(--brand-color) / 0.25);
}

.lightbox-title {
  @apply text-white text-sm sm:text-lg font-heading font-bold leading-tight truncate;
}

.lightbox-counter {
  @apply text-[10px] font-black uppercase tracking-[0.2em] px-3 py-1.5 rounded-lg hidden sm:block;
  color: rgba(180, 200, 190, 0.7);
  background: rgba(15, 30, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.lightbox-btn {
  @apply flex items-center justify-center rounded-xl transition-all duration-300 cursor-pointer active:scale-90;
  color: rgba(180, 200, 190, 0.8);
  background: rgba(15, 30, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
}

.lightbox-btn:hover {
  color: hsl(var(--brand-color));
  background: rgba(15, 30, 22, 0.85);
  border-color: hsl(var(--brand-color) / 0.35);
  box-shadow: 0 0 20px hsl(var(--brand-color) / 0.15);
}

.lightbox-close-btn {
  @apply w-11 h-11;
}

.lightbox-nav-btn {
  @apply absolute top-1/2 -translate-y-1/2 w-12 h-12 z-20 hidden sm:flex;
  @apply flex items-center justify-center rounded-xl transition-all duration-300 cursor-pointer active:scale-90;
  color: rgba(180, 200, 190, 0.8);
  background: rgba(15, 30, 22, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
}

.lightbox-nav-btn:hover {
  color: hsl(var(--brand-color));
  background: rgba(15, 30, 22, 0.85);
  border-color: hsl(var(--brand-color) / 0.35);
  box-shadow: 0 0 30px hsl(var(--brand-color) / 0.15);
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
  @apply rounded-xl sm:rounded-2xl object-contain select-none pointer-events-none transition-opacity duration-300;
  max-width: calc(100vw - 2rem);
  max-height: calc(100vh - 12rem);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.03),
    0 0 80px hsl(var(--brand-color) / 0.06);
}

@media (min-width: 640px) {
  .lightbox-image {
    max-width: calc(100vw - 10rem);
    max-height: calc(100vh - 10rem);
  }
}

.lightbox-skeleton {
  @apply absolute inset-0 rounded-2xl overflow-hidden;
  background: rgba(15, 30, 22, 0.4);
  min-width: 300px;
  min-height: 200px;
}

.lightbox-skeleton-pulse {
  @apply absolute inset-0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(30, 60, 45, 0.2) 50%,
    transparent 100%
  );
  animation: skeleton-sweep 1.5s ease-in-out infinite;
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
  @apply flex gap-1.5 sm:gap-2 overflow-x-auto py-2 px-2 rounded-xl max-w-full;
  background: rgba(10, 20, 15, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(16px);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.lightbox-thumbnail-track::-webkit-scrollbar {
  display: none;
}

.lightbox-thumbnail {
  @apply w-10 h-8 sm:w-14 sm:h-10 rounded-md sm:rounded-lg overflow-hidden shrink-0 transition-all duration-300 cursor-pointer;
  border: 2px solid transparent;
  opacity: 0.4;
  filter: grayscale(0.6);
}

.lightbox-thumbnail:hover {
  opacity: 0.7;
  filter: grayscale(0.2);
}

.lightbox-thumbnail-active {
  opacity: 1 !important;
  filter: grayscale(0) !important;
  border-color: hsl(var(--brand-color)) !important;
  box-shadow: 0 0 12px hsl(var(--brand-color) / 0.3);
}

/* Swipe hint */
.lightbox-swipe-hint {
  @apply absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center gap-2 text-[9px] font-black uppercase tracking-widest z-20;
  color: rgba(180, 200, 190, 0.4);
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
