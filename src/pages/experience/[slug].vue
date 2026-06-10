<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 min-h-screen relative overflow-hidden bg-surface text-main">
    <!-- Background bubble glows -->
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-brand/5 blur-[150px] pointer-events-none rounded-full"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-brand-light/5 blur-[150px] pointer-events-none rounded-full"></div>

    <div class="max-w-5xl mx-auto relative z-10" v-if="exp">
      <!-- Breadcrumb -->
      <NuxtLink to="/about" class="inline-flex items-center gap-2 text-sm font-black uppercase tracking-wider text-muted hover:text-brand transition-colors mb-10 group">
        <ArrowLeftIcon class="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
        Back to About Me
      </NuxtLink>

      <!-- Main Layout Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Left Side: Role Header & Duration -->
        <div class="lg:col-span-5 space-y-8">
          <!-- Role Header Card -->
          <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border">
            <div class="w-14 h-14 rounded-2xl bg-brand/5 border border-brand/20 text-brand flex items-center justify-center mb-6">
              <BriefcaseIcon class="w-6 h-6" />
            </div>
            
            <h1 class="text-3xl font-heading font-black text-main leading-tight mb-2">
              {{ exp.role }}
            </h1>
            <p class="text-brand-light font-bold text-lg mb-6">{{ exp.company }}</p>

            <div class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-surface-elevated border border-border text-muted text-xs font-bold w-full justify-center">
              <CalendarIcon class="w-4 h-4 text-brand" />
              {{ exp.period }}
            </div>
          </div>

          <!-- Technologies Used Card -->
          <div class="glass-card p-8 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-sm font-black uppercase tracking-widest text-muted mb-6 border-b border-border pb-3">Tech Stack Used</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tech in exp.techUsed" 
                :key="tech"
                class="text-[9px] px-3.5 py-2 rounded-xl bg-surface-elevated text-main font-black uppercase tracking-widest border border-border transition-all hover:border-brand/40 hover:text-brand"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </div>

        <!-- Right Side: Job details & Achievements -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Description Bento -->
          <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-lg font-heading font-black text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Role Overview</h3>
            <p class="text-muted leading-relaxed font-medium text-lg">
              {{ exp.description }}
            </p>
          </div>

          <!-- Key Achievements Bento -->
          <div class="glass-card p-8 md:p-10 rounded-[2.5rem] bg-surface-card border border-border">
            <h3 class="text-lg font-heading font-black text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Key Achievements</h3>
            <ul class="space-y-4">
              <li 
                v-for="achievement in exp.achievements" 
                :key="achievement" 
                class="flex items-start gap-4 text-muted leading-relaxed font-medium"
              >
                <div class="w-2 h-2 rounded-full bg-brand mt-2 flex-shrink-0"></div>
                <span>{{ achievement }}</span>
              </li>
            </ul>
          </div>
        </div>

      </div>
    </div>

    <!-- Error Fallback -->
    <div class="max-w-xl mx-auto text-center py-20" v-else>
      <BoxIcon class="w-16 h-16 text-muted mx-auto mb-6 opacity-30 animate-bounce" />
      <h2 class="text-2xl font-black text-main mb-4">Experience Record Not Found</h2>
      <p class="text-muted mb-8 font-medium">The experience slug you are looking for does not exist in our registry.</p>
      <NuxtLink to="/about" class="btn-primary inline-flex py-4 px-10 text-xs font-black uppercase tracking-wider">
        Back to About Me
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ArrowLeftIcon, 
  BriefcaseIcon, 
  CalendarIcon, 
  BoxIcon 
} from 'lucide-vue-next'
import aboutData from '~/data/about.json'

const route = useRoute()

const exp = computed(() => {
  const slug = route.params.slug
  return aboutData.experience.find(e => e.slug === slug)
})

useHead({
  title: exp.value ? `${exp.value.role} at ${exp.value.company}` : 'Experience Details',
  meta: [
    { name: 'description', content: exp.value ? exp.value.description : 'Job role timeline details' }
  ]
})
</script>
