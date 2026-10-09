<template>
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start mb-40">
    <!-- Profile Photo Section -->
    <div class="lg:col-span-5 relative">
      <div class="absolute -top-10 -left-10 w-40 h-40 halftone-2 pointer-events-none"></div>
      <div class="relative p-4 riso-card group overflow-hidden bg-surface-card">
        <img
          :src="aboutData.bio.image"
          :alt="aboutData.bio.titleHighlight"
          loading="lazy"
          decoding="async"
          @error="onImgError"
          v-if="!imgError"
          class="w-full aspect-square object-cover grayscale contrast-125 saturate-50 group-hover:grayscale-0 transition-[filter] duration-300"
        />
        <div
          v-else
          class="w-full aspect-square bg-surface-elevated border-[1.5px] border-ink/70 flex items-center justify-center text-brand font-display text-6xl font-bold riso-ghost"
        >
          RD
        </div>
        <div class="absolute inset-0 halftone opacity-0 group-hover:opacity-100 transition-opacity duration-150 pointer-events-none"></div>
      </div>

      <!-- Experience Badge -->
      <div class="absolute -bottom-6 -right-6 riso-card-2 p-6 bg-surface-card">
        <div class="numeral text-4xl text-brand mb-1">{{ aboutData.bio.experienceYears }}</div>
        <div class="font-mono text-[10px] font-semibold text-muted uppercase tracking-[0.2em] leading-tight">Years of<br/>Expertise</div>
      </div>
    </div>

    <!-- Narrative Section -->
    <div class="lg:col-span-7">
      <SectionHeader :badge="aboutData.bio.badge">
        <template #title>
          {{ aboutData.bio.title }} <span class="text-brand">{{ aboutData.bio.titleHighlight }}</span>
        </template>
      </SectionHeader>

      <div class="space-y-6 text-muted text-lg md:text-xl font-serif leading-relaxed mb-12">
        <p v-for="(p, index) in aboutData.bio.paragraphs" :key="index" v-html="highlightKeywords(p)"></p>
      </div>

      <div class="flex flex-wrap gap-6 items-center">
        <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary flex items-center gap-3 px-10 font-mono text-xs font-semibold uppercase tracking-[0.18em] py-4">
          Let's Collaborate
          <ExternalLinkIcon class="w-5 h-5" />
        </a>
        <a :href="aboutData.bio.cvUrl" target="_blank" rel="noopener" class="btn-secondary flex items-center gap-3 px-10 font-mono text-xs font-semibold uppercase tracking-[0.18em] py-4">
          Full Profile
          <ExternalLinkIcon class="w-5 h-5" />
        </a>
        <div class="flex gap-4 items-center">
          <a
            v-for="social in socialList"
            :key="social.name"
            :href="social.url"
            target="_blank"
            class="w-12 h-12 riso-card flex items-center justify-center text-muted hover:text-brand"
            :aria-label="social.name"
          >
            <component :is="social.icon" class="w-5 h-5" />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  GithubIcon,
  LinkedinIcon,
  MailIcon,
  ExternalLinkIcon
} from 'lucide-vue-next'
import aboutData from '~/data/about.json'
import globalData from '~/data/global.json'

const imgError = ref(false)

const onImgError = () => {
  imgError.value = true
}

const socialList = computed(() => {
  return [
    { name: 'GitHub', icon: GithubIcon, url: globalData.socials.github },
    { name: 'LinkedIn', icon: LinkedinIcon, url: globalData.socials.linkedin },
    { name: 'Email', icon: MailIcon, url: globalData.socials.email }
  ]
})

// Highlight specific keywords in bio paragraphs for premium design accent
const highlightKeywords = (text) => {
  const highlights = [
    'Senior Mobile Developer',
    'Kotlin Multiplatform',
    'Jetpack Compose',
    'kmp-printer',
    'PT Batamfast Indonesia'
  ]
  let result = text
  highlights.forEach(word => {
    const regex = new RegExp(`(${word})`, 'gi')
    result = result.replace(regex, '<span class="text-main font-bold">$1</span>')
  })
  return result
}
</script>
