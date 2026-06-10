<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 min-h-screen relative overflow-hidden bg-surface text-main">
    <!-- Background bubble glows -->
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-brand/5 blur-[150px] pointer-events-none rounded-full"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-brand-light/5 blur-[150px] pointer-events-none rounded-full"></div>

    <div class="max-w-5xl mx-auto relative z-10" v-if="skill">
      <!-- Breadcrumb -->
      <NuxtLink to="/about" class="inline-flex items-center gap-2 text-sm font-black uppercase tracking-wider text-muted hover:text-brand transition-colors mb-10 group">
        <ArrowLeftIcon class="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
        Back to About Me
      </NuxtLink>

      <!-- Main Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Left Column: Header and Stats -->
        <div class="lg:col-span-5 space-y-8">
          <!-- Skill Header Glass Card -->
          <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border text-center">
            <div class="w-20 h-20 rounded-3xl bg-brand/5 border border-brand/20 text-brand flex items-center justify-center mx-auto mb-6">
              <component :is="getIcon(skill.icon)" class="w-10 h-10" />
            </div>
            
            <h1 class="text-3xl font-heading font-black text-main mb-2">
              {{ skill.name }}
            </h1>
            
            <div class="inline-block px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-[9px] font-black uppercase tracking-widest mt-2 mb-6">
              {{ skill.proficiency }} Tier
            </div>

            <!-- Animated Bar -->
            <div class="space-y-2 text-left">
              <div class="flex justify-between text-xs font-black uppercase tracking-wider text-muted">
                <span>Proficiency Level</span>
                <span class="text-brand">{{ skill.level }}%</span>
              </div>
              <div class="h-2 w-full bg-surface-elevated rounded-full overflow-hidden border border-border">
                <div 
                  class="h-full bg-gradient-to-r from-brand to-brand-light rounded-full transition-all duration-1000"
                  :style="{ width: `${skill.level}%` }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Quick Metrics Card -->
          <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-sm font-black uppercase tracking-widest text-muted mb-6 border-b border-border pb-3">Metrics</h3>
            <div class="grid grid-cols-2 gap-6">
              <div>
                <div class="text-[10px] font-black text-muted uppercase tracking-widest mb-1">Experience</div>
                <div class="text-xl font-heading font-black text-main">{{ skill.yearsOfUse }}</div>
              </div>
              <div>
                <div class="text-[10px] font-black text-muted uppercase tracking-widest mb-1">Projects Done</div>
                <div class="text-xl font-heading font-black text-main">{{ associatedProjects.length }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Detail Overview -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Toolkit Description -->
          <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-lg font-heading font-black text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Capability Overview</h3>
            <p class="text-muted leading-relaxed font-medium text-lg">
              {{ skill.longDescription }}
            </p>
          </div>

          <!-- Associated Projects list -->
          <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-lg font-heading font-black text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Projects Using This Skill</h3>
            
            <div class="space-y-4" v-if="associatedProjects.length > 0">
              <NuxtLink 
                v-for="project in associatedProjects" 
                :key="project.title"
                :to="`/projects/${project.slug}`"
                class="flex items-center gap-6 p-4 rounded-2xl bg-surface-elevated/40 border border-border hover:border-brand/30 hover:bg-surface-elevated/70 transition-all group"
              >
                <!-- Thumbnail -->
                <div class="w-16 h-12 rounded-xl overflow-hidden flex-shrink-0 border border-border bg-surface-elevated">
                  <img :src="project.image" :alt="project.title" class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500" />
                </div>
                <!-- Title & info -->
                <div class="flex-1 min-w-0">
                  <h4 class="font-heading font-black text-main group-hover:text-brand transition-colors text-base truncate">{{ project.title }}</h4>
                  <p class="text-xs text-muted truncate mt-0.5">{{ project.description }}</p>
                </div>
                <ArrowRightIcon class="w-5 h-5 text-muted group-hover:text-brand group-hover:translate-x-1 transition-all flex-shrink-0" />
              </NuxtLink>
            </div>
            
            <div class="text-center py-8 text-muted font-medium" v-else>
              <CpuIcon class="w-12 h-12 mx-auto mb-4 opacity-25 animate-pulse" />
              No public projects registered with this exact skill currently.
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Error Fallback -->
    <div class="max-w-xl mx-auto text-center py-20" v-else>
      <BoxIcon class="w-16 h-16 text-muted mx-auto mb-6 opacity-30 animate-bounce" />
      <h2 class="text-2xl font-black text-main mb-4">Skill Not Found</h2>
      <p class="text-muted mb-8 font-medium">The skill you are looking for does not exist in our registry.</p>
      <NuxtLink to="/about" class="btn-primary inline-flex py-4 px-10 text-xs font-black uppercase tracking-wider">
        Back to About Me
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ArrowLeftIcon, 
  ArrowRightIcon, 
  SmartphoneIcon, 
  ZapIcon, 
  LayersIcon, 
  CodeIcon, 
  DatabaseIcon, 
  CpuIcon,
  BoxIcon
} from 'lucide-vue-next'
import aboutData from '~/data/about.json'
import projectsData from '~/data/projects.json'

const route = useRoute()

const skill = computed(() => {
  const slug = route.params.slug
  return aboutData.skills.find(s => s.slug === slug)
})

const getIcon = (name) => {
  switch (name) {
    case 'SmartphoneIcon': return SmartphoneIcon
    case 'ZapIcon': return ZapIcon
    case 'LayersIcon': return LayersIcon
    case 'CodeIcon': return CodeIcon
    case 'DatabaseIcon': return DatabaseIcon
    case 'CpuIcon': return CpuIcon
    default: return CodeIcon
  }
}

// Dynamically associate projects using tags mapping
const associatedProjects = computed(() => {
  if (!skill.value) return []
  const skillName = skill.value.name.toLowerCase()
  return projectsData.projects.filter(p => {
    return p.tags.some(tag => {
      const tagLower = tag.toLowerCase()
      return skillName.includes(tagLower) || tagLower.includes(skillName)
    }) || p.category.toLowerCase().includes(skillName)
  })
})

useHead({
  title: skill.value ? `${skill.value.name} | Toolkit Details` : 'Skill Details',
  meta: [
    { name: 'description', content: skill.value ? skill.value.longDescription : 'Toolkit capability details' }
  ]
})
</script>
