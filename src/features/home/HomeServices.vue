<template>
  <section class="max-w-7xl mx-auto px-6 py-28 relative z-10">
    <SectionHeader 
      badge="Strategic Expertise" 
      description="Crafting high-performance digital ecosystems with technical precision and architectural excellence."
      centered
    >
      <template #title>
        Precision <span class="text-gradient">Engineering</span>
      </template>
    </SectionHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-16 auto-rows-fr">
      <div 
        v-for="(service, index) in homeData.services" 
        :key="service.title"
        :class="[
          'group relative p-8 md:p-10 rounded-[2rem] overflow-hidden bg-surface-card border border-border hover:border-brand/40 transition-all duration-500 scroll-reveal flex flex-col hover:-translate-y-1.5',
          index === 0 ? 'lg:col-span-2 lg:row-span-2' : 'lg:col-span-1'
        ]"
      >
        <div class="absolute -right-16 -top-16 w-52 h-52 rounded-full bg-brand/5 blur-3xl group-hover:bg-brand/15 transition-all duration-700 pointer-events-none"></div>
        
        <div class="relative z-10 flex flex-col h-full">
          <div class="flex items-center justify-between mb-8">
            <div class="w-14 h-14 rounded-2xl bg-surface-elevated/60 flex items-center justify-center text-brand border border-border group-hover:scale-110 group-hover:-rotate-3 transition-all duration-500">
              <component :is="getIcon(service.icon)" class="w-7 h-7" />
            </div>
            <span class="font-heading font-black text-5xl text-border/50 group-hover:text-brand/20 transition-colors duration-500">
              0{{ index + 1 }}
            </span>
          </div>
          
          <h3 :class="['font-black text-main mb-4 group-hover:text-brand transition-colors', index === 0 ? 'text-3xl lg:text-4xl' : 'text-2xl']">
            {{ service.title }}
          </h3>
          
          <p class="text-muted font-medium leading-relaxed mb-8 text-base">
            {{ service.description }}
          </p>
          
          <ul class="space-y-3 mt-auto">
            <li 
              v-for="feature in service.features" 
              :key="feature" 
              class="flex items-center gap-3 text-sm font-bold text-muted group-hover:text-main transition-colors duration-300"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-brand shadow-[0_0_10px] shadow-brand/50"></span>
              {{ feature }}
            </li>
          </ul>
        </div>
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
