<template>
  <section class="relative z-10 py-16">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid grid-cols-2 md:grid-cols-4 border-[1.5px] border-ink/80 rounded-sm overflow-hidden shadow-riso divide-x divide-ink/20">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="text-center px-4 py-8 bg-surface-card"
        >
          <component :is="getIcon(stat.icon)" class="w-5 h-5 text-brand mx-auto mb-4" />
          <div class="numeral text-4xl md:text-5xl mb-2">
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
import { ref } from 'vue'
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

// Angka diambil dari home.json (sudah diverifikasi ke GitHub API). Tidak ada
// fetch runtime: itu menggeser angka setelah paint (layout shift) dan menambah
// round-trip pihak ketiga di jalan kritikal. Update home.json kalau angkanya berubah.
</script>
