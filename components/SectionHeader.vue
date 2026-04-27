<template>
  <div class="mb-12 md:mb-20 scroll-reveal" :class="[centered ? 'text-center' : 'text-left']">
    <div 
      class="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-brand/10 border border-brand/20 text-brand text-[10px] font-black tracking-[0.2em] uppercase mb-4"
    >
      {{ badge }}
    </div>
    <h2 class="mb-6 leading-tight">
      <slot name="title"></slot>
    </h2>
    <p 
      v-if="description" 
      class="text-slate-400 text-base md:text-lg font-medium leading-relaxed max-w-2xl"
      :class="[centered ? 'mx-auto' : '']"
    >
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  badge: String,
  description: String,
  centered: {
    type: Boolean,
    default: false
  }
})
</script>
