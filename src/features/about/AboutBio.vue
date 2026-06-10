<template>
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start mb-40">
    <!-- Profile Photo Section -->
    <div class="lg:col-span-5 scroll-reveal relative">
      <div class="absolute -top-10 -left-10 w-40 h-40 bg-brand/10 blur-[60px]"></div>
      <div class="relative p-4 glass rounded-[3.5rem] group overflow-hidden bg-surface-card border-border">
        <img 
          :src="aboutData.bio.image" 
          :alt="aboutData.bio.titleHighlight" 
          @error="onImgError"
          v-if="!imgError"
          class="rounded-[2.8rem] w-full aspect-square object-cover grayscale group-hover:grayscale-0 transition-all duration-1000 group-hover:scale-105" 
        />
        <div 
          v-else 
          class="rounded-[2.8rem] w-full aspect-square bg-surface-elevated border border-border flex items-center justify-center text-brand font-heading text-6xl font-black"
        >
          RD
        </div>
        <div class="absolute inset-0 bg-brand/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
      </div>
      
      <!-- Experience Badge -->
      <div class="absolute -bottom-6 -right-6 glass p-6 rounded-[2rem] shadow-2xl border-brand/20 scroll-reveal" style="transition-delay: 400ms">
        <div class="text-3xl font-black text-brand leading-none mb-1">{{ aboutData.bio.experienceYears }}</div>
        <div class="text-[10px] font-black text-muted uppercase tracking-widest leading-tight">Years of<br/>Expertise</div>
      </div>
    </div>
    
    <!-- Narrative Section -->
    <div class="lg:col-span-7 scroll-reveal" style="transition-delay: 200ms">
      <SectionHeader :badge="aboutData.bio.badge">
        <template #title>
          {{ aboutData.bio.title }} <span class="text-gradient">{{ aboutData.bio.titleHighlight }}</span>
        </template>
      </SectionHeader>
      
      <div class="space-y-6 text-muted text-lg md:text-xl font-medium leading-relaxed mb-12">
        <p v-for="(p, index) in aboutData.bio.paragraphs" :key="index" v-html="highlightKeywords(p)"></p>
      </div>
      
      <div class="flex flex-wrap gap-6 items-center">
        <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary flex items-center gap-3 px-10 text-xs font-black uppercase tracking-wider py-4">
          Let's Collaborate
          <ExternalLinkIcon class="w-5 h-5" />
        </a>
        <a :href="aboutData.bio.cvUrl" class="btn-secondary flex items-center gap-3 px-10 text-xs font-black uppercase tracking-wider py-4">
          Download CV
          <DownloadIcon class="w-5 h-5" />
        </a>
        <div class="flex gap-4 items-center">
          <a 
            v-for="social in socialList" 
            :key="social.name" 
            :href="social.url" 
            target="_blank" 
            class="w-12 h-12 glass rounded-xl flex items-center justify-center text-muted hover:text-brand hover:border-brand/35 hover:-translate-y-1 transition-all"
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
  ExternalLinkIcon, 
  DownloadIcon 
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
    'Multi-Platform Engineer',
    'Kotlin Multiplatform',
    'Connectivity',
    'Android POS drivers',
    'Nuxt applications'
  ]
  let result = text
  highlights.forEach(word => {
    const regex = new RegExp(`(${word})`, 'gi')
    result = result.replace(regex, '<span class="text-main font-bold">$1</span>')
  })
  return result
}
</script>
