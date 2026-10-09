<template>
  <div class="min-h-screen relative overflow-x-hidden bg-surface text-main transition-colors duration-500 pb-32">
    <!-- Floating Immersive Navigation Controls -->
    <!-- Floating Back Button -->
    <NuxtLink 
      to="/projects" 
      class="fixed top-6 left-6 md:top-8 md:left-8 z-50 flex items-center justify-center w-12 h-12 rounded-sm riso-card hover:border-brand text-main transition-[transform,box-shadow] duration-150 group"
      aria-label="Back to projects"
    >
      <ArrowLeftIcon class="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
    </NuxtLink>

    <!-- Floating Theme Toggle wrapper to align with back button -->
    <div class="fixed top-6 right-6 md:top-8 md:right-8 z-50 flex items-center gap-3">
      <div class="w-12 h-12 rounded-sm riso-card flex items-center justify-center hover:border-brand transition-[transform,box-shadow] duration-150">
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
        <div class="max-w-6xl mx-auto w-full px-6 pb-16 relative z-20">
          <div class="stamp inline-block px-3 py-1 text-brand mb-4">
            {{ project.category }}
          </div>
          
          <h1 class="text-4xl sm:text-6xl md:text-7xl font-display font-bold text-brand leading-tight tracking-tight mb-4 max-w-4xl riso-ghost">
            {{ project.title }}
          </h1>
          
          <p class="text-base sm:text-lg md:text-xl text-muted font-serif max-w-3xl leading-relaxed mb-6">
            {{ project.description }}
          </p>

          <!-- Meta Stamp Badges -->
          <div class="flex flex-wrap items-center gap-4 text-xs font-mono font-semibold text-muted bg-surface-card border-[1.5px] border-ink/70 shadow-riso p-4 rounded-sm w-fit">
            <span class="flex items-center gap-2">
              <UserIcon class="w-4 h-4 text-brand" />
              <span class="text-main font-semibold">Role:</span> {{ project.details.role }}
            </span>
            <div class="hidden sm:block w-1.5 h-1.5 bg-brand rotate-45"></div>
            <span class="flex items-center gap-2">
              <CalendarIcon class="w-4 h-4 text-brand" />
              <span class="text-main font-semibold">Timeline:</span> {{ project.details.timeline }}
            </span>
          </div>
        </div>

        <!-- Scroll indicator -->
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-1.5 opacity-70">
          <span class="text-[9px] font-mono font-semibold uppercase tracking-widest text-muted">Scroll Details</span>
          <div class="w-1 h-3 bg-brand"></div>
        </div>
      </div>

      <!-- MAIN STORY CONTENT CONTAINER -->
      <div class="max-w-6xl mx-auto px-6 pt-16 relative z-20">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          <!-- LEFT AREA (Col Span 8): Overview & Deliverables -->
          <div class="lg:col-span-8 space-y-8">
            
            <!-- Project Media Showcase Card -->
            <div 
              @click="openLightbox"
              class="group riso-card p-3 bg-surface-card relative overflow-hidden aspect-[16/10] cursor-pointer hover:-translate-x-0.5 hover:-translate-y-0.5"
            >
              <MediaLoader 
                :media="project.media" 
                :alt-text="project.title"
                :hover-play="false"
                :zoom-on-hover="true"
                class="w-full h-full object-cover"
              />
              
              <!-- Hover Overlay -->
              <div class="absolute inset-0 bg-surface/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <div class="bg-surface-card border-[1.5px] border-ink p-4 shadow-riso text-brand flex items-center gap-2">
                  <Maximize2Icon class="w-5 h-5" />
                  <span class="text-xs font-mono font-semibold uppercase tracking-wider pr-1">Fullscreen Preview</span>
                </div>
              </div>
            </div>

            <!-- Project Description Bento -->
            <div class="riso-card p-8 md:p-10 bg-surface-card">
              <div class="flex items-center gap-3 mb-6 border-b border-border pb-4">
                <div class="w-8 h-8 rounded-sm border-[1.5px] border-ink flex items-center justify-center text-brand shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)]">
                  <BriefcaseIcon class="w-4 h-4" />
                </div>
                <h3 class="text-xl font-display font-bold text-main uppercase tracking-wider">Project Overview</h3>
              </div>
              <p class="text-muted leading-relaxed font-serif text-lg whitespace-pre-line">
                {{ project.details.longDescription }}
              </p>
            </div>

            <!-- Deliverables Bento -->
            <div class="riso-card-2 p-8 md:p-10 bg-surface-card">
              <div class="flex items-center gap-3 mb-6 border-b border-border pb-4">
                <div class="w-8 h-8 rounded-sm border-[1.5px] border-ink flex items-center justify-center text-ink-2 shadow-[2px_2px_0_hsl(var(--ink-2)/0.6)]">
                  <ShieldCheckIcon class="w-4 h-4" />
                </div>
                <h3 class="text-xl font-display font-bold text-main uppercase tracking-wider">Key Deliverables</h3>
              </div>
              <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <li 
                  v-for="feature in project.details.features" 
                  :key="feature" 
                  class="flex items-start gap-3 text-muted leading-relaxed font-serif p-4 rounded-sm bg-surface-elevated/20 border-[1.5px] border-ink/60 hover:border-brand hover:-translate-x-0.5 hover:-translate-y-0.5 transition-[transform,box-shadow,border-color] duration-150"
                >
                  <div class="w-5 h-5 bg-brand/15 border-[1.5px] border-brand text-brand flex items-center justify-center mt-0.5 flex-shrink-0">
                    <span class="text-[10px] font-semibold">✓</span>
                  </div>
                  <span class="text-sm font-serif text-main">{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- RIGHT AREA (Col Span 4): Specs, Stack, Actions -->
          <div class="lg:col-span-4 space-y-8">
            
            <!-- Actions Panel -->
            <div class="riso-card-2 p-8 bg-surface-card space-y-4">
              <h3 class="text-xs font-mono font-semibold uppercase tracking-widest text-muted border-b border-border pb-3 mb-4">Project Links</h3>
              
              <div class="flex flex-col gap-3">
                <!-- Repository Link -->
                <a 
                  v-if="project.github" 
                  :href="project.github" 
                  target="_blank" 
                  class="btn-primary w-full flex items-center justify-center gap-3 px-6 py-4 text-xs font-mono font-semibold uppercase tracking-wider"
                >
                  <GithubIcon class="w-4 h-4" />
                  GitHub Repository
                </a>

                <!-- Live Demo -->
                <a 
                  v-if="project.link && project.link !== '#'" 
                  :href="project.link" 
                  target="_blank"
                  class="btn-secondary w-full flex items-center justify-center gap-3 px-6 py-4 text-xs font-mono font-semibold uppercase tracking-wider hover:border-brand"
                >
                  <ExternalLinkIcon class="w-4 h-4 text-brand" />
                  Live Application
                </a>
                <div 
                  v-else 
                  class="w-full flex items-center justify-center gap-2 px-6 py-4 text-[10px] font-mono font-semibold uppercase tracking-wider bg-surface-elevated/30 border-[1.5px] border-ink/40 text-muted rounded-sm cursor-not-allowed select-none"
                >
                  <ShieldCheckIcon class="w-4 h-4 opacity-50" />
                  Internal Access Only
                </div>

                <!-- Discuss WhatsApp -->
                <a 
                  :href="whatsappUrl" 
                  target="_blank"
                  class="w-full flex items-center justify-center gap-2 px-6 py-4 text-[10px] font-mono font-semibold uppercase tracking-wider border-[1.5px] border-ink/60 hover:border-brand bg-brand/5 hover:bg-brand/10 text-brand rounded-sm transition-[transform,box-shadow,border-color] duration-150 hover:-translate-x-0.5 hover:-translate-y-0.5 mt-2"
                >
                  Discuss Project Details
                  <ArrowUpRightIcon class="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            <!-- Tech Stack Bento -->
            <div class="riso-card p-8 bg-surface-card">
              <h3 class="text-xs font-mono font-semibold uppercase tracking-widest text-muted border-b border-border pb-3 mb-5">Tech Stack</h3>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="tech in project.details.techStack" 
                  :key="tech"
                  class="text-[9px] px-3.5 py-2 bg-surface-elevated text-main font-mono font-semibold uppercase tracking-widest border-[1.5px] border-ink/60 transition-[transform,box-shadow,border-color] duration-150 hover:border-brand hover:text-brand hover:-translate-x-0.5 hover:-translate-y-0.5"
                >
                  {{ tech }}
                </span>
              </div>
            </div>

            <!-- Architectural Challenges Bento -->
            <div class="riso-card-2 p-8 bg-surface-card">
              <h3 class="text-xs font-mono font-semibold uppercase tracking-widest text-muted border-b border-border pb-3 mb-4">Engineering Challenges</h3>
              <p class="text-muted leading-relaxed font-serif text-sm">
                {{ project.details.challenges }}
              </p>
              <div class="mt-6 p-4 bg-ink-2/10 border-[1.5px] border-ink-2/40 text-ink-2 text-xs font-semibold flex items-center gap-3">
                <ShieldCheckIcon class="w-5 h-5 flex-shrink-0" />
                <span>Resolved and implemented in production.</span>
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>

    <!-- Error Fallback -->
    <div class="max-w-xl mx-auto text-center py-32" v-else>
      <BoxIcon class="w-16 h-16 text-muted mx-auto mb-6 opacity-35" />
      <h2 class="text-2xl font-display font-semibold text-main mb-4">Project Not Found</h2>
      <p class="text-muted mb-8 font-serif">The project you are looking for does not exist in our registry.</p>
      <NuxtLink to="/projects" class="btn-primary inline-flex py-4 px-10 text-xs font-mono font-semibold uppercase tracking-wider">
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
                class="lightbox-media max-w-full max-h-[80vh]"
              ></video>

              <!-- Iframe embedded Video -->
              <iframe
                v-else-if="project?.media?.type === 'video' && !isLocalVideo(project.media.src)"
                :src="embeddedUrl(project.media.src)"
                frameborder="0"
                allow="autoplay; encrypted-media"
                allowfullscreen
                class="lightbox-media w-[85vw] h-[55vw] max-w-[1000px] max-h-[600px]"
              ></iframe>

              <!-- Fallback Image -->
              <img
                v-else
                :src="project?.media?.src || project?.image"
                :alt="project?.title"
                class="lightbox-media max-w-full max-h-[80vh] object-contain"
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
  background: hsl(36 24% 5% / 0.97);
}

.lightbox-topbar {
  @apply absolute top-0 inset-x-0 px-6 py-5 flex items-center justify-between z-30;
  border-bottom: 1px solid hsl(32 16% 20%);
}

.lightbox-category-badge {
  @apply font-mono text-[10px] uppercase tracking-[0.2em] px-3 py-1 shrink-0 rotate-stamp-l inline-block;
  color: hsl(var(--brand-color));
  border: 1.5px solid hsl(var(--brand-color) / 0.6);
}

.lightbox-title {
  @apply text-sm sm:text-base font-display font-bold leading-tight truncate;
  color: hsl(36 30% 92%);
}

.lightbox-btn {
  @apply flex items-center justify-center transition-[color,border-color,box-shadow,transform] duration-150 cursor-pointer w-10 h-10;
  color: hsl(32 14% 62%);
  background: transparent;
  border: 1.5px solid hsl(32 16% 20%);
}

.lightbox-btn:hover {
  color: hsl(var(--brand-color));
  border-color: hsl(var(--brand-color) / 0.6);
  box-shadow: 2px 2px 0 hsl(var(--brand-color) / 0.5);
  transform: translate(-1px, -1px);
}

.lightbox-content-container {
  @apply relative flex items-center justify-center z-10 px-4;
  max-width: min(90vw, 1200px);
  max-height: 80vh;
}

.lightbox-media {
  @apply max-h-[75vh] object-contain select-none;
  border: 1px solid hsl(var(--text-main) / 0.2);
  box-shadow: 4px 4px 0 hsl(var(--brand-color) / 0.55);
}
</style>
