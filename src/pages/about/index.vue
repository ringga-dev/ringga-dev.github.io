<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 relative overflow-hidden bg-surface">
    <div class="max-w-7xl mx-auto relative z-10">
      <AboutBio />

      <!-- Wrap slider in ClientOnly to avoid SSR window issues -->
      <ClientOnly>
        <AboutSlider />
      </ClientOnly>
      
      <AboutSkills />
      <AboutTimeline />
    </div>
    
    <BackToTop />
  </div>
</template>

<script setup>
import globalData from '~/data/global.json'

useHead({
  title: `About | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: `Learn more about the background, experience, and expert skills of ${globalData.siteName}.` }
  ]
})
</script>
