<template>
  <section class="max-w-7xl mx-auto px-6 py-32 relative z-10 bg-surface">
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
      <div 
        v-for="service in homeData.services" 
        :key="service.title"
        class="glass-card p-8 rounded-[2.5rem] group hover:-translate-y-2 transition-all duration-500 scroll-reveal border border-border hover:border-brand/20 relative overflow-hidden bg-surface-card"
      >
        <div class="absolute -right-8 -bottom-8 w-32 h-32 bg-brand/5 rounded-full blur-3xl group-hover:bg-brand/10 transition-colors"></div>
        
        <div class="w-16 h-16 rounded-2xl bg-brand/5 flex items-center justify-center text-brand mb-8 group-hover:bg-brand group-hover:text-slate-950 transition-all duration-500 border border-brand/10">
          <component :is="getIcon(service.icon)" class="w-8 h-8" />
        </div>
        
        <h3 class="text-2xl font-black mb-4 text-main group-hover:text-brand transition-colors">
          {{ service.title }}
        </h3>
        
        <p class="text-muted font-medium leading-relaxed mb-8">
          {{ service.description }}
        </p>
        
        <ul class="space-y-3 mb-8">
          <li 
            v-for="feature in service.features" 
            :key="feature" 
            class="flex items-center gap-3 text-sm font-bold text-muted group-hover:text-main transition-colors duration-300"
          >
            <div class="w-1.5 h-1.5 rounded-full bg-brand"></div>
            {{ feature }}
          </li>
        </ul>

        <div class="h-1 w-0 bg-brand group-hover:w-full transition-all duration-700 absolute bottom-0 left-0"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { SmartphoneIcon, CpuIcon, LayersIcon } from 'lucide-vue-next'
import homeData from '~/data/home.json'

const getIcon = (name) => {
  switch (name) {
    case 'SmartphoneIcon': return SmartphoneIcon
    case 'CpuIcon': return CpuIcon
    case 'LayersIcon': return LayersIcon
    default: return SmartphoneIcon
  }
}
</script>
