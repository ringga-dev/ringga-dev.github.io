<template>
  <nav class="fixed top-6 left-1/2 -translate-x-1/2 z-50 w-[90%] max-w-4xl">
    <div class="glass px-6 py-3 rounded-2xl flex items-center justify-between">
      <NuxtLink to="/" class="text-xl font-bold tracking-tighter">
        RINGGA<span class="text-purple-500">DEV</span>
      </NuxtLink>
      
      <div class="hidden md:flex items-center gap-8 text-sm font-medium text-white/70">
        <NuxtLink to="/" class="hover:text-white transition-colors" active-class="text-white">Home</NuxtLink>
        <NuxtLink to="/projects" class="hover:text-white transition-colors" active-class="text-white">Projects</NuxtLink>
        <NuxtLink to="/about" class="hover:text-white transition-colors" active-class="text-white">About</NuxtLink>
      </div>

      <a href="mailto:contact@ringga.dev" class="btn-primary text-xs uppercase tracking-widest font-bold">
        Hire Me
      </a>
    </div>
  </nav>
</template>

<script setup>
import { useWindowScroll } from '@vueuse/core'
const { y } = useWindowScroll()
</script>
