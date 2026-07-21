<template>
  <section class="max-w-7xl mx-auto px-6 py-24 relative z-10 bg-surface">
    <!-- Section Header -->
    <SectionHeader 
      badge="Technical Methodology" 
      description="Interactive visual blueprints demonstrating my engineering, UI/UX architecture, performance analysis, and operational lifecycles."
      centered
    >
      <template #title>
        Engineering <span class="text-gradient">Blueprints</span>
      </template>
    </SectionHeader>

    <!-- Grid Layout of Capability Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
      <div 
        v-for="(banner, index) in banners" 
        :key="banner.id"
        @click="openLightbox(index)"
        :class="[
          'group relative p-3 rounded-3xl bg-surface-card border border-border hover:border-brand/40 hover:-translate-y-1.5 transition-all duration-300 cursor-pointer scroll-reveal overflow-hidden',
          (index === 0 || index === 5) ? 'lg:col-span-2' : 'lg:col-span-1'
        ]"
        :style="{ transitionDelay: `${(index % 4 + 1) * 80}ms` }"
      >
        <!-- Thumbnail with dynamic aspect based on span -->
        <div :class="['rounded-2xl overflow-hidden relative border border-border/40', (index === 0 || index === 5) ? 'aspect-[16/9] lg:aspect-[21/9]' : 'aspect-[16/10]']">
          <img 
            :src="banner.image" 
            :alt="banner.title"
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            loading="lazy"
          />
          <!-- Category Badge Overlay -->
          <div class="absolute top-3 left-3 px-2.5 py-1 rounded-lg bg-surface-card/80 backdrop-blur border border-border/50 text-[8px] font-black uppercase tracking-widest text-brand opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            {{ banner.category }}
          </div>
          <!-- Hover Zoom Indicator -->
          <div class="absolute inset-0 bg-surface/60 backdrop-blur-[1px] opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
            <div class="bg-brand text-brand-dark p-3 rounded-full shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-all duration-300">
              <Maximize2Icon class="w-5 h-5" />
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="mt-3 px-2 pb-2 flex flex-col gap-1.5">
          <span class="text-[9px] font-black uppercase tracking-widest text-brand/70 block">
            {{ banner.category }}
          </span>
          <h4 :class="['text-sm font-black text-main group-hover:text-brand transition-colors leading-snug', (index === 0 || index === 5) ? 'line-clamp-2' : 'line-clamp-2']">
            {{ banner.title }}
          </h4>
          <p :class="['text-[11px] text-muted font-medium leading-relaxed mt-0.5', (index === 0 || index === 5) ? 'line-clamp-2' : 'line-clamp-7']">
            {{ banner.description }}
          </p>
          <div class="flex items-center gap-1 text-[9px] font-black uppercase tracking-widest text-brand/60 group-hover:text-brand transition-colors mt-1">
            View Details
            <ChevronRightIcon class="w-3 h-3" />
          </div>
        </div>
      </div>
    </div>

    <!-- Fullscreen Lightbox Modal -->
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
            @click.self="closeLightbox"
            role="dialog"
            aria-modal="true"
            :aria-label="`Methodology viewer: ${currentBanner?.title || ''}`"
          >
            <!-- Background glow -->
            <div class="lightbox-ambient-glow"></div>

            <!-- Top Header Bar -->
            <div class="lightbox-topbar">
              <div class="flex items-center gap-3 min-w-0">
                <span class="lightbox-category-badge">
                  {{ currentBanner?.category }}
                </span>
                <h3 class="lightbox-title text-white">
                  {{ currentBanner?.title }}
                </h3>
              </div>
              <div class="flex items-center gap-2">
                <div class="lightbox-counter text-xs">
                  {{ activeIndex + 1 }} / {{ banners.length }}
                </div>
                <button 
                  @click="closeLightbox" 
                  class="lightbox-btn"
                  aria-label="Close modal"
                >
                  <XIcon class="w-5 h-5" />
                </button>
              </div>
            </div>

            <!-- Previous navigation -->
            <button 
              @click="prev" 
              class="lightbox-nav-btn lightbox-nav-prev"
              aria-label="Previous image"
            >
              <ChevronLeftIcon class="w-6 h-6" />
            </button>

            <!-- Image Container -->
            <div class="lightbox-content-container" @click.stop>
              <Transition
                :enter-active-class="imageEnterClass"
                :leave-active-class="imageLeaveClass"
                :enter-from-class="imageEnterFromClass"
                :leave-to-class="imageLeaveToClass"
                enter-to-class="opacity-100 translate-x-0 scale-100"
                leave-from-class="opacity-100 translate-x-0 scale-100"
                mode="out-in"
              >
                <div :key="currentBanner?.id" class="lightbox-wrapper flex flex-col items-center gap-4">
                  <img
                    :src="currentBanner?.image"
                    :alt="currentBanner?.title"
                    class="lightbox-media rounded-2xl max-w-full max-h-[70vh] object-contain shadow-2xl border border-white/10"
                    draggable="false"
                  />
                  <!-- Subtitle details -->
                  <p class="text-white/70 font-semibold text-center text-xs max-w-2xl px-6">
                    {{ currentBanner?.description }}
                  </p>
                </div>
              </Transition>
            </div>

            <!-- Next navigation -->
            <button 
              @click="next" 
              class="lightbox-nav-btn lightbox-nav-next"
              aria-label="Next image"
            >
              <ChevronRightIcon class="w-6 h-6" />
            </button>
            
            <div class="lightbox-swipe-hint select-none">
              Swipe or use keyboard Arrow Keys to navigate
            </div>
          </div>
        </Transition>
      </Teleport>
    </ClientOnly>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  Maximize2Icon, 
  XIcon, 
  ChevronLeftIcon, 
  ChevronRightIcon 
} from 'lucide-vue-next'

// Capability Infographic Metadata
const banners = [
  {
    id: 1,
    title: "Secure & Reliable Systems",
    category: "Security & Operations",
    image: "/images/infographics/secure-reliable.png",
    description: "Deep integration of secure local SQLite databases with AES-256 encryption, biometric parameter validation, hardware-backed keystore isolation, and runtime integrity checks ensuring data remains protected even when fully offline."
  },
  {
    id: 2,
    title: "Product Launch & Operations",
    category: "Lifecycle Mgmt",
    image: "/images/infographics/launch-support.png",
    description: "End-to-end lifecycle management from conceptualization and feature scoping to CI/CD automated releases, over-the-air system updates, real-time performance monitoring dashboards, and long-term support metrics tracking for sustained operational health."
  },
  {
    id: 3,
    title: "Retail & POS Business Apps",
    category: "Commercial POS",
    image: "/images/infographics/mobile-business.png",
    description: "Mobile-first cash register systems with offline-first transaction queuing, multi-jurisdiction tax matrix calculations, instant Bluetooth and USB thermal receipt printing, and integrated payment gateway orchestration for seamless retail operations."
  },
  {
    id: 4,
    title: "Cloud Infrastructure & Backend APIs",
    category: "API & Infrastructure",
    image: "/images/infographics/backend-api.png",
    description: "Multi-layered backend server architecture spanning RESTful and GraphQL APIs, relational database replication and sharding, multi-provider payment aggregation, and high-frequency webhook pipelines with dead-letter queue resilience for maximum uptime."
  },
  {
    id: 5,
    title: "QA Delivery & Performance",
    category: "Quality Assurance",
    image: "/images/infographics/qa-performance.png",
    description: "Automated test coverage enforcement at 98%+, CI/CD build pipelines with gated quality checks, static analysis and clean code validation, comprehensive regression suites, and bug-free delivery checklists signed off per release cycle."
  },
  {
    id: 6,
    title: "Clean Code & Modular Architecture",
    category: "Software Design",
    image: "/images/infographics/clean-architecture.png",
    description: "Strict separation of concerns across Presentation, Application, Domain, and Data layers following SOLID principles, dependency injection patterns, repository abstractions, and interface-driven design for maximum testability and long-term maintainability."
  },
  {
    id: 7,
    title: "Mobile App Engineering",
    category: "Mobile Developer",
    image: "/images/infographics/mobile-developer.png",
    description: "Cross-platform application builds compiling to native platforms via Android SDK with Kotlin and Java, iOS Swift interfaces with UIKit and SwiftUI, and Flutter for unified codebase deployment across mobile, tablet, and desktop form factors."
  },
  {
    id: 8,
    title: "UI/UX Mobile System Design",
    category: "UI/UX Systems",
    image: "/images/infographics/ui-ux-design.png",
    description: "Unified design systems with modular typography components, dynamic HSL color palette theming supporting dark and light modes, user flow diagrams, pixel-perfect responsiveness across device sizes, and accessibility-first interaction patterns for inclusive experiences."
  },
  {
    id: 9,
    title: "Performance Optimization",
    category: "Analysis & Metrics",
    image: "/images/infographics/optimize-scale.png",
    description: "Systematic analysis of loading benchmarks and Core Web Vitals, minimization of Cumulative Layout Shift through optimized asset loading, crash ratio monitoring with root cause analysis, and proactive resource scaling based on usage pattern forecasting."
  },
  {
    id: 10,
    title: "Cross-Platform Mobile Integration",
    category: "Cross Platform",
    image: "/images/infographics/cross-platform.png",
    description: "Single-codebase development leveraging Vue.js, Nuxt, and React Native for universal app delivery, optimized rendering pipelines achieving 60fps even on mid-range devices, and shared business logic modules reducing cross-platform maintenance overhead by up to 40%."
  }
]

// Modal controller state
const activeIndex = ref(-1)
const direction = ref('none')
const isTransitioning = ref(false)

const isOpen = computed(() => activeIndex.value >= 0)
const currentBanner = computed(() => activeIndex.value >= 0 ? banners[activeIndex.value] : null)

const openLightbox = (index) => {
  direction.value = 'none'
  activeIndex.value = index
  if (import.meta.client) {
    document.body.style.overflow = 'hidden'
  }
}

const closeLightbox = () => {
  activeIndex.value = -1
  direction.value = 'none'
  if (import.meta.client) {
    document.body.style.overflow = ''
  }
}

const next = () => {
  if (isTransitioning.value) return
  isTransitioning.value = true
  direction.value = 'next'
  activeIndex.value = (activeIndex.value + 1) % banners.length
  setTimeout(() => { isTransitioning.value = false }, 300)
}

const prev = () => {
  if (isTransitioning.value) return
  isTransitioning.value = true
  direction.value = 'prev'
  activeIndex.value = (activeIndex.value - 1 + banners.length) % banners.length
  setTimeout(() => { isTransitioning.value = false }, 300)
}

// Directional transitions
const imageEnterClass = computed(() => 'transition-all duration-300 ease-out')
const imageLeaveClass = computed(() => 'transition-all duration-200 ease-in')

const imageEnterFromClass = computed(() => {
  if (direction.value === 'next') return 'opacity-0 translate-x-12 scale-95'
  if (direction.value === 'prev') return 'opacity-0 -translate-x-12 scale-95'
  return 'opacity-0 scale-90'
})

const imageLeaveToClass = computed(() => {
  if (direction.value === 'next') return 'opacity-0 -translate-x-12 scale-95'
  if (direction.value === 'prev') return 'opacity-0 translate-x-12 scale-95'
  return 'opacity-0 scale-90'
})

// Keyboard hooks
const handleKeydown = (e) => {
  if (!isOpen.value) return
  if (e.key === 'ArrowRight') next()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'Escape') closeLightbox()
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (isOpen.value && import.meta.client) {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
.lightbox-overlay {
  @apply fixed inset-0 z-[100] flex flex-col items-center justify-center select-none;
  background: rgba(2, 6, 4, 0.96);
  backdrop-filter: blur(35px) saturate(0.7);
}

.lightbox-ambient-glow {
  @apply absolute inset-0 pointer-events-none;
  background: 
    radial-gradient(ellipse 60% 40% at 50% 50%, hsl(var(--brand-color) / 0.06) 0%, transparent 70%),
    radial-gradient(ellipse 80% 60% at 30% 80%, hsl(var(--brand-light) / 0.03) 0%, transparent 50%);
}

.lightbox-topbar {
  @apply absolute top-0 inset-x-0 px-6 py-5 flex items-center justify-between z-30;
  background: linear-gradient(to bottom, rgba(2, 6, 4, 0.8) 0%, transparent 100%);
}

.lightbox-category-badge {
  @apply text-[9px] font-black uppercase tracking-[0.15em] px-3 py-1 rounded-lg shrink-0;
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.1);
  border: 1px solid hsl(var(--brand-color) / 0.25);
}

.lightbox-title {
  @apply text-white text-sm sm:text-base font-heading font-bold leading-tight truncate max-w-[50vw];
}

.lightbox-counter {
  @apply text-[10px] font-black uppercase tracking-[0.2em] px-3 py-1.5 rounded-lg text-white/50 border border-white/5 bg-slate-900/60 backdrop-blur-md;
}

.lightbox-btn {
  @apply flex items-center justify-center rounded-xl transition-all duration-300 cursor-pointer active:scale-95 w-10 h-10;
  color: hsl(var(--text-muted) / 0.8);
  background: hsl(var(--surface-elevated) / 0.7);
  border: 1px solid hsl(var(--border-color) / 0.2);
  backdrop-filter: blur(12px);
}

.lightbox-btn:hover {
  color: hsl(var(--brand-color));
  background: rgba(15, 30, 22, 0.85);
  border-color: hsl(var(--brand-color) / 0.35);
  box-shadow: 0 0 20px hsl(var(--brand-color) / 0.15);
}

.lightbox-nav-btn {
  @apply absolute top-1/2 -translate-y-1/2 w-12 h-12 z-20 hidden sm:flex;
  @apply flex items-center justify-center rounded-xl transition-all duration-300 cursor-pointer active:scale-90;
  color: hsl(var(--text-muted) / 0.8);
  background: hsl(var(--surface-elevated) / 0.65);
  border: 1px solid hsl(var(--border-color) / 0.2);
  backdrop-filter: blur(12px);
}

.lightbox-nav-btn:hover {
  color: hsl(var(--brand-color));
  background: rgba(15, 30, 22, 0.85);
  border-color: hsl(var(--brand-color) / 0.35);
  box-shadow: 0 0 30px hsl(var(--brand-color) / 0.15);
}

.lightbox-nav-prev {
  @apply left-6;
}

.lightbox-nav-next {
  @apply right-6;
}

.lightbox-content-container {
  @apply relative flex items-center justify-center z-10 px-4;
  max-width: min(90vw, 1000px);
  max-height: 75vh;
}

.lightbox-media {
  @apply max-h-[65vh] object-contain select-none shadow-2xl;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.8),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    0 0 80px hsl(var(--brand-color) / 0.08);
}

.lightbox-swipe-hint {
  @apply absolute bottom-8 left-1/2 -translate-x-1/2 text-[9px] font-black uppercase tracking-widest text-white/30 select-none;
}
</style>
