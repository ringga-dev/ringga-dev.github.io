<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0 translate-y-10 scale-90"
    enter-to-class="opacity-100 translate-y-0 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100 translate-y-0 scale-100"
    leave-to-class="opacity-0 translate-y-10 scale-90"
  >
    <button 
      v-show="isVisible"
      @click="scrollToTop"
      class="fixed bottom-8 right-8 z-40 w-12 h-12 rounded-2xl bg-brand text-surface shadow-2xl shadow-brand/20 flex items-center justify-center hover:bg-brand-light hover:-translate-y-1 transition-all active:scale-95"
      aria-label="Back to Top"
    >
      <ArrowUpIcon class="w-6 h-6" />
    </button>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowUpIcon } from 'lucide-vue-next'

const isVisible = ref(false)

const handleScroll = () => {
  isVisible.value = window.scrollY > 400
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
