<template>
  <div class="min-h-screen relative selection:bg-brand/30 selection:text-brand-dark">
    <!-- Global Background Elements -->
    <div class="bg-mesh"></div>
    <div class="nebula-bg"></div>
    <div class="noise-bg"></div>
    
    <!-- Decorative Glows -->
    <div class="glow w-[500px] h-[500px] bg-brand/5 top-[-100px] left-[-100px]"></div>
    <div class="glow w-[400px] h-[400px] bg-brand-light/5 bottom-[-50px] right-[-50px]"></div>
    
    <NuxtLoadingIndicator :height="3" />
    
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
  return route.path.startsWith('/projects/') && route.params.slug
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
