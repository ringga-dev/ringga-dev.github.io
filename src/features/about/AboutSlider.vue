<template>
  <section class="py-20 relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-6 mb-12">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <span class="text-primary font-medium tracking-wider uppercase text-sm mb-3 block">
            {{ sliderData.title }}
          </span>
          <h2 class="text-4xl md:text-5xl font-bold text-content-primary">
            {{ sliderData.subtitle }}
          </h2>
        </div>
        <div class="flex gap-4">
          <button 
            @click="prev" 
            class="p-4 rounded-full border border-content-secondary/20 hover:border-primary text-content-primary hover:text-primary transition-all duration-300 group bg-surface/50 backdrop-blur-sm"
            aria-label="Previous slide"
          >
            <ChevronLeftIcon class="w-6 h-6 group-hover:-translate-x-1 transition-transform" />
          </button>
          <button 
            @click="next" 
            class="p-4 rounded-full border border-content-secondary/20 hover:border-primary text-content-primary hover:text-primary transition-all duration-300 group bg-surface/50 backdrop-blur-sm"
            aria-label="Next slide"
          >
            <ChevronRightIcon class="w-6 h-6 group-hover:translate-x-1 transition-transform" />
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
        class="flex-shrink-0 px-3 transition-all duration-500"
        :style="{ width: `${100 / itemsPerView}%` }"
      >
        <div 
          class="relative aspect-[4/3] rounded-3xl overflow-hidden group shadow-2xl shadow-primary/5"
          :class="{ 'scale-95 opacity-50': index !== currentIndex && itemsPerView === 1 }"
        >
          <MediaLoader
            :media="{ type: 'image', src: img }"
            :alt-text="`About Image ${index + 1}`"
            class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-110"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500">
            <div class="absolute bottom-8 left-8">
              <p class="text-white font-medium text-lg">Moments of Creation</p>
              <p class="text-white/70 text-sm">Professional Journey</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="max-w-7xl mx-auto px-6 mt-12">
      <div class="h-1.5 w-full bg-content-secondary/10 rounded-full overflow-hidden">
        <div 
          class="h-full bg-primary transition-all duration-500 ease-out"
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
