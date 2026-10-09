<template>
  <div class="pt-32 md:pt-44 pb-24 px-6 min-h-screen relative overflow-hidden bg-surface">
    <!-- Riso screen accent: second spot-ink dot field, printed off register -->
    <div class="halftone-2 absolute top-24 -left-20 w-64 h-64 pointer-events-none opacity-50"></div>

    <!-- Projects Layout Grid component -->
    <ProjectsGrid />
    
    <BackToTop />
  </div>
</template>

<script setup>
import globalData from '~/data/global.json'

useHead({
  title: `Projects | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: `Browse selected open-source libraries, products, and technical developments created by ${globalData.siteName}.` }
  ]
})
</script>
