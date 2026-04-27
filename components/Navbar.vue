<template>
  <nav 
    class="fixed top-0 left-0 w-full z-50 transition-all duration-500"
    :class="[isScrolled ? 'py-3 bg-surface/80 backdrop-blur-lg border-b border-white/5' : 'py-6 md:py-8 bg-transparent']"
  >
    <div class="max-w-7xl mx-auto px-6 md:px-12 flex items-center justify-between">
      <!-- Logo -->
      <NuxtLink to="/" class="group flex items-center gap-4">
        <RdLogo size="sm" />
        <div class="flex flex-col">
          <span class="text-xl font-heading font-black tracking-tighter leading-none">
            RINGGA <span class="text-brand">DEV</span>
          </span>
          <span class="text-[10px] text-slate-500 font-bold tracking-[0.2em] uppercase mt-1">Fullstack Engineer</span>
        </div>
      </NuxtLink>
      
      <!-- Desktop Links -->
      <div class="hidden md:flex items-center bg-slate-900/50 border border-slate-800/50 px-2 py-1.5 rounded-2xl backdrop-blur-md">
        <NuxtLink 
          v-for="link in links" 
          :key="link.path"
          :to="link.path" 
          class="px-6 py-2 rounded-xl text-sm font-bold transition-all duration-300 hover:text-brand"
          :class="[route.path === link.path ? 'bg-brand text-surface' : 'text-slate-400']"
        >
          {{ link.name }}
        </NuxtLink>
      </div>

      <div class="flex items-center gap-4">
        <a 
          href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" 
          target="_blank"
          class="btn-primary hidden sm:flex items-center gap-2 py-2.5 px-6 text-sm"
        >
          Hire Me
          <ArrowUpRightIcon class="w-4 h-4" />
        </a>
        
        <!-- Mobile Menu Toggle -->
        <button 
          @click="isMenuOpen = !isMenuOpen" 
          class="md:hidden w-11 h-11 flex items-center justify-center rounded-xl bg-slate-900/50 border border-slate-800 text-slate-400 hover:text-brand transition-colors"
          aria-label="Toggle Menu"
        >
          <MenuIcon v-if="!isMenuOpen" class="w-6 h-6" />
          <XIcon v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu Overlay -->
    <Transition
      enter-active-class="transition duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
      enter-from-class="opacity-0 -translate-y-10"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-10"
    >
      <div v-if="isMenuOpen" class="md:hidden fixed top-20 left-6 right-6 p-6 glass rounded-[2rem] shadow-2xl border-brand/10">
        <div class="flex flex-col gap-3">
          <NuxtLink 
            v-for="link in links" 
            :key="link.path" 
            :to="link.path"
            @click="isMenuOpen = false"
            class="px-6 py-4 rounded-2xl text-lg font-bold transition-all"
            :class="[route.path === link.path ? 'bg-brand/10 text-brand' : 'text-slate-400 hover:bg-white/5 hover:text-white']"
          >
            {{ link.name }}
          </NuxtLink>
          <div class="h-px bg-slate-800 my-2"></div>
          <a 
            href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" 
            class="btn-primary flex items-center justify-center gap-2 py-4"
          >
            Contact Me
          </a>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { MenuIcon, XIcon, ArrowUpRightIcon } from 'lucide-vue-next'

const route = useRoute()
const isMenuOpen = ref(false)
const isScrolled = ref(false)

const links = [
  { name: 'Home', path: '/' },
  { name: 'Projects', path: '/projects' },
  { name: 'About', path: '/about' }
]

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

