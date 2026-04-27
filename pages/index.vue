<template>
  <div>
    <Hero />
    
    <!-- Services Section -->
    <section class="max-w-7xl mx-auto px-6 py-32 relative z-10">
      <SectionHeader 
        badge="Strategic Expertise" 
        description="Crafting high-performance digital ecosystems with technical precision and architectural excellence."
        centered
      >
        <template #title>
          Precision <span class="text-gradient">Engineering</span>
        </template>
      </SectionHeader>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-20">
        <ServiceCard 
          v-for="service in services" 
          :key="service.title" 
          v-bind="service"
        />
      </div>
    </section>
    
    <!-- Stats Section -->
    <section class="max-w-7xl mx-auto px-6 py-20 relative z-10">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-12">
        <div v-for="stat in stats" :key="stat.label" class="glass-card p-8 rounded-[2rem] text-center group scroll-reveal relative overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-brand/20 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
          <div class="flex justify-center mb-6">
            <div class="w-14 h-14 rounded-2xl bg-brand/5 flex items-center justify-center text-brand group-hover:bg-brand group-hover:text-surface transition-all duration-500">
              <component :is="stat.icon" class="w-7 h-7" />
            </div>
          </div>
          <div class="text-4xl md:text-5xl font-heading font-black text-white mb-2 transition-transform duration-500">
            <AnimatedCounter :target="stat.value" />{{ stat.suffix }}
          </div>
          <div class="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">
            {{ stat.label }}
          </div>
        </div>
      </div>
    </section>

    <!-- Projects Section -->
    <section class="max-w-7xl mx-auto px-6 py-20 relative z-10">
      <SectionHeader 
        badge="Technical Milestones" 
        description="A curated selection of high-impact innovations across the digital landscape."
      >
        <template #title>
          Featured <span class="text-gradient">Innovations</span>
        </template>
      </SectionHeader>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <ProjectCard 
          v-for="(project, index) in featuredProjects" 
          :key="project.title" 
          v-bind="project" 
          class="scroll-reveal"
          :style="{ transitionDelay: `${(index + 1) * 150}ms` }"
        />
      </div>

      <div class="mt-16 text-center scroll-reveal">
        <NuxtLink to="/projects" class="btn-secondary inline-flex items-center gap-3">
          Explore All Projects
          <ArrowRightIcon class="w-5 h-5" />
        </NuxtLink>
      </div>
    </section>

    <!-- Services / Tech -->
    <section class="max-w-7xl mx-auto px-6 py-24 relative z-10 overflow-hidden">
      <div class="glass-card p-12 md:p-24 rounded-[3rem] md:rounded-[5rem] border-white/5 relative overflow-hidden scroll-reveal">
        <div class="absolute top-0 right-0 w-64 h-64 bg-brand/10 blur-[80px]"></div>
        
        <SectionHeader 
          badge="Our Stack" 
          description="Leveraging modern industry-standard technologies to deliver seamless and scalable digital experiences."
          centered
        >
          <template #title>
            Built with <span class="text-gradient">Technical Precision</span>
          </template>
        </SectionHeader>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-12 relative z-10">
          <div v-for="tech in techStack" :key="tech.name" class="flex flex-col items-center gap-6 group">
            <div class="w-20 h-20 glass rounded-[2.5rem] flex items-center justify-center group-hover:bg-brand/10 group-hover:scale-110 group-hover:border-brand/30 transition-all duration-500">
              <component :is="tech.icon" class="w-9 h-9 text-slate-400 group-hover:text-brand transition-colors duration-300" />
            </div>
            <span class="text-[10px] font-black text-slate-500 group-hover:text-white transition-colors duration-300 tracking-[0.2em] uppercase">{{ tech.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="max-w-5xl mx-auto px-6 py-24 md:py-40 text-center relative z-10">
      <div class="scroll-reveal">
        <h2 class="mb-8 leading-[1.1] font-black">
          Let's build something <br/> 
          <span class="text-gradient underline decoration-brand/30 underline-offset-8">Extraordinary.</span>
        </h2>
        <p class="text-slate-400 text-lg md:text-2xl mb-16 max-w-2xl mx-auto font-medium leading-relaxed">
          Available for freelance projects and technical collaborations. Ready to elevate your digital presence with world-class engineering?
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-6">
          <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" target="_blank" class="btn-primary py-5 px-12 text-lg shadow-2xl w-full sm:w-auto">
            Start a Conversation
          </a>
          <a href="mailto:ringgadev@gmail.com" class="btn-secondary py-5 px-12 text-lg w-full sm:w-auto">
            Email Me
          </a>
        </div>
      </div>
    </section>
    
    <BackToTop />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ArrowRightIcon, 
  DatabaseIcon, 
  LayoutIcon, 
  SmartphoneIcon, 
  GlobeIcon, 
  LayersIcon, 
  ShieldCheckIcon,
  CalendarIcon,
  FolderIcon,
  StarIcon,
  UsersIcon,
  Code2Icon,
  CpuIcon,
  BoxIcon
} from 'lucide-vue-next'
import { useScrollReveal } from '~/composables/useScrollReveal'

useHead({
  title: 'Ringga Dev | Professional Multi-Platform Engineer',
})

// Scroll Reveal is now handled globally in app.vue

const stats = ref([
  { label: 'Years Experience', value: '3', suffix: '+', icon: CalendarIcon },
  { label: 'Projects Done', value: '25', suffix: '+', icon: FolderIcon },
  { label: 'GitHub Stars', value: '0', suffix: '+', icon: StarIcon },
  { label: 'Repositories', value: '0', suffix: '+', icon: UsersIcon }
])

onMounted(async () => {
  try {
    const res = await fetch('https://api.github.com/users/ringga-dev')
    const data = await res.json()
    if (data.public_repos) {
      stats.value[3].value = data.public_repos.toString()
    }
    
    // Fetch stars (approximate or via search)
    const reposRes = await fetch('https://api.github.com/users/ringga-dev/repos?per_page=100')
    const repos = await reposRes.json()
    const stars = repos.reduce((acc, repo) => acc + repo.stargazers_count, 0)
    stats.value[2].value = stars.toString()
  } catch (e) {
    console.error('Failed to fetch GitHub stats')
    stats.value[2].value = '100' // Fallback
    stats.value[3].value = '14' // Fallback
  }
})

const services = [
  {
    title: 'Cross-Platform Apps',
    description: 'Expertise in building high-performance apps for Mobile, Desktop, and Web using Kotlin Multiplatform.',
    icon: SmartphoneIcon,
    features: ['Single Codebase', 'Native UI/UX', 'Shared Business Logic']
  },
  {
    title: 'Hardware & Systems',
    description: 'Specialized in hardware integration, thermal printing, and low-level system communication.',
    icon: CpuIcon,
    features: ['ESC/POS Integration', 'USB/Bluetooth/TCP', 'Driver Development']
  },
  {
    title: 'Enterprise Architecture',
    description: 'Designing scalable architectures with Clean Architecture, SOLID principles, and modern design patterns.',
    icon: LayersIcon,
    features: ['Modular Design', 'MVVM/MVI', 'Reactive Streams']
  }
]

const featuredProjects = [
  {
    title: 'Printer-ESC-POS',
    description: 'Premier Kotlin library for advanced thermal printing solutions on Android devices. Supports Bluetooth, USB, and TCP.',
    image: '/images/branding/logo-software.jpeg',
    category: 'Library / Android',
    tags: ['Kotlin', 'Bluetooth', 'Hardware'],
    github: 'https://github.com/ringga-dev/Printer-ESC-POS',
    link: '#'
  },
  {
    title: 'Diggo POS Android',
    description: 'Enterprise-grade point of sale application with real-time analytics, inventory sync, and multi-branch support.',
    image: '/images/projects/project-pos-confirmation.png',
    category: 'Fintech / Mobile',
    tags: ['Android SDK', 'MVVM', 'SQLite'],
    github: 'https://github.com/ringga-dev/diggo-pos-android',
    link: '#'
  }
]

const techStack = [
  { name: 'Android', icon: SmartphoneIcon },
  { name: 'Web', icon: GlobeIcon },
  { name: 'Database', icon: DatabaseIcon },
  { name: 'UI/UX', icon: LayoutIcon },
  { name: 'Architecture', icon: LayersIcon },
  { name: 'Security', icon: ShieldCheckIcon }
]
</script>

