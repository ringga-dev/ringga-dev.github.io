<template>
  <div class="mb-10 md:mb-14" :class="[centered ? 'text-center' : 'text-left']">
    <!-- Top row: oversize numeral + stamp label. The number is the
         printed-page voice; the stamp is a hand-pressed label, a few
         degrees off axis. -->
    <div
      v-if="number || badge"
      class="flex items-center gap-4 mb-4"
      :class="[centered ? 'justify-center' : '']"
    >
      <span v-if="number" class="numeral text-4xl md:text-5xl text-brand leading-none">
        {{ number }}
      </span>
      <span v-if="badge" class="stamp">{{ badge }}</span>
      <span v-if="number" class="hidden sm:block flex-1 h-px bg-border"></span>
    </div>

    <h2 class="mb-4 text-main max-w-3xl" :class="[centered ? 'mx-auto' : '']">
      <slot name="title"></slot>
    </h2>

    <div
      v-if="description"
      class="text-muted text-base md:text-lg leading-relaxed max-w-2xl font-serif"
      :class="[centered ? 'mx-auto' : '']"
    >
      {{ description }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  number: String,
  badge: String,
  description: String,
  centered: {
    type: Boolean,
    default: false
  }
})
</script>
