<template>
  <div class="min-h-screen relative selection:bg-brand/20 selection:text-brand-dark">
    <NuxtLoadingIndicator :height="2" color="hsl(12 78% 43%)" />
    
    <Navbar v-if="!hideNavAndFooter" />
    
    <main class="relative z-10">
      <NuxtPage />
    </main>

    <Footer v-if="!hideNavAndFooter" />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useScrollReveal } from '~/composables/useScrollReveal'
import { useTheme } from '~/composables/useThemeEnhanced'

const { reveal } = useScrollReveal()
// Pre-initialize theme hooks
useTheme()

const route = useRoute()
const hideNavAndFooter = computed(() => {
  const p = route.path
  return (p.startsWith('/projects/') && route.params.slug) ||
         p.startsWith('/blog') ||
         p.startsWith('/news')
})

onMounted(() => {
  // Ensure the page is scrolled to top on initial load
  window.scrollTo(0, 0)
})
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
  filter: blur(10px);
}
</style>
