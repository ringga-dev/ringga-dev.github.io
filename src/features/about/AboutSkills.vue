<template>
  <div class="mb-40 bg-surface">
    <SectionHeader
      badge="Expertise"
      description="A specialized toolkit refined through years of professional development and complex problem-solving."
      centered
    >
      <template #title>Technical <span class="text-brand">Toolkit</span></template>
    </SectionHeader>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-20">
      <NuxtLink
        v-for="(skill, index) in skillsData"
        :key="skill.name"
        :to="`/skills/${skill.slug}`"
        :ref="(el) => { if (el) skillRefs[skill.name] = el }"
        :class="[
          'group p-6 bg-surface-card block',
          index % 2 === 1 ? 'riso-card-2' : 'riso-card'
        ]"
      >
        <div class="flex items-center gap-4 mb-4">
          <div class="w-10 h-10 rounded-sm border-[1.5px] border-ink flex items-center justify-center text-brand shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] group-hover:bg-brand group-hover:text-paper transition-[transform,box-shadow,color,background-color] duration-150">
            <component :is="getIcon(skill.icon)" class="w-5 h-5" />
          </div>
          <div class="flex-1">
            <div class="flex justify-between items-end mb-1 gap-2">
              <span class="font-display font-bold text-sm text-main leading-tight">{{ skill.name }}</span>
              <span class="font-mono text-xs font-semibold text-brand whitespace-nowrap">{{ skill.level }}%</span>
            </div>
            <div class="h-2 w-full bg-surface-elevated rounded-sm overflow-hidden border-[1.5px] border-ink/70">
              <div
                class="h-full bg-brand rounded-sm transition-[width] duration-700 ease-out origin-left"
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
