<template>
  <section class="max-w-7xl mx-auto px-6 py-20 relative z-10 bg-surface">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-12">
      <div 
        v-for="stat in stats" 
        :key="stat.label" 
        class="glass-card p-8 rounded-[2rem] text-center group scroll-reveal relative overflow-hidden bg-surface-card border border-border"
      >
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-brand/20 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
        <div class="flex justify-center mb-6">
          <div class="w-14 h-14 rounded-2xl bg-brand/5 flex items-center justify-center text-brand group-hover:bg-brand group-hover:text-slate-950 transition-all duration-500 border border-brand/10">
            <component :is="getIcon(stat.icon)" class="w-7 h-7" />
          </div>
        </div>
        <div class="text-4xl md:text-5xl font-heading font-black text-main mb-2 transition-transform duration-500">
          <AnimatedCounter :target="stat.value" />{{ stat.suffix }}
        </div>
        <div class="text-[9px] font-black text-muted uppercase tracking-[0.2em]">
          {{ stat.label }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { CalendarIcon, FolderIcon, StarIcon, UsersIcon } from 'lucide-vue-next'
import homeData from '~/data/home.json'

const stats = ref(homeData.stats.map(s => ({ ...s })))

const getIcon = (name) => {
  switch (name) {
    case 'CalendarIcon': return CalendarIcon
    case 'FolderIcon': return FolderIcon
    case 'StarIcon': return StarIcon
    case 'UsersIcon': return UsersIcon
    default: return FolderIcon
  }
}

onMounted(async () => {
  try {
    const res = await fetch('https://api.github.com/users/ringga-dev')
    const data = await res.json()
    if (data.public_repos) {
      // Find repositories stat card
      const repoStat = stats.value.find(s => s.icon === 'UsersIcon')
      if (repoStat) repoStat.value = data.public_repos.toString()
    }
    
    // Fetch stars (approximate or via search)
    const reposRes = await fetch('https://api.github.com/users/ringga-dev/repos?per_page=100')
    const repos = await reposRes.json()
    if (Array.isArray(repos)) {
      const stars = repos.reduce((acc, repo) => acc + (repo.stargazers_count || 0), 0)
      const starsStat = stats.value.find(s => s.icon === 'StarIcon')
      if (starsStat) starsStat.value = stars.toString()
    }
  } catch (e) {
    console.warn('Failed to fetch GitHub stats, using home.json default fallback values')
    const starStat = stats.value.find(s => s.icon === 'StarIcon')
    if (starStat) starStat.value = '8'
    const repoStat = stats.value.find(s => s.icon === 'UsersIcon')
    if (repoStat) repoStat.value = '18'
  }
})
</script>
