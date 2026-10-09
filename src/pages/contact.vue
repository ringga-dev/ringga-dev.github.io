<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 relative overflow-hidden bg-surface">
    <!-- Halftone plate accent, corner of the printed page -->
    <div class="halftone pointer-events-none absolute top-24 right-0 h-56 w-56 opacity-70" aria-hidden="true"></div>

    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Section Header -->
      <SectionHeader 
        badge="Get In Touch"
        number="05"
        :description="contactData.description"
        centered
      >
        <template #title>
          {{ contactData.title }} <span class="text-brand">{{ contactData.titleHighlight }}</span>
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
