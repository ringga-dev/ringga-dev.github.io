<template>
  <div ref="skillRef" class="glass-card p-6 rounded-3xl scroll-reveal group">
    <div class="flex items-center gap-4 mb-4">
      <div class="w-10 h-10 rounded-xl bg-brand/5 flex items-center justify-center text-brand group-hover:bg-brand group-hover:text-surface transition-all duration-500">
        <component :is="icon" class="w-5 h-5" />
      </div>
      <div class="flex-1">
        <div class="flex justify-between items-end mb-1">
          <span class="text-xs font-black text-white uppercase tracking-widest">{{ name }}</span>
          <span class="text-xs font-black text-brand">{{ level }}%</span>
        </div>
        <div class="h-1.5 w-full bg-slate-800/50 rounded-full overflow-hidden border border-white/5">
          <div 
            class="h-full bg-gradient-to-r from-brand to-brand-light rounded-full transition-all duration-1000 ease-out origin-left"
            :style="{ width: isVisible ? `${level}%` : '0%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  name: String,
  level: Number,
  icon: [Object, Function]
})

const isVisible = ref(false)
const skillRef = ref(null)

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      setTimeout(() => {
        isVisible.value = true
      }, 200)
      observer.disconnect()
    }
  }, { threshold: 0.1 })
  
  if (skillRef.value) {
    observer.observe(skillRef.value)
  }
})
</script>
