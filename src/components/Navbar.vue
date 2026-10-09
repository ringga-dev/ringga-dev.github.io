<template>
  <nav
    class="fixed top-0 left-0 w-full z-50 transition-colors duration-300 border-b"
    :class="[isScrolled ? 'py-3 bg-paper/90 border-border' : 'py-5 md:py-6 bg-transparent border-transparent']"
  >
    <div class="max-w-7xl mx-auto px-6 md:px-12 flex items-center justify-between">
      <!-- Logo / wordmark -->
      <NuxtLink to="/" class="group flex items-center gap-3">
        <RdLogo size="sm" />
        <div class="flex flex-col">
          <span class="text-lg font-display font-semibold tracking-tight leading-none text-main">
            {{ siteNameParts[0] }} <span class="text-brand">{{ siteNameParts[1] }}</span>
          </span>
          <span class="text-[10px] text-muted font-mono tracking-[0.2em] uppercase mt-1">
            {{ globalData.tagline }}
          </span>
        </div>
      </NuxtLink>

      <!-- Desktop links: mono nav, hairline underline on active -->
      <div class="hidden md:flex items-center gap-1">
        <NuxtLink
          v-for="link in globalData.navigation"
          :key="link.path"
          :to="link.path"
          class="px-3 py-2 font-mono text-xs uppercase tracking-[0.15em] transition-colors duration-200"
          :class="[route.path === link.path ? 'text-brand' : 'text-muted hover:text-main']"
        >
          {{ link.name }}
        </NuxtLink>
      </div>

      <div class="flex items-center gap-3">
        <!-- Theme Toggle -->
        <ThemeToggle />

        <!-- Contact CTA -->
        <a
          :href="globalData.socials.whatsapp"
          target="_blank"
          rel="noopener"
          class="btn-primary hidden sm:inline-flex items-center gap-2 py-2 px-5 font-mono text-xs uppercase tracking-[0.15em]"
        >
          Contact
        </a>

        <!-- Mobile Menu Toggle -->
        <button
          @click="isMenuOpen = !isMenuOpen"
          class="md:hidden w-10 h-10 flex items-center justify-center rounded border border-border text-main hover:border-brand transition-colors"
          :aria-label="isMenuOpen ? 'Close menu' : 'Open menu'"
          :aria-expanded="isMenuOpen"
        >
          <MenuIcon v-if="!isMenuOpen" class="w-5 h-5" />
          <XIcon v-else class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div v-if="isMenuOpen" class="md:hidden fixed top-20 left-6 right-6 p-6 bg-surface border border-border rounded">
        <div class="flex flex-col gap-1">
          <NuxtLink
            v-for="link in globalData.navigation"
            :key="link.path"
            :to="link.path"
            @click="isMenuOpen = false"
            class="px-4 py-3 font-mono text-sm uppercase tracking-[0.15em] transition-colors"
            :class="[route.path === link.path ? 'text-brand' : 'text-muted hover:text-main']"
          >
            {{ link.name }}
          </NuxtLink>
          <div class="h-px bg-border my-2"></div>
          <a
            :href="globalData.socials.whatsapp"
            target="_blank"
            rel="noopener"
            @click="isMenuOpen = false"
            class="btn-primary flex items-center justify-center gap-2 py-3 font-mono text-xs uppercase tracking-[0.15em]"
          >
            Contact
          </a>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { MenuIcon, XIcon } from 'lucide-vue-next'
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
