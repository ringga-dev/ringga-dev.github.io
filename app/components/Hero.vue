<template>
  <section class="min-h-screen flex flex-col items-center justify-center pt-20 px-6 text-center">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold mb-6 animate-fade-in">
      <span class="relative flex h-2 w-2">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
      </span>
      AVAILABLE FOR PROJECTS
    </div>
    
    <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-6 leading-tight">
      Ringga Septia <br />
      <span class="text-gradient">Pribadi</span>
    </h1>
    
    <p class="text-white/60 max-w-2xl text-lg mb-10 leading-relaxed">
      I'm an Android & Web Developer with 3 years of experience in building high-performance applications and premium digital experiences.
    </p>
    
    <div class="flex flex-col sm:flex-row gap-4">
      <NuxtLink to="/projects" class="btn-primary flex items-center gap-2">
        View My Work
        <ArrowRightIcon class="w-4 h-4" />
      </NuxtLink>
      <NuxtLink to="/about" class="px-6 py-2 rounded-full border border-white/10 hover:bg-white/5 transition-colors">
        About Me
      </NuxtLink>
    </div>

    <!-- Decorative Elements -->
    <div class="mt-20 flex gap-12 text-white/30 items-center justify-center flex-wrap">
      <div class="flex items-center gap-2">
        <Code2Icon class="w-5 h-5" />
        <span class="text-sm font-medium">Clean Code</span>
      </div>
      <div class="flex items-center gap-2">
        <LayoutIcon class="w-5 h-5" />
        <span class="text-sm font-medium">UI/UX Focus</span>
      </div>
      <div class="flex items-center gap-2">
        <ZapIcon class="w-5 h-5" />
        <span class="text-sm font-medium">Fast Performance</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ArrowRightIcon, Code2Icon, LayoutIcon, ZapIcon } from 'lucide-vue-next'
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 1s ease-out forwards;
}
</style>
