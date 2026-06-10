<template>
  <div class="mb-20 bg-surface">
    <SectionHeader 
      badge="Professional Journey" 
      description="My evolution through various technical challenges and roles."
      centered
    >
      <template #title>Work <span class="text-gradient">Experience</span></template>
    </SectionHeader>

    <div class="max-w-4xl mx-auto mt-20 space-y-12 relative before:absolute before:left-0 md:before:left-8 before:top-4 before:bottom-4 before:w-px before:bg-gradient-to-b before:from-brand/50 before:via-brand-light/30 before:to-transparent">
      <div 
        v-for="job in timelineData" 
        :key="job.company" 
        class="relative pl-12 md:pl-24 scroll-reveal group"
      >
        <!-- Timeline Dot -->
        <div class="absolute left-0 md:left-8 -translate-x-1/2 top-0 w-4 h-4 rounded-full bg-surface border-2 border-brand shadow-[0_0_15px_rgba(0,220,130,0.3)] z-10 group-hover:scale-150 transition-transform duration-500">
          <div class="absolute inset-1 rounded-full bg-brand animate-pulse"></div>
        </div>
        
        <!-- Experience Card -->
        <NuxtLink :to="`/experience/${job.slug}`" class="glass-card p-8 rounded-[2rem] border border-border hover:border-brand/20 transition-all duration-500 hover:-translate-y-1 bg-surface-card block hover:shadow-brand/5">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div>
              <h3 class="text-2xl font-heading font-black text-main mb-1 group-hover:text-brand transition-colors">
                {{ job.role }}
              </h3>
              <p class="text-brand-light font-bold">{{ job.company }}</p>
            </div>
            <div class="px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-[9px] font-black uppercase tracking-widest whitespace-nowrap self-start md:self-center">
              {{ job.period }}
            </div>
          </div>
          <p class="text-muted leading-relaxed font-medium">
            {{ job.description }}
          </p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import aboutData from '~/data/about.json'

const timelineData = aboutData.experience
</script>
