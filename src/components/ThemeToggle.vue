<template>
  <button 
    @click="toggleTheme" 
    class="relative w-11 h-11 flex items-center justify-center rounded-xl bg-surface-card/50 border border-border text-muted hover:text-brand hover:border-brand/30 transition-all duration-300 active:scale-90"
    aria-label="Toggle Theme"
  >
    <div class="relative w-6 h-6 transform transition-transform duration-500" :class="{ 'rotate-180': isDark }">
      <SunIcon v-if="!isDark" class="w-6 h-6 absolute inset-0 text-amber-500 animate-reveal" />
      <MoonIcon v-else class="w-6 h-6 absolute inset-0 text-brand animate-reveal" />
    </div>
  </button>
</template>

<script setup>
import { SunIcon, MoonIcon } from 'lucide-vue-next'
import { useTheme } from '~/composables/useTheme'

const { isDark, toggleTheme } = useTheme()
</script>
