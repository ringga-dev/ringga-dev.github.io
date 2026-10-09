<template>
  <div class="riso-card-2 p-10 bg-surface-card relative overflow-hidden h-full">
    <h3 class="text-2xl font-display font-bold text-main mb-4">
      {{ contactData.info.title }}
    </h3>
    <p class="text-muted font-serif mb-10 leading-relaxed">
      {{ contactData.info.description }}
    </p>

    <div class="space-y-8">
      <a
        v-for="item in contactData.info.items"
        :key="item.label"
        :href="item.url"
        :target="item.url !== '#' ? '_blank' : undefined"
        class="flex items-center gap-6 group hover:-translate-x-1 transition-[transform] duration-150"
        :class="{ 'pointer-events-none': item.url === '#' }"
      >
        <div class="w-14 h-14 rounded-sm border-[1.5px] border-ink text-brand flex items-center justify-center shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] group-hover:bg-brand group-hover:text-paper group-hover:shadow-[3px_3px_0_hsl(var(--brand-color)/0.8)] transition-[transform,box-shadow,color,background-color] duration-150">
          <component :is="getIcon(item.icon)" class="w-6 h-6" />
        </div>
        <div>
          <div class="font-mono text-[10px] font-semibold uppercase text-muted tracking-[0.2em] mb-1">{{ item.label }}</div>
          <div class="text-base font-display font-bold text-main group-hover:text-brand transition-colors duration-150">{{ item.value }}</div>
        </div>
      </a>
    </div>
  </div>
</template>

<script setup>
import { MailIcon, MessageSquareIcon, MapPinIcon } from 'lucide-vue-next'
import contactData from '~/data/contact.json'

const getIcon = (name) => {
  switch (name) {
    case 'MailIcon': return MailIcon
    case 'MessageSquareIcon': return MessageSquareIcon
    case 'MapPinIcon': return MapPinIcon
    default: return MailIcon
  }
}
</script>
