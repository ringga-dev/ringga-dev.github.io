<template>
  <section class="max-w-7xl mx-auto px-6 py-28 relative z-10">
    <SectionHeader 
      badge="Core Ecosystem" 
      description="A rotating showcase of the systems, architectures, and integrations I build end-to-end."
      centered
    >
      <template #title>
        Showcase <span class="text-gradient">Highlights</span>
      </template>
    </SectionHeader>

    <div 
      class="mt-16 glass-card rounded-[2.5rem] overflow-hidden border border-border relative group shadow-2xl"
      @mouseenter="pauseAutoplay"
      @mouseleave="startAutoplay"
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
    >
      <!-- Background neon glows -->
      <div 
        class="absolute -top-40 -left-40 w-96 h-96 rounded-full blur-[100px] pointer-events-none transition-all duration-1000"
        :class="activeSlideGlowClass"
      ></div>
      <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-brand-light/10 rounded-full blur-[100px] pointer-events-none group-hover:bg-brand-light/15 transition-colors"></div>

      <div class="relative min-h-[560px] lg:min-h-[460px] flex items-center">
        <Transition
          :name="slideTransitionName"
          mode="out-in"
        >
          <div 
            :key="currentSlideIndex"
            class="grid grid-cols-1 lg:grid-cols-12 gap-10 p-8 sm:p-12 lg:p-16 items-center w-full"
          >
            <!-- Left: Details -->
            <div class="lg:col-span-7 space-y-6 text-left">
              <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-xs font-black tracking-widest uppercase">
                {{ currentSlide.category }}
              </span>

              <h2 class="text-3xl sm:text-4xl md:text-5xl font-heading font-black text-main leading-[1.15] tracking-tight">
                {{ currentSlide.title }} <br />
                <span class="text-gradient">{{ currentSlide.titleHighlight }}</span>
              </h2>

              <p class="text-muted text-base md:text-lg font-medium leading-relaxed max-w-xl">
                {{ currentSlide.description }}
              </p>

              <div class="grid grid-cols-2 gap-6 pt-2">
                <div 
                  v-for="(hl, idx) in currentSlide.highlights" 
                  :key="idx" 
                  class="space-y-1"
                >
                  <h4 class="text-2xl sm:text-3xl font-black text-brand transition-all duration-300">
                    {{ hl.value }}
                  </h4>
                  <p class="text-[10px] sm:text-xs text-muted font-bold uppercase tracking-wider">
                    {{ hl.label }}
                  </p>
                </div>
              </div>

              <div class="flex flex-col sm:flex-row gap-4 pt-2">
                <NuxtLink 
                  :to="currentSlide.ctaLink" 
                  class="btn-primary inline-flex items-center justify-center gap-3 px-8 py-4 text-xs font-black uppercase tracking-wider shadow-lg shadow-brand/10 hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
                >
                  {{ currentSlide.ctaText }}
                  <ArrowRightIcon class="w-4 h-4" />
                </NuxtLink>
                <a 
                  :href="globalData.socials.whatsapp" 
                  target="_blank" 
                  class="btn-secondary inline-flex items-center justify-center gap-3 px-8 py-4 text-xs font-black uppercase tracking-wider"
                >
                  Start Project Discussion
                </a>
              </div>
            </div>

            <!-- Right: Visual -->
            <div class="lg:col-span-5 w-full flex justify-center">
              <div class="relative overflow-hidden rounded-[2rem] border border-border/80 shadow-2xl bg-surface-card w-full aspect-square flex items-center justify-center">
                <div class="absolute inset-0 bg-gradient-to-tr from-brand/20 to-brand-light/0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none z-10"></div>
                
                <img 
                  :src="currentSlide.image" 
                  :alt="currentSlide.title" 
                  class="w-full h-full object-cover transform hover:scale-[1.03] transition-transform duration-700 select-none pointer-events-none"
                />
                
                <div class="absolute bottom-4 left-4 right-4 glass px-5 py-3.5 rounded-2xl border border-border/40 flex items-center justify-between z-20">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2.5 h-2.5 rounded-full bg-brand animate-pulse"></span>
                    <span class="text-[10px] font-black uppercase tracking-widest text-main font-heading">
                      {{ currentSlide.tag }}
                    </span>
                  </div>
                  <span class="text-[9px] font-mono text-muted uppercase">
                    {{ currentSlide.version }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Navigation Arrows -->
      <button 
        @click="prevSlide" 
        class="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-2xl glass border border-border/50 flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 hover:scale-105 active:scale-95 transition-all duration-300 opacity-0 group-hover:opacity-100 z-30 cursor-pointer hidden md:flex"
        aria-label="Previous Slide"
      >
        <ChevronLeftIcon class="w-5 h-5" />
      </button>
      <button 
        @click="nextSlide" 
        class="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-2xl glass border border-border/50 flex items-center justify-center text-muted hover:text-brand hover:border-brand/40 hover:scale-105 active:scale-95 transition-all duration-300 opacity-0 group-hover:opacity-100 z-30 cursor-pointer hidden md:flex"
        aria-label="Next Slide"
      >
        <ChevronRightIcon class="w-5 h-5" />
      </button>

      <!-- Progress dots -->
      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-3 z-30">
        <button 
          v-for="(_, index) in slides" 
          :key="index"
          @click="setSlide(index)"
          class="w-8 h-1.5 rounded-full transition-all duration-300 cursor-pointer"
          :class="index === currentSlideIndex ? 'bg-brand w-12' : 'bg-border hover:bg-muted'"
          :aria-label="`Go to slide ${index + 1}`"
        ></button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ArrowRightIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next'
import globalData from '~/data/global.json'

const slides = [
  {
    category: "Core Ecosystem",
    title: "Universal Engineering.",
    titleHighlight: "No Platform Boundaries.",
    description: "From direct ESC/POS hardware control and socket communications to responsive reactive web layouts and cross-platform mobile apps. I architect complete end-to-end ecosystems designed for durability, lightning speed, and elite design aesthetics.",
    image: "/images/branding/home_showcase_banner.png",
    tag: "Active Architecture",
    version: "Ver. 2.0",
    highlights: [
      { value: "3+ Years", label: "Commercial Track Record" },
      { value: "100%", label: "Custom Performance-First Code" }
    ],
    ctaText: "Browse Applications",
    ctaLink: "/projects"
  },
  {
    category: "Software Design",
    title: "SOLID Architecture.",
    titleHighlight: "Maintainable & Modular.",
    description: "Strict layer separations (Presentation, Application, Domain, and Data) following modern engineering standards. Designed for ultimate stability, testing scalability, and multi-team collaboration.",
    image: "/images/infographics/clean-architecture.png",
    tag: "Modular Blueprint",
    version: "Ver. 1.8",
    highlights: [
      { value: "98%+", label: "Automated Code Coverage" },
      { value: "Clean", label: "Domain-Driven Structures" }
    ],
    ctaText: "See Architecture",
    ctaLink: "/projects"
  },
  {
    category: "Systems & POS integration",
    title: "Low-Level Drivers.",
    titleHighlight: "Hardware & ESC/POS Sockets.",
    description: "Direct Bluetooth, USB, and TCP Sockets driver communication for receipt printing, cash drawers, and commercial peripherals. Fully optimized command buffer rendering and offline queues.",
    image: "/images/infographics/secure-reliable.png",
    tag: "Hardware Buffers",
    version: "Ver. 2.4",
    highlights: [
      { value: "POS Ready", label: "Thermal Printers Sockets" },
      { value: "Offline", label: "Queued Sync Transactions" }
    ],
    ctaText: "Explore POS Projects",
    ctaLink: "/projects"
  },
  {
    category: "Cross-Platform Mobile",
    title: "Native Performance.",
    titleHighlight: "Kotlin Multiplatform Apps.",
    description: "Single-codebase efficiency without compromising native speed or visual precision. Shared business logic compiling directly to native Android SDK and iOS Swift runtime objects.",
    image: "/images/infographics/cross-platform.png",
    tag: "Compose / KMP",
    version: "Ver. 3.0",
    highlights: [
      { value: "Universal", label: "Android & iOS Deployments" },
      { value: "Zero Lag", label: "Direct Native Performance" }
    ],
    ctaText: "View Mobile Apps",
    ctaLink: "/projects"
  }
]

const currentSlideIndex = ref(0)
const direction = ref('next')
const currentSlide = computed(() => slides[currentSlideIndex.value])

const activeSlideGlowClass = computed(() => {
  switch(currentSlideIndex.value) {
    case 1: return 'bg-cyan-500/10 group-hover:bg-cyan-500/15'
    case 2: return 'bg-emerald-500/10 group-hover:bg-emerald-500/15'
    case 3: return 'bg-teal-500/10 group-hover:bg-teal-500/15'
    default: return 'bg-brand/10 group-hover:bg-brand/15'
  }
})

const slideTransitionName = computed(() => {
  return direction.value === 'next' ? 'slide-next' : 'slide-prev'
})

let autoplayTimer = null

const startAutoplay = () => {
  stopAutoplay()
  autoplayTimer = setInterval(() => {
    direction.value = 'next'
    currentSlideIndex.value = (currentSlideIndex.value + 1) % slides.length
  }, 6000)
}

const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

const pauseAutoplay = () => stopAutoplay()

const nextSlide = () => {
  direction.value = 'next'
  currentSlideIndex.value = (currentSlideIndex.value + 1) % slides.length
  startAutoplay()
}

const prevSlide = () => {
  direction.value = 'prev'
  currentSlideIndex.value = (currentSlideIndex.value - 1 + slides.length) % slides.length
  startAutoplay()
}

const setSlide = (index) => {
  direction.value = index > currentSlideIndex.value ? 'next' : 'prev'
  currentSlideIndex.value = index
  startAutoplay()
}

let touchStartX = 0
let touchEndX = 0

const handleTouchStart = (event) => {
  touchStartX = event.changedTouches[0].screenX
}

const handleTouchEnd = (event) => {
  touchEndX = event.changedTouches[0].screenX
  handleSwipeGesture()
}

const handleSwipeGesture = () => {
  const diff = touchStartX - touchEndX
  if (Math.abs(diff) > 50) {
    if (diff > 0) nextSlide()
    else prevSlide()
  }
}

onMounted(() => {
  startAutoplay()
})

onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.slide-next-enter-active,
.slide-next-leave-active,
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-next-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.slide-next-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

.slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-40px);
}
.slide-prev-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
