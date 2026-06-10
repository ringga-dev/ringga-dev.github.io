<template>
  <div class="pt-32 md:pt-44 pb-24 px-6 min-h-screen relative overflow-hidden bg-surface">
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
