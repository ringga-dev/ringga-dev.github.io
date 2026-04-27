<template>
  <div class="pt-40 pb-20 px-6">
    <div class="max-w-4xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-center mb-32">
        <div class="relative group">
          <div class="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl blur-2xl opacity-20 group-hover:opacity-40 transition-opacity"></div>
          <div class="relative glass rounded-3xl p-2 aspect-square">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=1000" alt="Ringga Dev" class="rounded-2xl w-full h-full object-cover" />
          </div>
        </div>
        
        <div>
          <h1 class="text-4xl font-bold mb-6">Hello, I'm <span class="text-gradient">Ringga Dev</span></h1>
          <p class="text-white/60 mb-6 leading-relaxed">
            I am a passionate Full-Stack Developer with over 5 years of experience in building digital products that combine aesthetic design with robust engineering.
          </p>
          <p class="text-white/60 mb-8 leading-relaxed">
            My philosophy is simple: build things that people love to use. I specialize in Nuxt, Vue, and modern cloud architectures.
          </p>
          <div class="flex gap-4">
            <a href="#" class="btn-primary">Download CV</a>
            <div class="flex gap-4 items-center px-4">
              <a href="#" class="text-white/40 hover:text-white transition-colors"><GithubIcon class="w-5 h-5" /></a>
              <a href="#" class="text-white/40 hover:text-white transition-colors"><LinkedinIcon class="w-5 h-5" /></a>
              <a href="#" class="text-white/40 hover:text-white transition-colors"><TwitterIcon class="w-5 h-5" /></a>
            </div>
          </div>
        </div>
      </div>

      <!-- Experience -->
      <div class="mb-32">
        <h2 class="text-2xl font-bold mb-12">Work <span class="text-gradient">Experience</span></h2>
        <div class="space-y-8">
          <div v-for="job in experience" :key="job.company" class="glass-card p-8 rounded-3xl flex flex-col md:flex-row justify-between gap-6">
            <div>
              <h3 class="text-xl font-bold mb-1">{{ job.role }}</h3>
              <p class="text-purple-400 font-medium mb-4">{{ job.company }}</p>
              <p class="text-white/50 text-sm max-w-xl">{{ job.description }}</p>
            </div>
            <div class="text-white/30 text-sm font-bold uppercase tracking-widest pt-1">
              {{ job.period }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { GithubIcon, LinkedinIcon, TwitterIcon } from 'lucide-vue-next'

const experience = [
  {
    role: 'Senior Frontend Engineer',
    company: 'Global Tech Solutions',
    period: '2022 - Present',
    description: 'Leading the frontend development of a massive SaaS platform using Nuxt 3 and high-performance micro-frontends.'
  },
  {
    role: 'Full Stack Developer',
    company: 'Creative Digital Agency',
    period: '2020 - 2022',
    description: 'Developed over 20+ custom web applications for international clients with a focus on interactive UI.'
  },
  {
    role: 'Junior Web Developer',
    company: 'Local Startup',
    period: '2018 - 2020',
    description: 'Mastered the fundamentals of web development and contributed to several early-stage MVP products.'
  }
]
</script>
