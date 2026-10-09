<template>
  <footer class="pt-20 pb-10 border-t border-border px-6 bg-surface">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
      <div class="lg:col-span-2">
        <NuxtLink to="/" class="flex items-center gap-3 mb-6">
          <RdLogo size="md" />
          <span class="text-2xl font-display font-semibold tracking-tight text-main">
            {{ siteNameParts[0] }} <span class="text-brand">{{ siteNameParts[1] }}</span>
          </span>
        </NuxtLink>
        <p class="text-muted text-base max-w-sm leading-relaxed font-serif">
          Digital work across Android and Web. High-performance architecture and clear, modern design.
        </p>

        <div class="flex gap-3 mt-8">
          <a
            v-for="social in socialList"
            :key="social.name"
            :href="social.url"
            target="_blank"
            rel="noopener"
            class="w-10 h-10 rounded border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand transition-colors"
            :aria-label="social.name"
          >
            <component :is="social.icon" class="w-4 h-4" />
          </a>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">Links</span>
        <NuxtLink
          v-for="link in globalData.navigation"
          :key="link.path"
          :to="link.path"
          class="nav-link text-base font-serif"
        >
          {{ link.name }}
        </NuxtLink>
      </div>

      <div class="flex flex-col gap-4">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">Contact</span>
        <a :href="globalData.socials.email" class="nav-link text-base font-serif flex items-center gap-3">
          <MailIcon class="w-4 h-4" />
          Email
        </a>
        <a :href="globalData.socials.whatsapp" target="_blank" rel="noopener" class="nav-link text-base font-serif flex items-center gap-3">
          <MessageSquareIcon class="w-4 h-4" />
          WhatsApp
        </a>
        <div class="text-muted text-sm font-serif flex items-center gap-3">
          <MapPinIcon class="w-4 h-4" />
          Pekanbaru, Indonesia
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto mt-16 pt-6 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4 font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
      <div>© {{ new Date().getFullYear() }} {{ globalData.siteName }}</div>
      <div class="flex gap-6 items-center">
        <span>Static Site</span>
        <span>Tailwind CSS</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import {
  GithubIcon,
  LinkedinIcon,
  MailIcon,
  MessageSquareIcon,
  MapPinIcon
} from 'lucide-vue-next'
import globalData from '~/data/global.json'

const siteNameParts = computed(() => {
  const name = globalData.siteName || 'RINGGA DEV'
  const parts = name.split(' ')
  return [parts[0] || 'RINGGA', parts.slice(1).join(' ') || 'DEV']
})

const socialList = computed(() => {
  return [
    { name: 'GitHub', icon: GithubIcon, url: globalData.socials.github },
    { name: 'LinkedIn', icon: LinkedinIcon, url: globalData.socials.linkedin },
    { name: 'WhatsApp', icon: MessageSquareIcon, url: globalData.socials.whatsapp },
    { name: 'Email', icon: MailIcon, url: globalData.socials.email }
  ]
})
</script>
