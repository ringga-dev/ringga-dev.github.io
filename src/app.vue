<template>
  <div class="min-h-screen relative selection:bg-brand/25 selection:text-main">
    <NuxtLoadingIndicator :height="3" color="hsl(12 78% 45%)" />
    
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
import { useTheme } from '~/composables/useThemeEnhanced'

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
/* Page transition: a printed sheet sliding into place. Translate + fade
   only, no blur (blur is the old glassy slop). Snappy, 200ms. */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
