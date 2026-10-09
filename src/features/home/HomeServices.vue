<template>
  <section class="max-w-7xl mx-auto px-6 py-24 relative z-10">
    <SectionHeader
      badge="Expertise"
      description="High-performance digital work with technical precision and architectural clarity."
    >
      <template #title>
        Precision <span class="text-brand">Engineering</span>
      </template>
    </SectionHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-px bg-border mt-12 border border-border">
      <div
        v-for="(service, index) in homeData.services"
        :key="service.title"
        :class="[
          'group relative p-8 md:p-10 bg-surface flex flex-col',
          index === 0 ? 'lg:col-span-2 lg:row-span-2' : 'lg:col-span-1'
        ]"
      >
        <div class="flex items-center justify-between mb-6">
          <div class="w-12 h-12 rounded border border-border flex items-center justify-center text-brand">
            <component :is="getIcon(service.icon)" class="w-6 h-6" />
          </div>
          <span class="font-mono text-4xl text-border">
            0{{ index + 1 }}
          </span>
        </div>

        <h3 :class="['font-display font-semibold text-main mb-3', index === 0 ? 'text-2xl lg:text-3xl' : 'text-xl']">
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
            <span class="w-1 h-1 rounded-full bg-brand shrink-0"></span>
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
