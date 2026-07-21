<template>
  <div class="min-h-screen relative overflow-x-hidden bg-surface text-main transition-colors duration-500 pb-32">
    <!-- Floating Immersive Navigation Controls -->
    <!-- Floating Back Button -->
    <NuxtLink 
      to="/projects" 
      class="fixed top-6 left-6 md:top-8 md:left-8 z-50 flex items-center justify-center w-12 h-12 rounded-full glass hover:border-brand/40 text-main transition-all duration-300 group shadow-lg hover:shadow-brand/5 active:scale-90"
      aria-label="Back to projects"
    >
      <ArrowLeftIcon class="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
    </NuxtLink>

    <!-- Floating Theme Toggle wrapper to align with back button -->
    <div class="fixed top-6 right-6 md:top-8 md:right-8 z-50 flex items-center gap-3">
      <div class="w-12 h-12 rounded-full glass flex items-center justify-center shadow-lg hover:border-brand/40 transition-colors">
        <ThemeToggle />
      </div>
    </div>

    <div v-if="project" class="w-full">
      <!-- FULL-BLEED HERO BANNER SECTION -->
      <div class="relative h-[85vh] w-full overflow-hidden flex items-end">
        <!-- Media background -->
        <div class="absolute inset-0 z-0">
          <!-- Video BG -->
          <video
            v-if="project.media?.type === 'video' && isLocalVideo(project.media.src)"
            :src="project.media.src"
            :poster="project.media.poster"
            muted
            autoplay
            loop
            playsinline
            class="w-full h-full object-cover scale-105"
          ></video>
          <!-- Embedded Video BG (Iframe) -->
          <iframe
            v-else-if="project.media?.type === 'video' && !isLocalVideo(project.media.src)"
            :src="embeddedBgUrl(project.media.src)"
            frameborder="0"
            allow="autoplay; encrypted-media"
            class="w-full h-full object-cover scale-105 pointer-events-none"
          ></iframe>
          <!-- Image BG -->
          <img
            v-else
            :src="project.media?.src || project.image"
            :alt="project.title"
            class="w-full h-full object-cover scale-105"
          />
          
          <!-- Cinematic overlay gradients -->
          <div class="absolute inset-0 bg-gradient-to-t from-surface via-surface/30 to-surface/80 z-10"></div>
          <div class="absolute inset-0 bg-surface/30 z-0"></div>
        </div>

        <!-- Floating Hero Content -->
        <div class="max-w-6xl mx-auto w-full px-6 pb-16 relative z-20 animate-reveal">
          <div class="inline-block px-3 py-1 rounded-lg bg-brand/10 border border-brand/20 text-brand text-[9px] font-black uppercase tracking-widest mb-4 backdrop-blur-md">
            {{ project.category }}
          </div>
          
          <h1 class="text-4xl sm:text-6xl md:text-7xl font-heading font-black text-gradient leading-tight tracking-tight mb-4 max-w-4xl">
            {{ project.title }}
          </h1>
          
          <p class="text-base sm:text-lg md:text-xl text-muted font-medium max-w-3xl leading-relaxed mb-6">
            {{ project.description }}
          </p>

          <!-- Meta Pill Badges -->
          <div class="flex flex-wrap items-center gap-4 text-xs font-bold text-muted bg-surface-card/30 backdrop-blur-md border border-border/40 p-4 rounded-2xl w-fit">
            <span class="flex items-center gap-2">
              <UserIcon class="w-4 h-4 text-brand" />
              <span class="text-main font-black">Role:</span> {{ project.details.role }}
            </span>
            <div class="hidden sm:block w-1.5 h-1.5 rounded-full bg-border"></div>
            <span class="flex items-center gap-2">
              <CalendarIcon class="w-4 h-4 text-brand" />
              <span class="text-main font-black">Timeline:</span> {{ project.details.timeline }}
            </span>
          </div>
        </div>

        <!-- Scroll indicator -->
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-1.5 animate-bounce opacity-70">
          <span class="text-[9px] font-black uppercase tracking-widest text-muted">Scroll Details</span>
          <div class="w-1 h-3 rounded-full bg-brand"></div>
        </div>
      </div>

      <!-- MAIN STORY CONTENT CONTAINER -->
      <div class="max-w-6xl mx-auto px-6 pt-16 relative z-20">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          <!-- LEFT AREA (Col Span 8): Overview & Deliverables -->
          <div class="lg:col-span-8 space-y-8 animate-reveal" style="animation-delay: 100ms">
            
            <!-- Project Media Showcase Card -->
            <div 
              @click="openLightbox"
              class="group glass-card p-3 rounded-[2.5rem] bg-surface-card border border-border relative overflow-hidden aspect-[16/10] cursor-pointer"
            >
              <MediaLoader 
                :media="project.media" 
                :alt-text="project.title"
                :hover-play="false"
                :zoom-on-hover="true"
                class="rounded-[1.8rem] w-full h-full object-cover"
              />
              
              <!-- Hover Overlay -->
              <div class="absolute inset-0 bg-surface/60 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center rounded-[2.5rem]">
                <div class="bg-surface-card/90 border border-brand/30 p-4 rounded-full shadow-lg hover:scale-105 active:scale-95 transition-all text-brand flex items-center gap-2">
                  <Maximize2Icon class="w-5 h-5 animate-pulse" />
                  <span class="text-xs font-black uppercase tracking-wider pr-1">Fullscreen Preview</span>
                </div>
              </div>
            </div>

            <!-- Project Description Bento -->
            <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
              <div class="flex items-center gap-3 mb-6 border-b border-border pb-4">
                <div class="w-8 h-8 rounded-lg bg-brand/5 border border-brand/20 flex items-center justify-center text-brand">
                  <BriefcaseIcon class="w-4 h-4" />
                </div>
                <h3 class="text-xl font-heading font-black text-main uppercase tracking-wider">Project Overview</h3>
              </div>
              <p class="text-muted leading-relaxed font-medium text-lg whitespace-pre-line">
                {{ project.details.longDescription }}
              </p>
            </div>

            <!-- Deliverables Bento -->
            <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
              <div class="flex items-center gap-3 mb-6 border-b border-border pb-4">
                <div class="w-8 h-8 rounded-lg bg-brand/5 border border-brand/20 flex items-center justify-center text-brand">
                  <ShieldCheckIcon class="w-4 h-4" />
                </div>
                <h3 class="text-xl font-heading font-black text-main uppercase tracking-wider">Key Deliverables</h3>
              </div>
              <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <li 
                  v-for="feature in project.details.features" 
                  :key="feature" 
                  class="flex items-start gap-3 text-muted leading-relaxed font-medium p-4 rounded-2xl bg-surface-elevated/20 border border-border/40 hover:border-brand/25 transition-all duration-300"
                >
                  <div class="w-5 h-5 rounded-full bg-brand/10 border border-brand/25 text-brand flex items-center justify-center mt-0.5 flex-shrink-0">
                    <span class="text-[10px] font-black">✓</span>
                  </div>
                  <span class="text-sm font-semibold text-main">{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- RIGHT AREA (Col Span 4): Specs, Stack, Actions -->
          <div class="lg:col-span-4 space-y-8 animate-reveal" style="animation-delay: 200ms">
            
            <!-- Actions Panel -->
            <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border space-y-4">
              <h3 class="text-xs font-black uppercase tracking-widest text-muted border-b border-border pb-3 mb-4">Project Links</h3>
              
              <div class="flex flex-col gap-3">
                <!-- Repository Link -->
                <a 
                  v-if="project.github" 
                  :href="project.github" 
                  target="_blank" 
                  class="btn-primary w-full flex items-center justify-center gap-3 px-6 py-4 text-xs font-black uppercase tracking-wider text-brand-dark hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
                >
                  <GithubIcon class="w-4 h-4" />
                  GitHub Repository
                </a>

                <!-- Live Demo -->
                <a 
                  v-if="project.link && project.link !== '#'" 
                  :href="project.link" 
                  target="_blank" 
                  class="btn-secondary w-full flex items-center justify-center gap-3 px-6 py-4 text-xs font-black uppercase tracking-wider hover:border-brand/40 hover:bg-surface-card/60 hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
                >
                  <ExternalLinkIcon class="w-4 h-4 text-brand" />
                  Live Application
                </a>
                <div 
                  v-else 
                  class="w-full flex items-center justify-center gap-2 px-6 py-4 text-[10px] font-black uppercase tracking-wider bg-surface-elevated/30 border border-border/40 text-muted rounded-xl cursor-not-allowed select-none"
                >
                  <ShieldCheckIcon class="w-4 h-4 opacity-50" />
                  Internal Access Only
                </div>

                <!-- Discuss WhatsApp -->
                <a 
                  :href="whatsappUrl" 
                  target="_blank"
                  class="w-full flex items-center justify-center gap-2 px-6 py-4 text-[10px] font-black uppercase tracking-wider border border-brand/20 hover:border-brand/50 bg-brand/5 hover:bg-brand/10 text-brand rounded-xl hover:-translate-y-0.5 active:scale-95 transition-all duration-300 mt-2"
                >
                  Discuss Project Details
                  <ArrowUpRightIcon class="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            <!-- Tech Stack Bento -->
            <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border">
              <h3 class="text-xs font-black uppercase tracking-widest text-muted border-b border-border pb-3 mb-5">Tech Stack</h3>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="tech in project.details.techStack" 
                  :key="tech"
                  class="text-[9px] px-3.5 py-2.5 rounded-xl bg-surface-elevated/40 text-main font-black uppercase tracking-widest border border-border/80 transition-all duration-300 hover:border-brand/45 hover:text-brand hover:scale-105"
                >
                  {{ tech }}
                </span>
              </div>
            </div>

            <!-- Architectural Challenges Bento -->
            <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border">
              <h3 class="text-xs font-black uppercase tracking-widest text-muted border-b border-border pb-3 mb-4">Engineering Challenges</h3>
              <p class="text-muted leading-relaxed font-medium text-sm">
                {{ project.details.challenges }}
              </p>
              <div class="mt-6 p-4 rounded-2xl bg-brand/5 border border-brand/10 text-brand text-xs font-bold flex items-center gap-3">
                <ShieldCheckIcon class="w-5 h-5 flex-shrink-0" />
                <span>Resolved and implemented in production.</span>
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>

    <!-- Error Fallback -->
    <div class="max-w-xl mx-auto text-center py-32 animate-reveal" v-else>
      <BoxIcon class="w-16 h-16 text-muted mx-auto mb-6 opacity-35 animate-pulse" />
      <h2 class="text-2xl font-black text-main mb-4">Project Not Found</h2>
      <p class="text-muted mb-8 font-medium">The project you are looking for does not exist in our registry.</p>
      <NuxtLink to="/projects" class="btn-primary inline-flex py-4 px-10 text-xs font-black uppercase tracking-wider">
        Back to Portfolio
      </NuxtLink>
    </div>

    <!-- Custom Media Fullscreen Lightbox Modal -->
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
            v-if="showLightbox"
            class="lightbox-overlay"
            @click.self="closeLightbox"
            role="dialog"
            aria-modal="true"
            :aria-label="`Media viewer: ${project?.title || ''}`"
          >
            <!-- Background glow -->
            <div class="lightbox-ambient-glow"></div>

            <!-- Top Close Bar -->
            <div class="lightbox-topbar">
              <div class="flex items-center gap-3 min-w-0">
                <span class="lightbox-category-badge">
                  {{ project?.category }}
                </span>
                <h3 class="lightbox-title">
                  {{ project?.title }}
                </h3>
              </div>
              <button 
                @click="closeLightbox" 
                class="lightbox-btn"
                aria-label="Close viewer"
              >
                <XIcon class="w-5 h-5" />
              </button>
            </div>

            <!-- Media Container -->
            <div class="lightbox-content-container" @click.stop>
              <!-- Video Player -->
              <video
                v-if="project?.media?.type === 'video' && isLocalVideo(project.media.src)"
                :src="project.media.src"
                :poster="project.media.poster"
                controls
                autoplay
                loop
                muted
                playsinline
                class="lightbox-media rounded-2xl max-w-full max-h-[80vh] shadow-2xl border border-border/30"
              ></video>

              <!-- Iframe embedded Video -->
              <iframe
                v-else-if="project?.media?.type === 'video' && !isLocalVideo(project.media.src)"
                :src="embeddedUrl(project.media.src)"
                frameborder="0"
                allow="autoplay; encrypted-media"
                allowfullscreen
                class="lightbox-media rounded-2xl w-[85vw] h-[55vw] max-w-[1000px] max-h-[600px] shadow-2xl border border-border/30"
              ></iframe>

              <!-- Fallback Image -->
              <img
                v-else
                :src="project?.media?.src || project?.image"
                :alt="project?.title"
                class="lightbox-media rounded-2xl max-w-full max-h-[80vh] object-contain shadow-2xl border border-border/30"
                draggable="false"
              />
            </div>
            
            <div class="lightbox-info-caption text-xs text-muted/50 absolute bottom-6 text-center w-full select-none pointer-events-none">
              Click outside or press ESC to exit
            </div>
          </div>
        </Transition>
      </Teleport>
    </ClientOnly>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ArrowLeftIcon, 
  ArrowUpRightIcon, 
  GithubIcon, 
  ExternalLinkIcon, 
  UserIcon, 
  CalendarIcon, 
  ShieldCheckIcon,
  BoxIcon,
  XIcon,
  Maximize2Icon,
  BriefcaseIcon
} from 'lucide-vue-next'
import projectsData from '~/data/projects.json'
import globalData from '~/data/global.json'

const route = useRoute()

const project = computed(() => {
  const slug = route.params.slug
  return projectsData.projects.find(p => p.slug === slug)
})

// Setup reactively computed head tags for Nuxt 4 SEO compliance
useHead({
  title: () => project.value ? `${project.value.title} | Project Details` : 'Project Details',
  meta: [
    { 
      name: 'description', 
      content: () => project.value ? project.value.description : 'Details and technical specifications of this project.' 
    }
  ]
})

// Lightbox state and control
const showLightbox = ref(false)

const openLightbox = () => {
  showLightbox.value = true
  if (import.meta.client) {
    document.body.style.overflow = 'hidden'
  }
}

const closeLightbox = () => {
  showLightbox.value = false
  if (import.meta.client) {
    document.body.style.overflow = ''
  }
}

// Check if a video source is local / raw mp4
const isLocalVideo = (src) => {
  if (!src) return false
  return src.startsWith('/') || src.endsWith('.mp4') || src.endsWith('.webm') || src.includes('mixkit.co')
}

// Compute embedded video source for iframe
const embeddedUrl = (src) => {
  if (!src) return ''
  let finalUrl = src
  if (src.includes('youtube.com') || src.includes('youtu.be')) {
    const videoId = src.includes('embed') ? src.split('embed/')[1] : src.split('v=')[1]
    finalUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&loop=1&playlist=${videoId}`
  } else if (src.includes('vimeo.com')) {
    const videoId = src.split('vimeo.com/')[1]
    finalUrl = `https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1`
  }
  return finalUrl
}

// Compute embedded bg video (no controls, autoplays, loops, mutes)
const embeddedBgUrl = (src) => {
  if (!src) return ''
  let finalUrl = src
  if (src.includes('youtube.com') || src.includes('youtu.be')) {
    const videoId = src.includes('embed') ? src.split('embed/')[1] : src.split('v=')[1]
    finalUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&loop=1&playlist=${videoId}&controls=0&showinfo=0&keyboard=0&disablekb=1&modestbranding=1`
  } else if (src.includes('vimeo.com')) {
    const videoId = src.split('vimeo.com/')[1]
    finalUrl = `https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1&background=1`
  }
  return finalUrl
}

// Compute dynamic WhatsApp contact link
const whatsappUrl = computed(() => {
  if (!project.value) return globalData.socials.whatsapp
  const text = encodeURIComponent(`Hi Ringga, I am interested in your project: "${project.value.title}". Let's discuss!`)
  return `${globalData.socials.whatsapp}&text=${text}`
})

// Esc keyboard handler for close lightbox
const handleKeydown = (e) => {
  if (e.key === 'Escape' && showLightbox.value) {
    closeLightbox()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (showLightbox.value && import.meta.client) {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
.lightbox-overlay {
  @apply fixed inset-0 z-[100] flex flex-col items-center justify-center select-none;
  background: rgba(2, 6, 4, 0.96);
  backdrop-filter: blur(30px) saturate(0.7);
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
  @apply text-sm sm:text-base font-heading font-bold leading-tight truncate;
  color: hsl(var(--text-main));
}

.lightbox-btn {
  @apply flex items-center justify-center rounded-xl transition-all duration-300 cursor-pointer active:scale-95 w-10 h-10;
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

.lightbox-content-container {
  @apply relative flex items-center justify-center z-10 px-4;
  max-width: min(90vw, 1200px);
  max-height: 80vh;
}

.lightbox-media {
  @apply max-h-[75vh] object-contain select-none shadow-2xl;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.7),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    0 0 80px hsl(var(--brand-color) / 0.08);
}
</style>
