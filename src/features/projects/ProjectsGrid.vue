<template>
  <div class="max-w-7xl mx-auto relative z-10">
    <SectionHeader 
      badge="Portfolio" 
      description="A comprehensive showcase of my open-source contributions and professional developments across mobile and web platforms."
      centered
    >
      <template #title>
        Selected <span class="text-brand">Projects</span>
      </template>
    </SectionHeader>

    <!-- Filters -->
    <div class="flex flex-wrap justify-center gap-3 sm:gap-4 mb-16">
      <button
        v-for="cat in categories"
        :key="cat"
        @click="activeCategory = cat"
        class="px-6 py-2.5 rounded-sm text-xs font-mono font-bold uppercase tracking-widest border-[1.5px] transition-[transform,box-shadow,background-color,border-color,color] duration-150"
        :class="activeCategory === cat ? 'bg-ink text-paper border-ink shadow-riso' : 'bg-surface-card text-muted border-ink/60 hover:border-brand hover:text-brand hover:shadow-riso'"
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
        :style="{ transitionDelay: `${(index % 3 + 1) * 100}ms` }"
      />
    </div>

    <!-- Bottom CTA -->
    <div class="mt-32 text-center">
      <div class="riso-card p-10 sm:p-12 inline-block max-w-2xl">
        <h3 class="mb-6 font-display font-bold text-main text-2xl">Interested in Collaboration?</h3>
        <p class="text-muted mb-8 font-serif">Always open to new projects, creative ideas, or opportunities to be part of your vision.</p>
        <a :href="globalData.socials.whatsapp" target="_blank" class="btn-primary py-4 px-10 text-xs font-mono font-bold uppercase tracking-wider">
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
