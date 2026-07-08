<template>
  <div class="bg-surface">
    <!-- Hero -->
    <HomeHero />

    <!-- Divider -->
    <div class="h-px max-w-7xl mx-auto bg-gradient-to-r from-transparent via-border to-transparent"></div>

    <!-- Credibility stats -->
    <HomeStats />

    <!-- Divider -->
    <div class="h-px max-w-7xl mx-auto bg-gradient-to-r from-transparent via-border to-transparent"></div>

    <!-- Services / Expertise -->
    <HomeServices />

    <!-- Divider -->
    <div class="h-px max-w-7xl mx-auto bg-gradient-to-r from-transparent via-border to-transparent"></div>

    <!-- Showcase slider -->
    <HomeShowcaseBanner />

    <!-- Divider -->
    <div class="h-px max-w-7xl mx-auto bg-gradient-to-r from-transparent via-border to-transparent"></div>

    <!-- Capabilities / Methodology -->
    <HomeCapabilities />

    <!-- Featured Projects -->
    <section class="max-w-7xl mx-auto px-6 py-28 relative z-10">
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

    <!-- Call to Action -->
    <section class="relative z-10">
      <div class="max-w-5xl mx-auto px-6 pb-32 md:pb-40">
        <div class="glass-card rounded-[3rem] px-8 py-16 md:px-16 md:py-24 text-center relative overflow-hidden scroll-reveal">
          <div class="absolute -top-24 -left-24 w-72 h-72 bg-brand/10 rounded-full blur-[90px] pointer-events-none"></div>
          <div class="absolute -bottom-24 -right-24 w-72 h-72 bg-brand-light/10 rounded-full blur-[90px] pointer-events-none"></div>

          <h2 class="relative z-10 mb-6 leading-[1.1] font-heading font-black text-main text-3xl sm:text-4xl md:text-5xl">
            Let's build something <br /> 
            <span class="text-gradient underline decoration-brand/30 underline-offset-8">Extraordinary.</span>
          </h2>
          <p class="relative z-10 text-muted text-lg md:text-2xl mb-12 max-w-2xl mx-auto font-medium leading-relaxed">
            Available for freelance projects and technical collaborations. Ready to elevate your digital presence with world-class engineering?
          </p>
          <div class="relative z-10 flex flex-col sm:flex-row items-center justify-center gap-6">
            <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary py-5 px-12 text-sm shadow-2xl w-full sm:w-auto font-black uppercase tracking-wider">
              Start a Conversation
            </a>
            <a :href="globalData.socials.email" class="btn-secondary py-5 px-12 text-sm w-full sm:w-auto font-black uppercase tracking-wider">
              Email Me
            </a>
          </div>
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
