<template>
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
        class="px-8 py-2.5 rounded-xl text-xs font-black transition-all duration-300 border uppercase tracking-widest"
        :class="[activeCategory === cat ? 'bg-brand border-brand text-brand-dark shadow-lg shadow-brand/20' : 'bg-surface-card border-border text-muted hover:border-brand/40 hover:text-brand']"
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
      <div class="glass-card p-12 rounded-[3rem] border border-border inline-block max-w-2xl bg-surface-card relative overflow-hidden">
        <div class="absolute -top-10 -right-10 w-24 h-24 bg-brand/5 rounded-full blur-2xl"></div>
        <h3 class="mb-6 font-heading font-black text-main text-2xl">Interested in Collaboration?</h3>
        <p class="text-muted mb-8 font-medium">I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.</p>
        <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary py-4 px-10 text-xs font-black uppercase tracking-wider">
          Get Started Now
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import projectsData from '~/data/projects.json'
import globalData from '~/data/global.json'

const activeCategory = ref('All')
const categories = projectsData.categories || ['All', 'Android', 'Library', 'Backend']
const projects = projectsData.projects || []

const filteredProjects = computed(() => {
  if (activeCategory.value === 'All') return projects
  return projects.filter(p => {
    const categoryLower = p.category.toLowerCase()
    const activeLower = activeCategory.value.toLowerCase()
    return categoryLower.includes(activeLower) || activeLower.includes(categoryLower)
  })
})
</script>
