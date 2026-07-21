<template>
  <nav 
    class="fixed top-0 left-0 w-full z-50 transition-all duration-500"
    :class="[isScrolled ? 'py-3 bg-surface/85 backdrop-blur-xl border-b border-border' : 'py-6 md:py-8 bg-transparent']"
  >
    <div class="max-w-7xl mx-auto px-6 md:px-12 flex items-center justify-between">
      <!-- Logo -->
      <NuxtLink to="/" class="group flex items-center gap-4">
        <RdLogo size="sm" />
        <div class="flex flex-col">
          <span class="text-xl font-heading font-black tracking-tighter leading-none text-main">
            {{ siteNameParts[0] }} <span class="text-brand">{{ siteNameParts[1] }}</span>
          </span>
          <span class="text-[9px] text-muted font-black tracking-[0.2em] uppercase mt-1">
            {{ globalData.tagline }}
          </span>
        </div>
      </NuxtLink>
      
      <!-- Desktop Links -->
      <div class="hidden md:flex items-center bg-surface-card/40 border border-border px-2 py-1.5 rounded-2xl backdrop-blur-md">
        <NuxtLink 
          v-for="link in globalData.navigation" 
          :key="link.path"
          :to="link.path" 
          class="px-6 py-2 rounded-xl text-sm font-black transition-all duration-300 uppercase tracking-wider"
          :class="[route.path === link.path ? 'bg-brand text-white shadow-md shadow-brand/20' : 'text-muted hover:text-brand']"
        >
          {{ link.name }}
        </NuxtLink>
      </div>

      <div class="flex items-center gap-4">
        <!-- Theme Toggle -->
        <ThemeToggle />

        <!-- Hire Me CTA -->
        <a 
          :href="globalData.socials.whatsapp" 
          target="_blank"
          class="btn-primary hidden sm:flex items-center gap-2 py-2.5 px-6 text-xs font-black uppercase tracking-wider"
        >
          Hire Me
          <ArrowUpRightIcon class="w-4 h-4" />
        </a>
        
        <!-- Mobile Menu Toggle -->
        <button 
          @click="isMenuOpen = !isMenuOpen" 
          class="md:hidden w-11 h-11 flex items-center justify-center rounded-xl bg-surface-card/50 border border-border text-muted hover:text-brand transition-colors"
          aria-label="Toggle Menu"
        >
          <MenuIcon v-if="!isMenuOpen" class="w-6 h-6" />
          <XIcon v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]"
      enter-from-class="opacity-0 -translate-y-10 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 -translate-y-10 scale-95"
    >
      <div v-if="isMenuOpen" class="md:hidden fixed top-24 left-6 right-6 p-6 bg-surface/95 backdrop-blur-2xl rounded-[2.5rem] shadow-2xl border border-border">
        <div class="flex flex-col gap-3">
          <NuxtLink 
            v-for="link in globalData.navigation" 
            :key="link.path" 
            :to="link.path"
            @click="isMenuOpen = false"
            class="px-6 py-4 rounded-2xl text-lg font-black uppercase tracking-wider transition-all"
            :class="[route.path === link.path ? 'bg-brand/10 text-brand' : 'text-muted hover:bg-surface-card hover:text-main']"
          >
            {{ link.name }}
          </NuxtLink>
          <div class="h-px bg-border my-2"></div>
          <a 
            :href="globalData.socials.whatsapp" 
            target="_blank"
            class="btn-primary flex items-center justify-center gap-2 py-4 font-black uppercase tracking-wider"
          >
            Contact Me
          </a>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { MenuIcon, XIcon, ArrowUpRightIcon } from 'lucide-vue-next'
import globalData from '~/data/global.json'

const route = useRoute()
const isMenuOpen = ref(false)
const isScrolled = ref(false)

const siteNameParts = computed(() => {
  const name = globalData.siteName || 'RINGGA DEV'
  const parts = name.split(' ')
  return [parts[0] || 'RINGGA', parts.slice(1).join(' ') || 'DEV']
})

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
