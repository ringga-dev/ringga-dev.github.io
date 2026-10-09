<template>
  <section class="py-20 relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-6 mb-12">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <span class="eyebrow text-brand mb-3 block">
            {{ sliderData.title }}
          </span>
          <h2 class="text-4xl md:text-5xl font-display font-bold text-main leading-tight">
            {{ sliderData.subtitle }}
          </h2>
        </div>
        <div class="flex gap-4">
          <button
            @click="prev"
            class="p-4 rounded-sm border-[1.5px] border-ink/70 hover:border-brand text-muted hover:text-brand hover:shadow-[3px_3px_0_hsl(var(--brand-color)/0.6)] hover:-translate-x-0.5 hover:-translate-y-0.5 transition-[transform,box-shadow,border-color,color] duration-150 group bg-surface-card"
            aria-label="Previous slide"
          >
            <ChevronLeftIcon class="w-6 h-6 group-hover:-translate-x-1 transition-transform duration-150" />
          </button>
          <button
            @click="next"
            class="p-4 rounded-sm border-[1.5px] border-ink/70 hover:border-brand text-muted hover:text-brand hover:shadow-[3px_3px_0_hsl(var(--brand-color)/0.6)] hover:-translate-x-0.5 hover:-translate-y-0.5 transition-[transform,box-shadow,border-color,color] duration-150 group bg-surface-card"
            aria-label="Next slide"
          >
            <ChevronRightIcon class="w-6 h-6 transition-transform duration-150" />
          </button>
        </div>
      </div>
    </div>

    <div
      class="relative flex transition-transform duration-700 ease-out cursor-grab active:cursor-grabbing"
      :style="{ transform: `translateX(-${currentIndex * (100 / itemsPerView)}%)` }"
      @mousedown="startDrag"
      @touchstart="startDrag"
      @mousemove="onDrag"
      @touchmove="onDrag"
      @mouseup="endDrag"
      @touchend="endDrag"
      @mouseleave="endDrag"
    >
      <div
        v-for="(img, index) in sliderData.images"
        :key="index"
        class="flex-shrink-0 px-3 transition-[opacity] duration-500"
        :style="{ width: `${100 / itemsPerView}%` }"
      >
        <div
          class="relative aspect-[4/3] overflow-hidden group border-[1.5px] border-ink/70 shadow-riso-2 bg-surface-elevated"
          :class="{ 'opacity-40': index !== currentIndex && itemsPerView === 1 }"
        >
          <MediaLoader
            :media="{ type: 'image', src: img }"
            :alt-text="`About Image ${index + 1}`"
            class="w-full h-full object-cover grayscale contrast-125 group-hover:grayscale-0 transition-[filter] duration-300"
          />
          <div class="absolute inset-0 bg-surface/90 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
            <div class="absolute bottom-8 left-8">
              <p class="text-main font-display font-bold text-lg">Moments of Creation</p>
              <p class="eyebrow text-muted">Professional Journey</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="max-w-7xl mx-auto px-6 mt-12">
      <div class="h-2 w-full bg-surface-elevated border-[1.5px] border-ink/70 rounded-sm overflow-hidden">
        <div
          class="h-full bg-brand transition-[width] duration-700 ease-out"
          :style="{ width: `${((currentIndex + 1) / sliderData.images.length) * 100}%` }"
        ></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next'
import aboutData from '~/data/about.json'

const sliderData = aboutData.slider || { title: 'Moments', subtitle: 'Professional Journey', images: [] }
const currentIndex = ref(0)
const itemsPerView = ref(1)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)

const updateItemsPerView = () => {
  if (typeof window === 'undefined') return
  if (window.innerWidth >= 1024) {
    itemsPerView.value = 3
  } else if (window.innerWidth >= 768) {
    itemsPerView.value = 2
  } else {
    itemsPerView.value = 1
  }
}

const next = () => {
  if (!sliderData.images || sliderData.images.length === 0) return
  if (currentIndex.value < sliderData.images.length - itemsPerView.value) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

const prev = () => {
  if (!sliderData.images || sliderData.images.length === 0) return
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = Math.max(0, sliderData.images.length - itemsPerView.value)
  }
}

// Auto play
let autoplayInterval
onMounted(() => {
  updateItemsPerView()
  window.addEventListener('resize', updateItemsPerView)

  autoplayInterval = setInterval(() => {
    if (!isDragging.value) {
      next()
    }
  }, 5000)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateItemsPerView)
  clearInterval(autoplayInterval)
})

// Drag logic
const startDrag = (e) => {
  isDragging.value = true
  startX.value = e.type.includes('touch') ? e.touches[0].pageX : e.pageX
}

const onDrag = (e) => {
  if (!isDragging.value) return
  const x = e.type.includes('touch') ? e.touches[0].pageX : e.pageX
  const walk = (x - startX.value)
  if (Math.abs(walk) > 100) {
    if (walk > 0) prev()
    else next()
    isDragging.value = false
  }
}

const endDrag = () => {
  isDragging.value = false
}
</script>
