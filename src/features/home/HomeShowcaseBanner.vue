<template>
  <section class="max-w-7xl mx-auto px-6 py-28 relative z-10">
    <SectionHeader 
      badge="Core Ecosystem" 
      description="A rotating showcase of the systems, architectures, and integrations I build end-to-end."
      centered
    >
      <template #title>
        Showcase <span class="text-brand">Highlights</span>
      </template>
    </SectionHeader>

    <div
      class="mt-12 relative group bg-surface p-2 overflow-hidden"
      @mouseenter="pauseAutoplay"
      @mouseleave="startAutoplay"
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
    >
      <div class="relative min-h-[560px] lg:min-h-[460px] flex items-center">
        <Transition
          :name="slideTransitionName"
          mode="out-in"
        >
          <div
            :key="currentSlideIndex"
            class="riso-card grid grid-cols-1 lg:grid-cols-12 gap-10 p-6 sm:p-10 lg:p-14 items-center w-full"
          >
            <!-- Left: Details -->
            <div class="lg:col-span-7 space-y-5 text-left">
              <span class="stamp">
                {{ currentSlide.category }}
              </span>

              <h2 class="text-3xl sm:text-4xl md:text-5xl font-display font-bold text-main leading-[1.05] tracking-tight">
                {{ currentSlide.title }} <br />
                <span class="text-brand riso-ghost">{{ currentSlide.titleHighlight }}</span>
              </h2>

              <p class="text-muted text-base md:text-lg font-serif leading-relaxed max-w-xl">
                {{ currentSlide.description }}
              </p>

              <div class="grid grid-cols-2 gap-6 pt-2">
                <div
                  v-for="(hl, idx) in currentSlide.highlights"
                  :key="idx"
                  class="space-y-1"
                >
                  <h4 class="numeral text-2xl sm:text-3xl text-brand">
                    {{ hl.value }}
                  </h4>
                  <p class="font-mono text-[10px] sm:text-xs text-muted uppercase tracking-wider">
                    {{ hl.label }}
                  </p>
                </div>
              </div>

              <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <NuxtLink
                  :to="currentSlide.ctaLink"
                  class="btn-primary gap-3 px-7 py-3.5 font-mono text-xs uppercase tracking-[0.15em]"
                >
                  {{ currentSlide.ctaText }}
                </NuxtLink>
                <a
                  :href="globalData.socials.whatsapp"
                  target="_blank"
                  rel="noopener"
                  class="btn-secondary gap-3 px-7 py-3.5 font-mono text-xs uppercase tracking-[0.15em]"
                >
                  Start Project Discussion
                </a>
              </div>
            </div>

            <!-- Right: Visual -->
            <div class="lg:col-span-5 w-full flex justify-center">
              <div class="relative overflow-hidden border-[1.5px] border-ink bg-surface-card w-full aspect-square flex items-center justify-center shadow-riso-2">
                <img
                  :src="currentSlide.image"
                  :alt="currentSlide.title"
                  loading="lazy"
                  decoding="async"
                  class="w-full h-full object-cover select-none pointer-events-none"
                />

                <div class="absolute bottom-0 left-0 right-0 px-5 py-3 border-t-[1.5px] border-ink bg-surface flex items-center justify-between z-20">
                  <div class="flex items-center gap-2.5">
                    <span class="w-2 h-2 bg-brand"></span>
                    <span class="font-mono text-[10px] font-bold uppercase tracking-widest text-main">
                      {{ currentSlide.tag }}
                    </span>
                  </div>
                  <span class="font-mono text-[9px] font-bold text-muted uppercase">
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
        class="absolute left-4 top-1/2 -translate-y-1/2 w-11 h-11 rounded-sm border-[1.5px] border-ink bg-surface flex items-center justify-center text-main hover:text-brand hover:border-brand hover:shadow-riso hover:-translate-x-0.5 transition-[transform,box-shadow,border-color,color] duration-150 z-30 cursor-pointer hidden md:flex"
        aria-label="Previous Slide"
      >
        <ChevronLeftIcon class="w-5 h-5" />
      </button>
      <button
        @click="nextSlide"
        class="absolute right-4 top-1/2 -translate-y-1/2 w-11 h-11 rounded-sm border-[1.5px] border-ink bg-surface flex items-center justify-center text-main hover:text-brand hover:border-brand hover:shadow-riso hover:translate-x-0.5 transition-[transform,box-shadow,border-color,color] duration-150 z-30 cursor-pointer hidden md:flex"
        aria-label="Next Slide"
      >
        <ChevronRightIcon class="w-5 h-5" />
      </button>

      <!-- Progress dots -->
      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2 z-30">
        <button
          v-for="(_, index) in slides"
          :key="index"
          @click="setSlide(index)"
          class="w-6 h-2 rounded-sm border-[1.5px] border-ink/60 bg-surface transition-[transform,box-shadow,background-color,border-color] duration-150 cursor-pointer"
          :class="index === currentSlideIndex ? 'bg-ink border-ink shadow-riso' : 'hover:border-brand hover:shadow-riso'"
          :aria-label="`Go to slide ${index + 1}`"
        ></button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next'
import globalData from '~/data/global.json'

const slides = [
  {
    category: "Core Ecosystem",
    title: "Universal Engineering.",
    titleHighlight: "No Platform Boundaries.",
    description: "From direct ESC/POS hardware control and socket communications to responsive reactive web layouts and cross-platform mobile apps. I architect complete end-to-end ecosystems designed for durability, lightning speed, and elite design aesthetics.",
    image: "/images/branding/home_showcase_banner.webp",
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
    image: "/images/infographics/clean-architecture.webp",
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
    image: "/images/infographics/secure-reliable.webp",
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
    image: "/images/infographics/cross-platform.webp",
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
    case 1: return 'bg-brand-light/10 group-hover:bg-brand-light/15'
    case 2: return 'bg-accent-1/10 group-hover:bg-accent-1/15'
    case 3: return 'bg-accent-2/10 group-hover:bg-accent-2/15'
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
