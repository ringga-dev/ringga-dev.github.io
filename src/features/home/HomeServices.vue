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

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8 mt-20 auto-rows-fr">
      <div 
        v-for="(service, index) in homeData.services" 
        :key="service.title"
        :class="[
          'glass-card p-8 md:p-10 rounded-[2.5rem] group hover:-translate-y-2 transition-all duration-500 scroll-reveal border border-border hover:border-brand/30 relative overflow-hidden bg-surface-card flex flex-col',
          index === 0 ? 'lg:col-span-2 lg:row-span-2' : 'lg:col-span-1 lg:row-span-1'
        ]"
      >
        <div class="absolute -right-12 -bottom-12 w-48 h-48 bg-brand/5 rounded-full blur-[60px] group-hover:bg-brand/15 transition-all duration-700"></div>
        <div class="absolute -left-12 -top-12 w-40 h-40 bg-brand-light/5 rounded-full blur-[50px] group-hover:bg-brand-light/10 transition-all duration-700"></div>
        
        <div class="relative z-10">
          <div class="w-16 h-16 rounded-2xl bg-surface-elevated/50 backdrop-blur-md flex items-center justify-center text-muted mb-8 group-hover:bg-brand group-hover:text-slate-950 transition-all duration-500 border border-border shadow-sm group-hover:shadow-brand/20 group-hover:scale-110 group-hover:-rotate-3">
            <component :is="getIcon(service.icon)" class="w-8 h-8" />
          </div>
          
          <h3 :class="['font-black mb-4 text-main group-hover:text-brand transition-colors', index === 0 ? 'text-3xl lg:text-4xl' : 'text-2xl']">
            {{ service.title }}
          </h3>
          
          <p class="text-muted font-medium leading-relaxed mb-8 text-base">
            {{ service.description }}
          </p>
          
          <ul class="space-y-4 mb-8 mt-auto">
            <li 
              v-for="feature in service.features" 
              :key="feature" 
              class="flex items-center gap-4 text-sm font-bold text-muted group-hover:text-main transition-colors duration-300"
            >
              <div class="w-2 h-2 rounded-full bg-border group-hover:bg-brand transition-colors duration-500 shadow-[0_0_10px_transparent] group-hover:shadow-brand/50"></div>
              {{ feature }}
            </li>
          </ul>
        </div>

        <div class="h-1.5 w-0 bg-gradient-to-r from-brand to-brand-light group-hover:w-full transition-all duration-700 absolute bottom-0 left-0 ease-out"></div>
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
