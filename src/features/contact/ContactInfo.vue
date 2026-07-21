<template>
  <div class="glass-card p-10 rounded-[2.5rem] bg-surface-card border border-border scroll-reveal relative overflow-hidden h-full">
    <div class="absolute -right-10 -bottom-10 w-40 h-40 bg-brand/5 rounded-full blur-3xl pointer-events-none"></div>

    <h3 class="text-2xl font-heading font-black text-main mb-4">
      {{ contactData.info.title }}
    </h3>
    <p class="text-muted font-medium mb-10 leading-relaxed">
      {{ contactData.info.description }}
    </p>

    <div class="space-y-8">
      <a 
        v-for="item in contactData.info.items" 
        :key="item.label"
        :href="item.url" 
        :target="item.url !== '#' ? '_blank' : undefined"
        class="flex items-center gap-6 group hover:-translate-x-1 transition-transform duration-300"
        :class="{ 'pointer-events-none': item.url === '#' }"
      >
        <div class="w-14 h-14 rounded-2xl bg-brand/5 border border-brand/10 text-brand flex items-center justify-center group-hover:bg-brand group-hover:text-brand-dark transition-all duration-300">
          <component :is="getIcon(item.icon)" class="w-6 h-6" />
        </div>
        <div>
          <div class="text-[9px] font-black uppercase text-muted tracking-widest mb-1">{{ item.label }}</div>
          <div class="text-base font-black text-main group-hover:text-brand transition-colors">{{ item.value }}</div>
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
