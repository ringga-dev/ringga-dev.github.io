<template>
  <div class="pt-32 md:pt-44 pb-24 px-6 min-h-screen relative overflow-hidden">
    <div class="max-w-7xl mx-auto relative z-10">
      <SectionHeader 
        badge="Portfolio" 
        description="A comprehensive showcase of my open-source contributions and professional developments across mobile and web platforms."
        centered
      >
        <template #title>
          Selected <span class="text-gradient">Projects</span>
        </template>
      </SectionHeader>

      <!-- Filters -->
      <div class="flex flex-wrap justify-center gap-4 mb-16 scroll-reveal">
        <button 
          v-for="cat in categories" 
          :key="cat"
          @click="activeCategory = cat"
          class="px-8 py-2.5 rounded-xl text-sm font-black transition-all duration-300 border uppercase tracking-widest"
          :class="[activeCategory === cat ? 'bg-brand border-brand text-surface shadow-lg shadow-brand/20' : 'bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700']"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-10">
        <ProjectCard 
          v-for="(project, index) in filteredProjects" 
          :key="project.title" 
          v-bind="project" 
          class="scroll-reveal"
          :style="{ transitionDelay: `${(index % 3 + 1) * 100}ms` }"
        />
      </div>

      <!-- Bottom CTA -->
      <div class="mt-32 text-center scroll-reveal">
        <div class="glass-card p-12 rounded-[3rem] border-white/5 inline-block max-w-2xl">
          <h3 class="mb-6 font-black">Interested in Collaboration?</h3>
          <p class="text-slate-400 mb-8 font-medium">I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.</p>
          <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" target="_blank" class="btn-primary">
            Get Started Now
          </a>
        </div>
      </div>
    </div>

    <BackToTop />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useScrollReveal } from '~/composables/useScrollReveal'

useHead({
  title: 'Projects | Ringga Dev - Professional Portfolio',
})

// Scroll Reveal is now handled globally in app.vue

const activeCategory = ref('All')
const categories = ['All', 'Android', 'Library', 'Backend']

const filteredProjects = computed(() => {
  if (activeCategory.value === 'All') return projects
  return projects.filter(p => p.category.includes(activeCategory.value))
})


const projects = [
  {
    title: 'Printer-ESC-POS',
    description: 'A powerful Kotlin library for ESC/POS thermal printers, supporting Bluetooth, USB, and TCP connections.',
    image: '/images/projects/printer.png',
    category: 'Kotlin Library',
    tags: ['Kotlin', 'Android', 'Hardware'],
    github: 'https://github.com/ringga-dev/Printer-ESC-POS',
    link: 'https://github.com/ringga-dev/Printer-ESC-POS'
  },
  {
    title: 'Diggo POS Android',
    description: 'A comprehensive Point of Sale system for Android, featuring inventory management and transaction tracking.',
    image: '/images/projects/diggo.png',
    category: 'Android App',
    tags: ['Kotlin', 'MVVM', 'Room'],
    github: 'https://github.com/ringga-dev/diggo-pos-android',
    link: '#'
  },
  {
    title: 'POS LaundryQ',
    description: 'Niche POS solution tailored for laundry businesses with order status monitoring and customer database.',
    image: '/images/projects/laundryq.png',
    category: 'Android App',
    tags: ['Kotlin', 'Jetpack', 'Firebase'],
    github: 'https://github.com/ringga-dev/POS-LaundryQ',
    link: '#'
  },
  {
    title: 'Hotel BE',
    description: 'Robust back-end service for hotel management systems, handling bookings, room status, and guest data.',
    image: '/images/projects/hotel.png',
    category: 'Backend',
    tags: ['Kotlin', 'Spring Boot', 'MySQL'],
    github: 'https://github.com/ringga-dev/hotel_be',
    link: '#'
  },
  {
    title: 'TV Schedule',
    description: 'Real-time television scheduling application with reminder notifications and channel listings.',
    image: '/images/projects/tv.png',
    category: 'Android App',
    tags: ['Kotlin', 'Retrofit', 'Coroutines'],
    github: 'https://github.com/ringga-dev/TV-schedule',
    link: '#'
  },
  {
    title: 'Synapse',
    description: 'Innovative development project focused on data processing and system synchronization.',
    image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=1600',
    category: 'Development',
    tags: ['Kotlin', 'KMP', 'Architecture'],
    github: 'https://github.com/ringga-dev/Synapse',
    link: '#'
  }
]
</script>

