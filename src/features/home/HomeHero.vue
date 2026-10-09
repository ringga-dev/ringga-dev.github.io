<template>
  <section class="relative min-h-screen flex items-center overflow-hidden bg-surface pt-28 pb-24">
    <div class="relative z-10 w-full max-w-7xl mx-auto px-6">
      <div class="grid lg:grid-cols-12 gap-12 lg:gap-10 items-center">
        <!-- LEFT: copy -->
        <div class="lg:col-span-7 space-y-6">
          <!-- Availability (mono label, no pill) -->
          <div class="flex items-center gap-2.5 font-mono text-xs uppercase tracking-[0.2em] text-muted">
            <span class="inline-block w-2 h-2 rounded-full bg-brand"></span>
            {{ homeData.hero.badge }}
          </div>

          <!-- Headline -->
          <h1 class="font-display text-main leading-[1.02] tracking-tight">
            <span class="block text-3xl sm:text-4xl md:text-5xl">{{ homeData.hero.title }}</span>
            <span class="block mt-2 text-brand text-2xl sm:text-3xl md:text-4xl font-medium">{{ typedRole || homeData.hero.titleHighlight }}</span>
          </h1>

          <!-- Description -->
          <p class="text-muted text-base sm:text-lg md:text-xl font-serif leading-relaxed max-w-xl">
            {{ homeData.hero.description }}
          </p>

          <!-- CTAs -->
          <div class="flex flex-col sm:flex-row gap-3 pt-1">
            <a
              :href="homeData.hero.primaryCta.url"
              target="_blank"
              rel="noopener"
              class="btn-primary gap-3 px-7 py-3.5 font-mono text-xs uppercase tracking-[0.15em]"
            >
              {{ homeData.hero.primaryCta.text }}
            </a>
            <NuxtLink
              :to="homeData.hero.secondaryCta.url"
              class="btn-secondary gap-3 px-7 py-3.5 font-mono text-xs uppercase tracking-[0.15em]"
            >
              {{ homeData.hero.secondaryCta.text }}
            </NuxtLink>
          </div>

          <!-- Mini stats -->
          <div class="flex flex-wrap gap-x-10 gap-y-4 pt-4">
            <div
              v-for="stat in homeData.stats"
              :key="stat.label"
              class="flex items-center gap-3"
            >
              <component :is="getIcon(stat.icon)" class="w-5 h-5 text-brand" />
              <div>
                <div class="text-2xl font-display font-semibold text-main leading-none">{{ stat.value }}{{ stat.suffix }}</div>
                <div class="text-[10px] font-mono uppercase tracking-[0.2em] text-muted mt-1">{{ stat.label }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT: 3D stage card -->
        <div class="lg:col-span-5">
          <div class="relative">
            <div class="glass-card p-3">
              <div class="relative aspect-square sm:aspect-[4/5] rounded overflow-hidden bg-surface-elevated">
                <HeroScene3D class="absolute inset-0" />

                <!-- Stage labels -->
                <div class="absolute top-3 left-3 z-10 font-mono text-[10px] uppercase tracking-[0.2em] text-brand">
                  Interactive 3D
                </div>
                <div class="absolute bottom-3 right-3 z-10 font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  Drag to explore
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tech stack strip: hairline top rule, no blur -->
    <div class="absolute bottom-0 inset-x-0 z-20 border-t border-border bg-surface">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center gap-6 overflow-x-auto">
        <span class="font-mono text-[10px] uppercase tracking-[0.25em] text-muted shrink-0 hidden sm:block">
          {{ homeData.techStack.badge }}
        </span>
        <div class="flex items-center gap-6">
          <div
            v-for="tech in homeData.techStack.techs"
            :key="tech.name"
            class="flex items-center gap-2 shrink-0"
          >
            <component :is="getIcon(tech.icon)" class="w-4 h-4 text-muted" />
            <span class="font-mono text-[10px] text-muted tracking-[0.15em] uppercase">
              {{ tech.name }}
            </span>
          </div>
        </div>
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
