<template>
  <div class="bg-surface">
    <!-- Hero Section -->
    <HomeHero />
    
    <!-- Services Section -->
    <HomeServices />
    
    <!-- Stats Section -->
    <HomeStats />

    <!-- Technical Methodology (Infographics) Section -->
    <HomeCapabilities />

    <!-- Showcase Banner Section -->
    <HomeShowcaseBanner />

    <!-- Featured Projects Section -->
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
        <NuxtLink to="/projects" class="btn-secondary inline-flex items-center gap-3 py-4 px-10 text-xs font-black uppercase tracking-wider">
          Explore All Projects
          <ArrowRightIcon class="w-5 h-5" />
        </NuxtLink>
      </div>
    </section>

    <!-- Built with Tech precision is now embedded in HomeHero.vue stack footer -->

    <!-- Call to Action -->
    <section class="max-w-5xl mx-auto px-6 py-24 md:py-40 text-center relative z-10">
      <div class="scroll-reveal">
        <h2 class="mb-8 leading-[1.1] font-heading font-black text-main">
          Let's build something <br/> 
          <span class="text-gradient underline decoration-brand/30 underline-offset-8">Extraordinary.</span>
        </h2>
        <p class="text-muted text-lg md:text-2xl mb-16 max-w-2xl mx-auto font-medium leading-relaxed">
          Available for freelance projects and technical collaborations. Ready to elevate your digital presence with world-class engineering?
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-6">
          <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary py-5 px-12 text-sm shadow-2xl w-full sm:w-auto font-black uppercase tracking-wider">
            Start a Conversation
          </a>
          <a :href="globalData.socials.email" class="btn-secondary py-5 px-12 text-sm w-full sm:w-auto font-black uppercase tracking-wider">
            Email Me
          </a>
        </div>
      </div>
    </section>
    
    <BackToTop />
  </div>
</template>

<script setup>
import { ArrowRightIcon } from 'lucide-vue-next'
import globalData from '~/data/global.json'
import projectsData from '~/data/projects.json'

useHead({
  title: `${globalData.siteName} | Professional Multi-Platform Engineer`,
  meta: [
    { name: 'description', content: globalData.seo.description }
  ]
})

// Feature the first 2 projects from projects.json
const featuredProjects = projectsData.projects.slice(0, 2)
</script>
