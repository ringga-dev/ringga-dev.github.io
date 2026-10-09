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
    <section class="max-w-7xl mx-auto px-6 py-24 relative z-10">
      <SectionHeader
        badge="Selected Work"
        description="A curated selection of recent engineering work."
      >
        <template #title>
          Featured <span class="text-brand">Projects</span>
        </template>
      </SectionHeader>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ProjectCard
          v-for="project in featuredProjects"
          :key="project.title"
          v-bind="project"
        />
      </div>

      <div class="mt-10 text-center">
        <NuxtLink to="/projects" class="btn-secondary inline-flex items-center gap-3 py-3.5 px-8 font-mono text-xs uppercase tracking-[0.15em]">
          View All Projects
          <ArrowRightIcon class="w-4 h-4" />
        </NuxtLink>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="relative z-10">
      <div class="max-w-5xl mx-auto px-6 pb-24">
        <div class="border border-border bg-surface px-8 py-14 md:px-16 md:py-20 text-center">
          <h2 class="mb-5 leading-[1.1] font-display font-semibold text-main text-3xl sm:text-4xl md:text-5xl">
            Let's build something <br />
            <span class="text-brand">solid.</span>
          </h2>
          <p class="text-muted text-lg md:text-xl mb-10 max-w-2xl mx-auto font-serif leading-relaxed">
            Available for freelance work and technical collaboration.
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a :href="globalData.socials.whatsapp" target="_blank" rel="noopener" class="btn-primary py-3.5 px-8 font-mono text-xs uppercase tracking-[0.15em] w-full sm:w-auto">
              Start a Conversation
            </a>
            <a :href="globalData.socials.email" class="btn-secondary py-3.5 px-8 font-mono text-xs uppercase tracking-[0.15em] w-full sm:w-auto">
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
