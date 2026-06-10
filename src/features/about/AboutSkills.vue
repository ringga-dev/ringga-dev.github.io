<template>
  <div class="mb-40 bg-surface">
    <SectionHeader 
      badge="Expertise" 
      description="A specialized toolkit refined through years of professional development and complex problem-solving."
      centered
    >
      <template #title>Technical <span class="text-gradient">Toolkit</span></template>
    </SectionHeader>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-20">
      <NuxtLink 
        v-for="skill in skillsData" 
        :key="skill.name"
        :to="`/skills/${skill.slug}`"
        :ref="(el) => { if (el) skillRefs[skill.name] = el }"
        class="glass-card p-6 rounded-3xl scroll-reveal group bg-surface-card border border-border block hover:-translate-y-1 transition-all duration-300"
      >
        <div class="flex items-center gap-4 mb-4">
          <div class="w-10 h-10 rounded-xl bg-brand/5 flex items-center justify-center text-brand group-hover:bg-brand group-hover:text-slate-950 transition-all duration-500 border border-brand/10">
            <component :is="getIcon(skill.icon)" class="w-5 h-5" />
          </div>
          <div class="flex-1">
            <div class="flex justify-between items-end mb-1">
              <span class="text-xs font-black text-main uppercase tracking-widest">{{ skill.name }}</span>
              <span class="text-xs font-black text-brand">{{ skill.level }}%</span>
            </div>
            <div class="h-1.5 w-full bg-surface-elevated rounded-full overflow-hidden border border-border">
              <div 
                class="h-full bg-gradient-to-r from-brand to-brand-light rounded-full transition-all duration-1000 ease-out origin-left"
                :style="{ width: visibleSkills[skill.name] ? `${skill.level}%` : '0%' }"
              ></div>
            </div>
          </div>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  SmartphoneIcon, 
  ZapIcon, 
  LayersIcon, 
  CodeIcon, 
  DatabaseIcon, 
  CpuIcon 
} from 'lucide-vue-next'
import aboutData from '~/data/about.json'

const skillsData = aboutData.skills
const visibleSkills = ref({})
const skillRefs = {}

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

onMounted(() => {
  skillsData.forEach(skill => {
    visibleSkills.value[skill.name] = false
    const element = skillRefs[skill.name]
    if (element) {
      const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          setTimeout(() => {
            visibleSkills.value[skill.name] = true
          }, 200)
          observer.disconnect()
        }
      }, { threshold: 0.1 })
      observer.observe(element instanceof HTMLElement ? element : element.$el)
    }
  })
})
</script>
