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
          <h1 class="text-4xl font-bold mb-6">Hello, I'm <span class="text-gradient">Ringga Septia Pribadi</span></h1>
          <p class="text-white/60 mb-6 leading-relaxed">
            I'm an Android & Web Developer with 3 years of experience. I can build applications either independently or in a team, starting from back-end & front-end.
          </p>
          <p class="text-white/60 mb-8 leading-relaxed">
            I specialize in building Android applications with beautiful user interfaces and responsive web applications that look attractive on every screen.
          </p>
          <div class="flex gap-4">
            <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="btn-primary">Get in Touch</a>
            <div class="flex gap-4 items-center px-4">
              <a href="https://github.com/ringga-dev" class="text-white/40 hover:text-white transition-colors"><GithubIcon class="w-5 h-5" /></a>
              <a href="https://www.facebook.com/ringga.septia/" class="text-white/40 hover:text-white transition-colors"><FacebookIcon class="w-5 h-5" /></a>
              <a href="https://www.instagram.com/ringga_dev/" class="text-white/40 hover:text-white transition-colors"><InstagramIcon class="w-5 h-5" /></a>
            </div>
          </div>
        </div>
      </div>

      <!-- Skills -->
      <div class="mb-32">
        <h2 class="text-2xl font-bold mb-12">My <span class="text-gradient">Skills</span></h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div v-for="skill in skills" :key="skill.name" class="glass-card p-6 rounded-2xl text-center">
            <div class="text-2xl font-bold text-white mb-2">{{ skill.level }}%</div>
            <div class="text-white/50 text-sm font-medium">{{ skill.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { GithubIcon, FacebookIcon, InstagramIcon } from 'lucide-vue-next'

const skills = [
  { name: 'Android Studio', level: 85 },
  { name: 'Kotlin', level: 75 },
  { name: 'MySQL', level: 90 },
  { name: 'JavaScript', level: 70 },
  { name: 'CSS', level: 60 },
  { name: 'RESTful API', level: 75 },
  { name: 'PHP (CI4/CI3)', level: 75 },
  { name: 'Compose', level: 50 }
]
</script>
