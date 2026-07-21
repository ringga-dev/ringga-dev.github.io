<template>
  <section class="relative min-h-screen flex items-center overflow-hidden bg-surface">
    <!-- Ambient background -->
    <div class="absolute inset-0 -z-10 opacity-[0.06] [mask-image:radial-gradient(ellipse_at_center,black,transparent_75%)] bg-grid-slate pointer-events-none"></div>
    <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-[900px] h-[520px] bg-brand/10 blur-[170px] pointer-events-none rounded-full -z-10"></div>
    <div class="absolute -bottom-32 -right-20 w-[600px] h-[600px] bg-brand-light/10 blur-[170px] pointer-events-none rounded-full -z-10"></div>

    <div class="relative z-10 w-full max-w-7xl mx-auto px-6 pt-32 pb-32">
      <div class="grid lg:grid-cols-12 gap-12 lg:gap-10 items-center">
        <!-- LEFT: copy -->
        <div class="lg:col-span-7 space-y-7">
          <!-- Availability -->
          <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-surface-card/80 border border-border/70 text-muted text-[11px] font-bold tracking-widest uppercase backdrop-blur">
            <span class="relative flex h-2.5 w-2.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-brand"></span>
            </span>
            {{ homeData.hero.badge }}
          </div>

          <!-- Headline -->
          <h1 class="font-heading font-black text-main leading-[1.02] tracking-tight">
            <span class="block text-2xl sm:text-3xl md:text-4xl lg:text-6xl">{{ homeData.hero.title }}</span>
            <span class="block mt-2 text-gradient text-2xl sm:text-3xl md:text-4xl lg:text-5xl">{{ typedRole || homeData.hero.titleHighlight }}</span><span class="animate-pulse text-brand font-light">|</span>
          </h1>

          <!-- Description -->
          <p class="text-muted text-base sm:text-lg md:text-xl font-medium leading-relaxed max-w-xl">
            {{ homeData.hero.description }}
          </p>

          <!-- CTAs -->
          <div class="flex flex-col sm:flex-row gap-4 pt-1">
            <a
              :href="homeData.hero.primaryCta.url"
              target="_blank"
              class="btn-primary flex items-center justify-center gap-3 px-8 py-4 group font-black uppercase tracking-wider text-xs shadow-lg shadow-brand/10 hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
            >
              {{ homeData.hero.primaryCta.text }}
              <ArrowRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
            <NuxtLink
              :to="homeData.hero.secondaryCta.url"
              class="btn-secondary flex items-center justify-center gap-3 px-8 py-4 font-black uppercase tracking-wider text-xs hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
            >
              {{ homeData.hero.secondaryCta.text }}
            </NuxtLink>
          </div>

          <!-- Mini stats -->
          <div class="flex flex-wrap gap-x-8 gap-y-4 pt-3">
            <div
              v-for="stat in homeData.stats"
              :key="stat.label"
              class="flex items-center gap-3"
            >
              <component :is="getIcon(stat.icon)" class="w-5 h-5 text-brand" />
              <div>
                <div class="text-xl font-black text-main leading-none">{{ stat.value }}{{ stat.suffix }}</div>
                <div class="text-[10px] font-black uppercase tracking-widest text-muted mt-0.5">{{ stat.label }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT: 3D stage card -->
        <div class="lg:col-span-5">
          <div class="relative">
            <div class="glass-card rounded-[2.5rem] p-3 shadow-2xl shadow-black/40">
              <div class="relative aspect-square sm:aspect-[4/5] rounded-[2rem] overflow-hidden bg-surface-elevated/40">
                <HeroScene3D class="absolute inset-0" />

                <!-- Stage labels -->
                <div class="absolute top-4 left-4 z-10 flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-elevated/60 backdrop-blur border border-border/30 text-[10px] font-black uppercase tracking-widest text-brand">
                  <span class="w-2 h-2 rounded-full bg-brand animate-pulse"></span>
                  Interactive 3D
                </div>
                <div class="absolute bottom-4 right-4 z-10 text-[10px] font-bold uppercase tracking-[0.2em] text-muted/70">
                  Drag to explore
                </div>
              </div>
            </div>
            <!-- Floating accent -->
            <div class="absolute -bottom-6 -left-6 w-24 h-24 rounded-3xl bg-gradient-to-br from-brand to-brand-light blur-2xl opacity-30 pointer-events-none"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tech stack strip -->
    <div class="absolute bottom-0 inset-x-0 z-20 border-t border-border/60 bg-surface/40 backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-6 py-5 flex items-center gap-6 overflow-x-auto">
        <span class="text-[9px] font-black uppercase tracking-[0.3em] text-muted shrink-0 hidden sm:block">
          {{ homeData.techStack.badge }}
        </span>
        <div class="flex items-center gap-7">
          <div
            v-for="tech in homeData.techStack.techs"
            :key="tech.name"
            class="flex items-center gap-2.5 group cursor-default shrink-0"
          >
            <component :is="getIcon(tech.icon)" class="w-5 h-5 text-muted group-hover:text-[var(--glow)] transition-colors duration-300" :style="{ '--glow': tech.color }" />
            <span class="text-[10px] font-black text-muted tracking-widest uppercase group-hover:text-main transition-colors duration-300">
              {{ tech.name }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="absolute bottom-24 left-1/2 -translate-x-1/2 z-20 hidden lg:flex flex-col items-center gap-2 text-muted/50">
      <span class="text-[9px] font-black uppercase tracking-[0.3em]">Scroll</span>
      <div class="w-5 h-8 rounded-full border border-muted/30 flex justify-center pt-1.5">
        <span class="w-1 h-1.5 rounded-full bg-brand animate-bounce"></span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ArrowRightIcon, 
  SmartphoneIcon, 
  LayersIcon, 
  DatabaseIcon, 
  Code2Icon, 
  CpuIcon, 
  BoxIcon 
} from 'lucide-vue-next'
import homeData from '~/data/home.json'
import HeroScene3D from '~/features/home/HeroScene3D.vue'

const getIcon = (name) => {
  switch (name) {
    case 'SmartphoneIcon': return SmartphoneIcon
    case 'LayersIcon': return LayersIcon
    case 'DatabaseIcon': return DatabaseIcon
    case 'Code2Icon': return Code2Icon
    case 'CpuIcon': return CpuIcon
    case 'BoxIcon': return BoxIcon
    default: return Code2Icon
  }
}

// Typing Effect for the hero highlight
const roles = ['Multi-Platform Developer', 'KMP/Compose Expert', 'Systems Architect', 'Fullstack Engineer']
const typedRole = ref('')
let roleIndex = 0
let charIndex = 0
let isDeleting = false

const typeEffect = () => {
  const currentRole = roles[roleIndex]

  if (isDeleting) {
    typedRole.value = currentRole.substring(0, charIndex - 1)
    charIndex--
  } else {
    typedRole.value = currentRole.substring(0, charIndex + 1)
    charIndex++
  }

  let typeSpeed = isDeleting ? 45 : 85

  if (!isDeleting && charIndex === currentRole.length) {
    typeSpeed = 2200
    isDeleting = true
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false
    roleIndex = (roleIndex + 1) % roles.length
    typeSpeed = 400
  }

  setTimeout(typeEffect, typeSpeed)
}

onMounted(() => {
  typeEffect()
})
</script>
