<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 min-h-screen relative overflow-hidden bg-surface text-main">
    <div class="max-w-5xl mx-auto relative z-10" v-if="exp">
      <!-- Breadcrumb -->
      <NuxtLink to="/about" class="inline-flex items-center gap-2 text-sm font-mono font-semibold uppercase tracking-wider text-muted hover:text-brand transition-colors mb-10 group">
        <ArrowLeftIcon class="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
        Back to About Me
      </NuxtLink>

      <!-- Main Layout Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Left Side: Role Header & Duration -->
        <div class="lg:col-span-5 space-y-8">
          <!-- Role Header Card -->
          <div class="riso-card p-8 bg-surface-card">
            <div class="w-14 h-14 rounded-sm border-[1.5px] border-ink text-brand flex items-center justify-center mb-6 shadow-[2px_2px_0_hsl(var(--brand-color)/0.6)]">
              <BriefcaseIcon class="w-6 h-6" />
            </div>
            
            <h1 class="text-3xl font-display font-bold text-main leading-tight mb-2">
              {{ exp.role }}
            </h1>
            <p class="text-brand font-semibold text-lg mb-6">{{ exp.company }}</p>

            <div class="inline-flex items-center gap-2 px-4 py-2 bg-surface-elevated border-[1.5px] border-ink/60 text-muted text-xs font-mono font-semibold w-full justify-center">
              <CalendarIcon class="w-4 h-4 text-brand" />
              {{ exp.period }}
            </div>
          </div>

          <!-- Technologies Used Card -->
          <div class="riso-card-2 p-8 bg-surface-card">
            <h3 class="text-sm font-mono font-semibold uppercase tracking-widest text-muted mb-6 border-b border-border pb-3">Tech Stack Used</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tech in exp.techUsed" 
                :key="tech"
                class="text-[9px] px-3.5 py-2 bg-surface-elevated text-main font-mono font-semibold uppercase tracking-widest border-[1.5px] border-ink/60 transition-[transform,box-shadow,border-color] duration-150 hover:border-ink-2 hover:text-ink-2 hover:-translate-x-0.5 hover:-translate-y-0.5"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </div>

        <!-- Right Side: Job details & Achievements -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Description Bento -->
          <div class="riso-card p-8 md:p-10 bg-surface-card">
            <h3 class="text-lg font-display font-bold text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Role Overview</h3>
            <p class="text-muted leading-relaxed font-serif text-lg">
              {{ exp.description }}
            </p>
          </div>

          <!-- Key Achievements Bento -->
          <div class="riso-card-2 p-8 md:p-10 bg-surface-card">
            <h3 class="text-lg font-display font-bold text-main uppercase tracking-wider mb-6 border-b border-border pb-3">Key Achievements</h3>
            <ul class="space-y-4">
              <li 
                v-for="achievement in exp.achievements" 
                :key="achievement"
                class="flex items-start gap-4 text-muted leading-relaxed font-serif"
              >
                <div class="w-2.5 h-2.5 bg-brand rotate-45 mt-2 flex-shrink-0"></div>
                <span>{{ achievement }}</span>
              </li>
            </ul>
          </div>
        </div>

      </div>
    </div>

    <!-- Error Fallback -->
    <div class="max-w-xl mx-auto text-center py-20" v-else>
      <BoxIcon class="w-16 h-16 text-muted mx-auto mb-6 opacity-30" />
      <h2 class="text-2xl font-display font-bold text-main mb-4">Experience Record Not Found</h2>
      <p class="text-muted mb-8 font-serif">The experience slug you are looking for does not exist in our registry.</p>
      <NuxtLink to="/about" class="btn-primary inline-flex py-4 px-10 text-xs font-mono font-semibold uppercase tracking-wider">
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
