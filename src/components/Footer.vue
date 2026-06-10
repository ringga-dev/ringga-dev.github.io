<template>
  <footer class="pt-32 pb-12 border-t border-border px-6 relative overflow-hidden bg-surface">
    <!-- Bottom glow -->
    <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-brand/5 blur-[120px] pointer-events-none rounded-full"></div>

    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-16 relative z-10">
      <div class="lg:col-span-2 scroll-reveal">
        <NuxtLink to="/" class="group flex items-center gap-4 mb-8">
          <RdLogo size="md" />
          <span class="text-3xl font-heading font-black tracking-tighter text-main">
            {{ siteNameParts[0] }} <span class="text-brand">{{ siteNameParts[1] }}</span>
          </span>
        </NuxtLink>
        <p class="text-muted text-lg max-w-sm leading-relaxed font-medium">
          Delivering premium digital solutions across Android and Web platforms. Focused on high-performance architecture and modern design.
        </p>
        
        <div class="flex gap-4 mt-10">
          <a 
            v-for="social in socialList" 
            :key="social.name" 
            :href="social.url" 
            target="_blank" 
            class="w-12 h-12 rounded-2xl bg-surface-card border border-border flex items-center justify-center text-muted hover:text-brand hover:border-brand/30 hover:-translate-y-1 transition-all duration-300"
            :aria-label="social.name"
          >
            <component :is="social.icon" class="w-5 h-5" />
          </a>
        </div>
      </div>
      
      <div class="flex flex-col gap-6 scroll-reveal" style="transition-delay: 200ms">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-brand">Quick Links</span>
        <NuxtLink 
          v-for="link in globalData.navigation" 
          :key="link.path" 
          :to="link.path" 
          class="nav-link text-lg"
        >
          {{ link.name }}
        </NuxtLink>
      </div>

      <div class="flex flex-col gap-6 scroll-reveal" style="transition-delay: 400ms">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-brand">Contact Info</span>
        <a :href="globalData.socials.email" class="nav-link text-lg flex items-center gap-3">
          <MailIcon class="w-5 h-5" />
          Email Me
        </a>
        <a :href="globalData.socials.whatsapp" target="_blank" class="nav-link text-lg flex items-center gap-3">
          <MessageSquareIcon class="w-5 h-5" />
          WhatsApp
        </a>
        <div class="text-muted text-sm mt-4 font-medium flex items-center gap-3">
          <MapPinIcon class="w-5 h-5" />
          Pekanbaru, Indonesia
        </div>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto mt-24 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-6 text-muted text-[10px] font-black uppercase tracking-[0.3em]">
      <div>© {{ new Date().getFullYear() }} {{ globalData.siteName }}. ALL RIGHTS RESERVED.</div>
      <div class="flex gap-8 items-center">
        <span class="text-brand">Static Site Hosting</span>
        <div class="w-1 h-1 rounded-full bg-border"></div>
        <span>Tailwind CSS v3</span>
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
