<template>
  <div>
    <Hero />
    
    <!-- Featured Projects -->
    <section class="max-w-6xl mx-auto px-6 py-20">
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
        <div>
          <h2 class="text-3xl md:text-4xl font-bold mb-4">Featured <span class="text-gradient">Projects</span></h2>
          <p class="text-white/50 max-w-md">A selection of my recent works where design meets code.</p>
        </div>
        <NuxtLink to="/projects" class="text-sm font-bold text-purple-400 hover:text-purple-300 flex items-center gap-2 group">
          Browse All Projects
          <ArrowRightIcon class="w-4 h-4 transition-transform group-hover:translate-x-1" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <ProjectCard 
          v-for="project in featuredProjects" 
          :key="project.title" 
          v-bind="project" 
        />
      </div>
    </section>

    <!-- Skills/Tech Stack -->
    <section class="max-w-6xl mx-auto px-6 py-20 bg-white/[0.02] border-y border-white/5">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold mb-4">Core <span class="text-gradient">Technologies</span></h2>
        <p class="text-white/40">The tools I use to build premium digital products.</p>
      </div>
      
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-8">
        <div v-for="tech in techStack" :key="tech.name" class="flex flex-col items-center gap-4 group">
          <div class="w-16 h-16 glass rounded-2xl flex items-center justify-center group-hover:bg-white/10 group-hover:scale-110 transition-all duration-300">
            <component :is="tech.icon" class="w-8 h-8 text-white/60 group-hover:text-purple-400 transition-colors" />
          </div>
          <span class="text-xs font-bold text-white/40 group-hover:text-white transition-colors tracking-widest uppercase">{{ tech.name }}</span>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="max-w-4xl mx-auto px-6 py-40 text-center">
      <h2 class="text-4xl md:text-6xl font-bold mb-8 leading-tight">Ready to start your <br/> <span class="text-gradient">next project?</span></h2>
      <p class="text-white/50 text-lg mb-12">I'm always open to discussing new projects, creative ideas or opportunities to be part of your visions.</p>
      <a href="mailto:contact@ringga.dev" class="btn-primary py-4 px-10 text-lg font-bold">
        Let's Connect
      </a>
    </section>
  </div>
</template>

<script setup>
import { ArrowRightIcon, DatabaseIcon, LayoutIcon, SmartphoneIcon, GlobeIcon, LayersIcon, ShieldCheckIcon } from 'lucide-vue-next'

const featuredProjects = [
  {
    title: 'E-Commerce Platform',
    description: 'A full-featured online store with real-time inventory and AI-powered recommendations.',
    image: 'https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&q=80&w=1600',
    category: 'Web Application',
    tags: ['Nuxt', 'Supabase', 'Tailwind'],
    github: '#',
    link: '#'
  },
  {
    title: 'Fintech Dashboard',
    description: 'Complex data visualization and management system for financial institutions.',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1600',
    category: 'SaaS Product',
    tags: ['Vue 3', 'Chart.js', 'PostgreSQL'],
    github: '#',
    link: '#'
  }
]

const techStack = [
  { name: 'Frontend', icon: GlobeIcon },
  { name: 'Backend', icon: DatabaseIcon },
  { name: 'UI/UX', icon: LayoutIcon },
  { name: 'Mobile', icon: SmartphoneIcon },
  { name: 'Architecture', icon: LayersIcon },
  { name: 'Security', icon: ShieldCheckIcon }
]
</script>
