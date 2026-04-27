<template>
  <div class="pt-40 pb-20 px-6 min-h-screen relative overflow-hidden">
    <div class="bg-mesh"></div>
    
    <div class="max-w-7xl mx-auto relative z-10">
      <div class="mb-24 text-center animate-reveal">
        <h1 class="text-6xl md:text-8xl font-black mb-8 leading-tight">
          Selected <span class="text-gradient">Projects</span>
        </h1>
        <p class="text-slate-400 max-w-2xl mx-auto text-lg md:text-xl leading-relaxed">
          A showcase of my open-source contributions and professional developments in Android and Web ecosystems.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <ProjectCard 
          v-for="(project, index) in projects" 
          :key="project.title" 
          v-bind="project" 
          class="animate-reveal"
          :style="{ animationDelay: `${(index + 1) * 150}ms` }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const projects = [
  {
    title: 'Printer-ESC-POS',
    description: 'A powerful Kotlin library for ESC/POS thermal printers, supporting Bluetooth, USB, and TCP connections.',
    image: 'https://images.unsplash.com/photo-1585336139118-10c9f7904609?auto=format&fit=crop&q=80&w=1600',
    category: 'Kotlin Library',
    tags: ['Kotlin', 'Android', 'Hardware'],
    github: 'https://github.com/ringga-dev/Printer-ESC-POS',
    link: 'https://github.com/ringga-dev/Printer-ESC-POS'
  },
  {
    title: 'Diggo POS Android',
    description: 'A comprehensive Point of Sale system for Android, featuring inventory management and transaction tracking.',
    image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&q=80&w=1600',
    category: 'Android App',
    tags: ['Kotlin', 'MVVM', 'Room'],
    github: 'https://github.com/ringga-dev/diggo-pos-android',
    link: '#'
  },
  {
    title: 'POS LaundryQ',
    description: 'Niche POS solution tailored for laundry businesses with order status monitoring and customer database.',
    image: 'https://images.unsplash.com/photo-1545173168-9f1947eebb9f?auto=format&fit=crop&q=80&w=1600',
    category: 'Android App',
    tags: ['Kotlin', 'Android Jetpack', 'Firebase'],
    github: 'https://github.com/ringga-dev/POS-LaundryQ',
    link: '#'
  },
  {
    title: 'Hotel BE',
    description: 'Robust back-end service for hotel management systems, handling bookings, room status, and guest data.',
    image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80&w=1600',
    category: 'Backend',
    tags: ['Kotlin', 'Spring Boot', 'MySQL'],
    github: 'https://github.com/ringga-dev/hotel_be',
    link: '#'
  },
  {
    title: 'TV Schedule',
    description: 'Real-time television scheduling application with reminder notifications and channel listings.',
    image: 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?auto=format&fit=crop&q=80&w=1600',
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
    tags: ['Kotlin', 'Architecture', 'Clean Code'],
    github: 'https://github.com/ringga-dev/Synapse',
    link: '#'
  }
]
</script>
