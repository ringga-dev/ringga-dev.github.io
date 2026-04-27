<template>
  <section class="min-h-screen flex flex-col items-center justify-center pt-32 pb-20 px-6 text-center relative overflow-hidden">
    <!-- Animated Glows -->
    <div class="nuxt-glow -top-20 -left-20"></div>
    <div class="nuxt-glow bottom-0 right-0 opacity-50"></div>

    <div class="animate-reveal [animation-delay:200ms] mb-8">
      <div class="relative inline-block">
        <div class="absolute inset-0 bg-[#00DC82] rounded-full blur-2xl opacity-20 animate-pulse"></div>
        <img 
          src="https://avatars.githubusercontent.com/u/76124039?v=4" 
          alt="Ringga Septia Pribadi" 
          class="relative w-32 h-32 md:w-40 md:h-40 rounded-full border-4 border-[#00DC82]/20 object-cover shadow-2xl"
        />
      </div>
    </div>

    <div class="animate-reveal [animation-delay:400ms] inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#00DC82]/10 border border-[#00DC82]/20 text-[#00DC82] text-xs font-bold mb-8">
      <span class="relative flex h-2 w-2">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00DC82] opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-[#00DC82]"></span>
      </span>
      OPEN TO NEW OPPORTUNITIES
    </div>
    
    <h1 class="animate-reveal [animation-delay:600ms] text-5xl md:text-8xl font-black mb-8 leading-[1.1] tracking-tight">
      Full-Stack <br />
      <span class="text-gradient">Developer</span>
    </h1>
    
    <p class="animate-reveal [animation-delay:800ms] text-slate-400 max-w-2xl text-lg md:text-xl mb-12 leading-relaxed">
      Crafting premium Android & Web applications with 3+ years of experience. Focused on performance, aesthetics, and user-centric solutions.
    </p>
    
    <div class="animate-reveal [animation-delay:1000ms] flex flex-col sm:flex-row gap-6">
      <NuxtLink to="/projects" class="btn-primary flex items-center justify-center gap-2 px-8 py-4">
        Explore Projects
        <ArrowRightIcon class="w-5 h-5" />
      </NuxtLink>
      <NuxtLink to="/about" class="btn-secondary flex items-center justify-center gap-2 px-8 py-4">
        Learn More
      </NuxtLink>
    </div>

    <!-- Tech Stack Icons -->
    <div class="animate-reveal [animation-delay:1200ms] mt-24 grid grid-cols-3 md:grid-cols-5 gap-8 md:gap-16 opacity-30 grayscale hover:grayscale-0 transition-all duration-500">
      <div class="flex items-center gap-3 group cursor-default">
        <div class="p-3 bg-slate-900 rounded-xl group-hover:bg-[#00DC82]/10 transition-colors">
          <SmartphoneIcon class="w-6 h-6 group-hover:text-[#00DC82]" />
        </div>
        <span class="text-sm font-bold">Android</span>
      </div>
      <div class="flex items-center gap-3 group cursor-default">
        <div class="p-3 bg-slate-900 rounded-xl group-hover:bg-[#00DC82]/10 transition-colors">
          <GlobeIcon class="w-6 h-6 group-hover:text-[#00DC82]" />
        </div>
        <span class="text-sm font-bold">Web</span>
      </div>
      <div class="flex items-center gap-3 group cursor-default">
        <div class="p-3 bg-slate-900 rounded-xl group-hover:bg-[#00DC82]/10 transition-colors">
          <DatabaseIcon class="w-6 h-6 group-hover:text-[#00DC82]" />
        </div>
        <span class="text-sm font-bold">SQL</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ArrowRightIcon, SmartphoneIcon, GlobeIcon, DatabaseIcon } from 'lucide-vue-next'
</script>
