<template>
  <div>
    <div class="bg-mesh"></div>
    <Hero />
    
    <!-- Featured Projects -->
    <section class="max-w-7xl mx-auto px-6 py-32 relative z-10">
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-20 gap-8">
        <div class="animate-reveal">
          <h2 class="text-4xl md:text-6xl font-black mb-6">Featured <span class="text-gradient">Work</span></h2>
          <p class="text-slate-400 max-w-md text-lg font-medium leading-relaxed">A selection of high-impact developments in the Android and Web ecosystem.</p>
        </div>
        <NuxtLink to="/projects" class="animate-reveal inline-flex items-center gap-3 text-[#00DC82] font-black uppercase tracking-widest text-sm hover:translate-x-2 transition-transform duration-300">
          All Projects
          <ArrowRightIcon class="w-5 h-5" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <ProjectCard 
          v-for="(project, index) in featuredProjects" 
          :key="project.title" 
          v-bind="project" 
          class="animate-reveal"
          :style="{ animationDelay: `${(index + 1) * 200}ms` }"
        />
      </div>
    </section>

    <!-- Services / Tech -->
    <section class="max-w-7xl mx-auto px-6 py-32 relative z-10 overflow-hidden">
      <div class="glass-card p-16 rounded-[4rem] border-slate-800/30 relative overflow-hidden">
        <div class="nuxt-glow top-0 right-0"></div>
        <div class="text-center mb-24 relative z-10">
          <h2 class="text-4xl md:text-6xl font-black mb-6">Built with <span class="text-gradient">Precision</span></h2>
          <p class="text-slate-400 text-lg md:text-xl font-medium max-w-2xl mx-auto">Leveraging modern stacks to deliver seamless and scalable digital experiences.</p>
        </div>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-12 relative z-10">
          <div v-for="tech in techStack" :key="tech.name" class="flex flex-col items-center gap-6 group">
            <div class="w-20 h-20 glass rounded-[2rem] flex items-center justify-center group-hover:bg-[#00DC82]/10 group-hover:scale-110 transition-all duration-500 border-slate-800/30 group-hover:border-[#00DC82]/30">
              <component :is="tech.icon" class="w-8 h-8 text-slate-400 group-hover:text-[#00DC82] transition-colors duration-300" />
            </div>
            <span class="text-xs font-black text-slate-500 group-hover:text-slate-200 transition-colors duration-300 tracking-[0.2em] uppercase">{{ tech.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="max-w-5xl mx-auto px-6 py-48 text-center relative z-10">
      <div class="animate-reveal">
        <h2 class="text-5xl md:text-8xl font-black mb-10 leading-[1.1]">Let's build <br/> something <span class="text-gradient">Extraordinary.</span></h2>
        <p class="text-slate-400 text-lg md:text-2xl mb-16 max-w-2xl mx-auto font-medium leading-relaxed">Available for freelance projects and technical collaborations. Ready to elevate your digital presence?</p>
        <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="btn-primary py-5 px-12 text-xl shadow-2xl">
          Get in Touch
        </a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ArrowRightIcon, DatabaseIcon, LayoutIcon, SmartphoneIcon, GlobeIcon, LayersIcon, ShieldCheckIcon } from 'lucide-vue-next'

const featuredProjects = [
  {
    title: 'Printer-ESC-POS',
    description: 'Premier Kotlin library for advanced thermal printing solutions on Android devices.',
    image: 'https://images.unsplash.com/photo-1585336139118-10c9f7904609?auto=format&fit=crop&q=80&w=1600',
    category: 'Kotlin / Hardware',
    tags: ['Kotlin', 'Bluetooth', 'USB'],
    github: 'https://github.com/ringga-dev/Printer-ESC-POS',
    link: '#'
  },
  {
    title: 'Diggo POS Android',
    description: 'Enterprise-grade point of sale application with real-time analytics and inventory sync.',
    image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&q=80&w=1600',
    category: 'Mobile / Fintech',
    tags: ['Android SDK', 'MVVM', 'SQLite'],
    github: 'https://github.com/ringga-dev/diggo-pos-android',
    link: '#'
  }
]

const techStack = [
  { name: 'Android', icon: SmartphoneIcon },
  { name: 'Web', icon: GlobeIcon },
  { name: 'Database', icon: DatabaseIcon },
  { name: 'Design', icon: LayoutIcon },
  { name: 'System', icon: LayersIcon },
  { name: 'Security', icon: ShieldCheckIcon }
]
</script>
