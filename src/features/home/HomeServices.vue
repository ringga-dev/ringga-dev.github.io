<template>
  <section class="max-w-7xl mx-auto px-6 py-24 relative z-10">
    <SectionHeader
      number="02"
      badge="Expertise"
      description="High-performance digital work with technical precision and architectural clarity."
    >
      <template #title>
        Precision <span class="text-brand">Engineering</span>
      </template>
    </SectionHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mt-12">
      <div
        v-for="(service, index) in homeData.services"
        :key="service.title"
        :class="[
          'group relative p-8 md:p-10 bg-surface-card border-[1.5px] border-ink/80 rounded-sm flex flex-col shadow-riso hover:-translate-x-0.5 hover:-translate-y-0.5 transition-[transform,box-shadow] duration-150',
          index === 0 ? 'lg:col-span-2 lg:row-span-2' : 'lg:col-span-1'
        ]"
      >
        <div class="flex items-center justify-between mb-6">
          <div class="w-12 h-12 rounded-sm border-[1.5px] border-ink flex items-center justify-center text-brand shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)]">
            <component :is="getIcon(service.icon)" class="w-6 h-6" />
          </div>
          <span class="numeral-outline text-4xl md:text-5xl">
            0{{ index + 1 }}
          </span>
        </div>

        <h3 :class="['font-display font-bold text-main mb-3', index === 0 ? 'text-2xl lg:text-3xl' : 'text-xl']">
          {{ service.title }}
        </h3>

        <p class="text-muted font-serif leading-relaxed mb-6 text-base">
          {{ service.description }}
        </p>

        <ul class="space-y-2.5 mt-auto">
          <li
            v-for="feature in service.features"
            :key="feature"
            class="flex items-center gap-3 text-sm font-serif text-muted"
          >
            <span class="w-2.5 h-2.5 shrink-0 bg-brand rotate-45"></span>
            {{ feature }}
          </li>
        </ul>
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
