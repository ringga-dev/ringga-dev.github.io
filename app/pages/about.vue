<template>
  <div class="pt-48 pb-32 px-6 relative overflow-hidden">
    <div class="bg-mesh"></div>
    
    <div class="max-w-6xl mx-auto relative z-10">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-24 items-start mb-40">
        <div class="animate-reveal [animation-delay:200ms] relative group max-w-md mx-auto lg:mx-0">
          <div class="absolute inset-0 bg-[#00DC82] rounded-[3rem] blur-3xl opacity-10 group-hover:opacity-20 transition-opacity duration-700"></div>
          <div class="relative glass rounded-[3.5rem] p-4 aspect-square">
            <img 
              src="https://avatars.githubusercontent.com/u/76124039?v=4" 
              alt="Ringga Septia Pribadi" 
              class="rounded-[2.8rem] w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 shadow-2xl" 
            />
          </div>
        </div>
        
        <div class="animate-reveal [animation-delay:400ms]">
          <h1 class="text-5xl md:text-7xl font-black mb-10 leading-tight">
            I'm <span class="text-gradient">Ringga Septia Pribadi</span>
          </h1>
          <p class="text-slate-400 text-lg md:text-xl mb-8 leading-relaxed font-medium">
            A results-driven Android & Web Developer with over 3 years of professional experience. I specialize in building robust digital infrastructures that scale.
          </p>
          <p class="text-slate-400 text-lg mb-12 leading-relaxed">
            My expertise lies in Kotlin, Nuxt, and high-performance system architecture. I am passionate about open-source and contribute to several hardware integration libraries.
          </p>
          
          <div class="flex flex-wrap gap-6 items-center">
            <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="btn-primary flex items-center gap-3 px-8">
              Let's Talk
              <MessageCircleIcon class="w-5 h-5" />
            </a>
            <div class="flex gap-6 items-center px-6">
              <a href="https://github.com/ringga-dev" class="nav-link"><GithubIcon class="w-6 h-6" /></a>
              <a href="https://www.facebook.com/ringga.septia/" class="nav-link"><FacebookIcon class="w-6 h-6" /></a>
              <a href="https://www.instagram.com/ringga_dev/" class="nav-link"><InstagramIcon class="w-6 h-6" /></a>
            </div>
          </div>
        </div>
      </div>

      <!-- Skills Section -->
      <div class="mb-40 animate-reveal [animation-delay:600ms]">
        <h2 class="text-3xl md:text-5xl font-black mb-16 text-center">Core <span class="text-gradient">Competencies</span></h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div v-for="skill in skills" :key="skill.name" class="glass-card p-10 rounded-[2.5rem] text-center group">
            <div class="text-4xl font-black text-[#00DC82] mb-3 group-hover:scale-110 transition-transform duration-300">{{ skill.level }}%</div>
            <div class="text-slate-400 text-sm font-bold uppercase tracking-widest">{{ skill.name }}</div>
          </div>
        </div>
      </div>

      <!-- Experience Section -->
      <div class="animate-reveal [animation-delay:800ms]">
        <h2 class="text-3xl md:text-5xl font-black mb-16 text-center">Work <span class="text-gradient">Experience</span></h2>
        <div class="space-y-10">
          <div v-for="job in experience" :key="job.company" class="glass-card p-10 rounded-[2.5rem] flex flex-col md:flex-row justify-between gap-10 items-center">
            <div class="flex-1">
              <h3 class="text-2xl font-black mb-2">{{ job.role }}</h3>
              <p class="text-[#00DC82] font-extrabold text-lg mb-6">{{ job.company }}</p>
              <p class="text-slate-400 text-lg leading-relaxed font-medium">{{ job.description }}</p>
            </div>
            <div class="px-6 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-500 text-sm font-black uppercase tracking-widest whitespace-nowrap">
              {{ job.period }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { GithubIcon, FacebookIcon, InstagramIcon, MessageCircleIcon } from 'lucide-vue-next'

const skills = [
  { name: 'Android / Kotlin', level: 90 },
  { name: 'Nuxt / Vue', level: 85 },
  { name: 'Hardware / POS', level: 95 },
  { name: 'MySQL / DB', level: 88 },
  { name: 'JavaScript', level: 80 },
  { name: 'Architecture', level: 85 },
  { name: 'API Design', level: 92 },
  { name: 'Git Workflow', level: 88 }
]

const experience = [
  {
    role: 'Lead Full-Stack Developer',
    company: 'Freelance / Open Source',
    period: '2021 - Present',
    description: 'Developed and maintained high-impact open-source libraries for ESC/POS printing and managed complex POS system implementations for diverse clients.'
  },
  {
    role: 'Android Developer',
    company: 'Tech Solutions',
    period: '2019 - 2021',
    description: 'Designed and implemented intuitive mobile applications with a focus on hardware integration and real-time data synchronization.'
  },
  {
    role: 'Web Developer',
    company: 'Creative Studio',
    period: '2018 - 2019',
    description: 'Crafted responsive and interactive websites using modern frontend frameworks and ensured cross-platform compatibility.'
  }
]
</script>
