<template>
  <button 
    @click="toggleTheme" 
    class="relative w-11 h-11 flex items-center justify-center rounded-xl bg-surface-card/50 border border-border text-muted hover:text-brand hover:border-brand/30 transition-all duration-300 active:scale-90"
    aria-label="Toggle Theme"
  >
    <div class="relative w-6 h-6">
      <SunIcon class="w-6 h-6 absolute inset-0 text-brand transition-all duration-500" :class="isDark ? 'opacity-0 rotate-90 scale-0' : 'opacity-100 rotate-0 scale-100'" />
      <MoonIcon class="w-6 h-6 absolute inset-0 text-brand transition-all duration-500" :class="isDark ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 -rotate-90 scale-0'" />
    </div>
  </button>
</template>

<script setup>
import { SunIcon, MoonIcon } from 'lucide-vue-next'
import { useTheme } from '~/composables/useThemeEnhanced'

const { isDark, toggleTheme } = useTheme()
</script>
