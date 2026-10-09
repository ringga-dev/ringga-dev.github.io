<template>
  <div class="mb-20 bg-surface">
    <SectionHeader
      badge="Professional Journey"
      description="My evolution through various technical challenges and roles."
      centered
    >
      <template #title>Work <span class="text-brand">Experience</span></template>
    </SectionHeader>

    <div class="max-w-4xl mx-auto mt-20 space-y-12 relative before:absolute before:left-0 md:before:left-8 before:top-4 before:bottom-4 before:w-px before:bg-ink/30">
      <div
        v-for="(job, index) in timelineData"
        :key="job.company"
        class="relative pl-12 md:pl-24 group"
      >
        <!-- Timeline Dot -->
        <div class="absolute left-0 md:left-8 -translate-x-1/2 top-1 w-4 h-4 rounded-sm bg-surface-card border-[2px] border-brand shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)] z-10">
          <div class="absolute inset-1 rounded-sm bg-brand"></div>
        </div>

        <!-- Experience Card -->
        <NuxtLink
          :to="`/experience/${job.slug}`"
          :class="[
            'p-8 bg-surface-card block',
            index % 2 === 1 ? 'riso-card-2' : 'riso-card'
          ]"
        >
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div>
              <h3 class="text-2xl font-display font-bold text-main mb-1 group-hover:text-brand transition-colors duration-150">
                {{ job.role }}
              </h3>
              <p class="text-brand font-mono text-xs font-semibold uppercase tracking-[0.18em]">{{ job.company }}</p>
            </div>
            <span class="stamp self-start md:self-center whitespace-nowrap">
              {{ job.period }}
            </span>
          </div>
          <p class="text-muted leading-relaxed font-serif">
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
