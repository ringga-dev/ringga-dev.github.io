<template>
  <div class="glass-card p-8 rounded-[2.5rem] group hover:-translate-y-2 transition-all duration-500 scroll-reveal border-white/5 hover:border-brand/20 relative overflow-hidden">
    <div class="absolute -right-8 -bottom-8 w-32 h-32 bg-brand/5 rounded-full blur-3xl group-hover:bg-brand/10 transition-colors"></div>
    
    <div class="w-16 h-16 rounded-2xl bg-brand/5 flex items-center justify-center text-brand mb-8 group-hover:bg-brand group-hover:text-surface transition-all duration-500">
      <component :is="icon" class="w-8 h-8" />
    </div>
    
    <h3 class="text-2xl font-black mb-4 text-white group-hover:text-brand transition-colors">{{ title }}</h3>
    <p class="text-slate-400 font-medium leading-relaxed mb-8">
      {{ description }}
    </p>
    
    <ul class="space-y-3 mb-8">
      <li v-for="feature in features" :key="feature" class="flex items-center gap-3 text-sm font-bold text-slate-500 group-hover:text-slate-300">
        <div class="w-1.5 h-1.5 rounded-full bg-brand"></div>
        {{ feature }}
      </li>
    </ul>

    <div class="h-1 w-0 bg-brand group-hover:w-full transition-all duration-700 absolute bottom-0 left-0"></div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
  icon: [Object, Function],
  features: Array
})
</script>
