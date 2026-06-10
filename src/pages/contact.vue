<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 relative overflow-hidden bg-surface">
    <!-- Nebula blur glow background -->
    <div class="absolute top-1/3 left-1/4 w-[500px] h-[500px] bg-brand/5 blur-[150px] pointer-events-none rounded-full"></div>
    <div class="absolute bottom-1/3 right-1/4 w-[500px] h-[500px] bg-brand-light/5 blur-[150px] pointer-events-none rounded-full"></div>

    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Section Header -->
      <SectionHeader 
        :badge="contactData.badge"
        :description="contactData.description"
        centered
      >
        <template #title>
          {{ contactData.title }} <span class="text-gradient">{{ contactData.titleHighlight }}</span>
        </template>
      </SectionHeader>
      
      <!-- Side by Side Contact Info & Contact Form -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-stretch mt-12 md:mt-20">
        <ContactInfo />
        <ContactForm />
      </div>
    </div>
    
    <BackToTop />
  </div>
</template>

<script setup>
import SectionHeader from '~/components/SectionHeader.vue'
import contactData from '~/data/contact.json'
import globalData from '~/data/global.json'

useHead({
  title: `Contact | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: `Get in touch with ${globalData.siteName} for business inquiries, projects, and collaborations.` }
  ]
})
</script>
