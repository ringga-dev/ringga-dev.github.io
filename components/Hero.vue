<template>
  <section class="min-h-screen flex flex-col items-center justify-center pt-32 pb-20 px-6 text-center relative overflow-hidden">
    <!-- Animated Decoration -->
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-brand/5 blur-[100px] animate-pulse-slow"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-brand-light/5 blur-[100px] animate-pulse-slow"></div>

    <!-- Floating Decorative Elements -->
    <div class="absolute top-20 left-10 w-24 h-24 border border-brand/20 rounded-full animate-float-slow hidden lg:block"></div>
    <div class="absolute bottom-40 right-20 w-16 h-16 border border-brand-light/20 rounded-lg rotate-12 animate-float hidden lg:block"></div>
    <div class="absolute top-1/2 left-20 text-brand/10 text-8xl font-black select-none hidden xl:block">&lt;/&gt;</div>
    <div class="absolute bottom-1/2 right-20 text-brand-light/10 text-8xl font-black select-none hidden xl:block">{}</div>

    <div class="scroll-reveal mb-8">
      <div class="relative inline-block group">
        <div class="absolute inset-0 bg-brand rounded-full blur-3xl opacity-20 group-hover:opacity-40 transition-opacity"></div>
        <div class="relative p-1.5 rounded-full bg-gradient-to-tr from-brand to-brand-light">
          <img 
            src="/images/branding/logo-3d.jpeg" 
            alt="Ringga Septia Pribadi" 
            class="w-32 h-32 md:w-44 md:h-44 rounded-full object-cover border-4 border-surface shadow-2xl"
          />
        </div>
      </div>
    </div>

    <div class="scroll-reveal inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand/10 border border-brand/20 text-brand text-[10px] md:text-xs font-black mb-8">
      <span class="relative flex h-2 w-2">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-brand"></span>
      </span>
      OPEN FOR NEW PROJECTS & COLLABORATIONS
    </div>
    
    <h1 class="scroll-reveal mb-8 leading-[1] font-black">
      Digital <span class="text-brand">Architect</span> & <br />
      <span class="text-gradient">{{ typedRole }}</span><span class="animate-pulse text-brand">|</span>
    </h1>
    
    <p class="scroll-reveal text-slate-400 max-w-2xl text-lg md:text-xl mb-12 leading-relaxed font-medium">
      Crafting high-performance <span class="text-white">Multi-Platform</span> solutions across Mobile, Desktop, and Web with <span class="text-white">3+ years</span> of technical excellence.
    </p>
    
    <div class="scroll-reveal flex flex-col sm:flex-row gap-4 mb-24">
      <NuxtLink to="/projects" class="btn-primary flex items-center justify-center gap-3 px-10 py-4 group">
        View Portfolio
        <ArrowRightIcon class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
      </NuxtLink>
      <NuxtLink to="/about" class="btn-secondary flex items-center justify-center gap-3 px-10 py-4">
        My Story
      </NuxtLink>
    </div>

    <!-- Tech Stack Icons -->
    <div class="scroll-reveal w-full max-w-5xl border-t border-white/5 pt-12">
      <p class="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 mb-8">Our Core Stack</p>
      <div class="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-10 gap-4 md:gap-6 opacity-80">
        <div v-for="tech in techItems" :key="tech.name" class="flex flex-col items-center gap-3 group cursor-default">
          <div class="p-3 bg-slate-900 rounded-2xl border border-slate-800 group-hover:border-brand/30 group-hover:bg-brand/5 transition-all">
            <component :is="tech.icon" class="w-5 h-5 group-hover:text-brand" />
          </div>
          <span class="text-[8px] font-black text-slate-400 tracking-widest uppercase group-hover:text-white">{{ tech.name }}</span>
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
  GlobeIcon, 
  DatabaseIcon, 
  CodeIcon, 
  LayersIcon, 
  CpuIcon,
  ZapIcon,
  BoxIcon,
  ShieldCheckIcon,
  TerminalIcon,
  CloudIcon,
  ServerIcon,
  ActivityIcon
} from 'lucide-vue-next'

const roles = ['Multi-Platform Developer', 'KMP/CMP Expert', 'Systems Architect', 'Full-Stack Engineer']
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

  let typeSpeed = isDeleting ? 50 : 100

  if (!isDeleting && charIndex === currentRole.length) {
    typeSpeed = 2000
    isDeleting = true
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false
    roleIndex = (roleIndex + 1) % roles.length
    typeSpeed = 500
  }

  setTimeout(typeEffect, typeSpeed)
}

onMounted(() => {
  typeEffect()
})

const techItems = [
  { name: 'KMP', icon: ZapIcon },
  { name: 'CMP', icon: BoxIcon },
  { name: 'Android', icon: SmartphoneIcon },
  { name: 'Kotlin', icon: CodeIcon },
  { name: 'Nuxt', icon: LayersIcon },
  { name: 'Spring', icon: ServerIcon },
  { name: 'Node.js', icon: TerminalIcon },
  { name: 'Hilt', icon: ShieldCheckIcon },
  { name: 'Firebase', icon: CloudIcon },
  { name: 'DB', icon: DatabaseIcon }
]
</script>

