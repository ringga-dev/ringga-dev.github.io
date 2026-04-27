<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 relative overflow-hidden">
    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Profile Header -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start mb-40">
        <div class="lg:col-span-5 scroll-reveal relative">
          <div class="absolute -top-10 -left-10 w-40 h-40 bg-brand/10 blur-[60px]"></div>
          <div class="relative p-4 glass rounded-[3.5rem] group overflow-hidden">
            <img 
              src="https://avatars.githubusercontent.com/u/76124039?v=4" 
              alt="Ringga Septia Pribadi" 
              class="rounded-[2.8rem] w-full aspect-square object-cover grayscale group-hover:grayscale-0 transition-all duration-1000 group-hover:scale-105" 
            />
            <div class="absolute inset-0 bg-brand/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </div>
          
          <!-- Experience Badge -->
          <div class="absolute -bottom-6 -right-6 glass p-6 rounded-[2rem] shadow-2xl border-brand/20 scroll-reveal" style="transition-delay: 400ms">
            <div class="text-3xl font-black text-brand leading-none mb-1">3+</div>
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Years of<br/>Expertise</div>
          </div>
        </div>
        
        <div class="lg:col-span-7 scroll-reveal" style="transition-delay: 200ms">
          <SectionHeader badge="Behind the Code">
            <template #title>
              I'm <span class="text-gradient">Ringga Septia Pribadi</span>
            </template>
          </SectionHeader>
          
          <div class="space-y-6 text-slate-400 text-lg md:text-xl font-medium leading-relaxed mb-12">
            <p>
              A results-driven <span class="text-white">Multi-Platform Engineer</span> specializing in Mobile, Desktop, and Web ecosystems. I bridge the gap between high-performance hardware and seamless user experiences using <span class="text-white">Kotlin Multiplatform</span>.
            </p>
            <p>
              My vision is centered on <span class="text-brand">Connectivity</span>—building systems that work everywhere, for everyone. From custom Android POS drivers to scalable Nuxt applications, I craft solutions that are as robust as they are intuitive.
            </p>
          </div>
          
          <div class="flex flex-wrap gap-6 items-center">
            <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" target="_blank" class="btn-primary flex items-center gap-3 px-10">
              Let's Collaborate
              <ExternalLinkIcon class="w-5 h-5" />
            </a>
            <a href="#" class="btn-secondary flex items-center gap-3 px-10">
              Download CV
              <DownloadIcon class="w-5 h-5" />
            </a>
            <div class="flex gap-4 items-center">
              <a v-for="social in socials" :key="social.name" :href="social.url" target="_blank" class="w-12 h-12 glass rounded-xl flex items-center justify-center text-slate-400 hover:text-brand transition-all">
                <component :is="social.icon" class="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Skills Section -->
      <div class="mb-40">
        <SectionHeader 
          badge="Expertise" 
          description="A specialized toolkit refined through years of professional development and complex problem-solving."
          centered
        >
          <template #title>Technical <span class="text-gradient">Toolkit</span></template>
        </SectionHeader>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-20">
          <SkillBar v-for="skill in skills" :key="skill.name" v-bind="skill" />
        </div>
      </div>

      <!-- Experience Section -->
      <div class="mb-20">
        <SectionHeader 
          badge="Professional Journey" 
          description="My evolution through various technical challenges and roles."
          centered
        >
          <template #title>Work <span class="text-gradient">Experience</span></template>
        </SectionHeader>

        <div class="max-w-4xl mx-auto mt-20 space-y-12 relative before:absolute before:left-0 md:before:left-8 before:top-4 before:bottom-4 before:w-px before:bg-gradient-to-b before:from-brand/50 before:via-brand-light/30 before:to-transparent">
          <div 
            v-for="job in experience" 
            :key="job.company" 
            class="relative pl-12 md:pl-24 scroll-reveal group"
          >
            <!-- Timeline Dot -->
            <div class="absolute left-0 md:left-8 -translate-x-1/2 top-0 w-4 h-4 rounded-full bg-surface border-2 border-brand shadow-[0_0_15px_rgba(0,220,130,0.3)] z-10 group-hover:scale-150 transition-transform duration-500">
              <div class="absolute inset-1 rounded-full bg-brand animate-pulse"></div>
            </div>
            
            <div class="glass-card p-8 rounded-[2rem] border-white/5 hover:border-brand/20 transition-all duration-500 hover:-translate-y-1">
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                  <h3 class="text-2xl font-black text-white mb-1 group-hover:text-brand transition-colors">{{ job.role }}</h3>
                  <p class="text-brand-light font-bold">{{ job.company }}</p>
                </div>
                <div class="px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-[10px] font-black uppercase tracking-widest whitespace-nowrap self-start md:self-center">
                  {{ job.period }}
                </div>
              </div>
              <p class="text-slate-400 leading-relaxed font-medium">
                {{ job.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <BackToTop />
  </div>
</template>

<script setup>
import { 
  GithubIcon, 
  LinkedinIcon, 
  MailIcon, 
  ExternalLinkIcon, 
  DownloadIcon,
  SmartphoneIcon,
  LayersIcon,
  CodeIcon,
  DatabaseIcon,
  ZapIcon,
  CpuIcon
} from 'lucide-vue-next'
import { useScrollReveal } from '~/composables/useScrollReveal'

useHead({
  title: 'About | Ringga Dev - Professional Portfolio',
})

// Scroll Reveal is now handled globally in app.vue


const socials = [
  { name: 'GitHub', icon: GithubIcon, url: 'https://github.com/ringga-dev' },
  { name: 'LinkedIn', icon: LinkedinIcon, url: 'https://linkedin.com/in/ringga-dev' },
  { name: 'Email', icon: MailIcon, url: 'mailto:ringga.dev@gmail.com' }
]

const skills = [
  { name: 'Android (Kotlin)', level: 95, icon: SmartphoneIcon },
  { name: 'KMP / CMP', level: 85, icon: ZapIcon },
  { name: 'Nuxt / Vue', level: 90, icon: LayersIcon },
  { name: 'Spring Boot', level: 80, icon: CodeIcon },
  { name: 'PostgreSQL', level: 85, icon: DatabaseIcon },
  { name: 'Clean Architecture', level: 90, icon: CpuIcon }
]

const experience = [
  {
    role: 'Lead Fullstack Engineer',
    company: 'Freelance & Open Source',
    period: '2021 - Present',
    description: 'Leading technical strategy for complex POS implementations and maintaining mission-critical Kotlin libraries for thermal printing technologies.'
  },
  {
    role: 'Android Systems Developer',
    company: 'Tech Solutions Global',
    period: '2019 - 2021',
    description: 'Focused on low-level hardware integration and building high-performance mobile applications with real-time data synchronization.'
  },
  {
    role: 'Frontend Developer',
    company: 'Pixel Creative Agency',
    period: '2018 - 2019',
    description: 'Developed interactive and high-conversion web platforms using modern JavaScript frameworks and responsive design principles.'
  }
]
</script>

