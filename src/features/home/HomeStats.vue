<template>
  <section class="relative z-10 py-16">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid grid-cols-2 md:grid-cols-4 border border-border divide-x divide-border">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="text-center px-4 py-8"
        >
          <component :is="getIcon(stat.icon)" class="w-5 h-5 text-brand mx-auto mb-4" />
          <div class="text-4xl md:text-5xl font-display font-semibold text-main mb-2">
            <AnimatedCounter :target="stat.value" /><span class="text-brand">{{ stat.suffix }}</span>
          </div>
          <div class="font-mono text-[10px] text-muted uppercase tracking-[0.2em]">
            {{ stat.label }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { CalendarIcon, FolderIcon, StarIcon, BoxesIcon } from 'lucide-vue-next'
import homeData from '~/data/home.json'

const stats = ref(homeData.stats.map(s => ({ ...s })))

const getIcon = (name) => {
  switch (name) {
    case 'CalendarIcon': return CalendarIcon
    case 'FolderIcon': return FolderIcon
    case 'StarIcon': return StarIcon
    case 'BoxesIcon': return BoxesIcon
    default: return FolderIcon
  }
}

const findByLabel = (needle) => stats.value.find(s => s.label.toLowerCase().includes(needle))

onMounted(async () => {
  try {
    const user = await fetch('https://api.github.com/users/ringga-dev').then(r => r.json())
    if (user.public_repos != null) {
      const repoStat = findByLabel('repos')
      if (repoStat) repoStat.value = String(user.public_repos)
    }

    const repos = await fetch('https://api.github.com/users/ringga-dev/repos?per_page=100').then(r => r.json())
    if (Array.isArray(repos)) {
      const stars = repos.reduce((acc, repo) => acc + (repo.stargazers_count || 0), 0)
      const starsStat = findByLabel('stars')
      if (starsStat) starsStat.value = String(stars)
    }
  } catch (e) {
    console.warn('[HomeStats] GitHub stats unavailable, using defaults from home.json')
  }
})
</script>
