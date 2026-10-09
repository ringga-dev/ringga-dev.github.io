<template>
  <!--
    IMPORTANT: the initial value MUST be the target, not 0. This component is
    rendered during prerender, so whatever it emits at SSR time is what ships in
    the static HTML. Starting at 0 meant every crawler and every visitor before
    hydration saw "0 Years Experience / 0 GitHub Stars" — the numbers only
    appeared after JS ran. Emit the real value, then animate up from 0 on the
    client only.
  -->
  <span ref="counterRef">{{ displayValue }}</span>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  target: {
    type: [Number, String],
    required: true
  },
  duration: {
    type: Number,
    default: 2000
  }
})

const endValue = parseInt(props.target) || 0
const displayValue = ref(endValue)
const counterRef = ref(null)

onMounted(() => {
  if (endValue === 0) return

  const animate = () => {
    const startTime = performance.now()

    const update = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / props.duration, 1)
      // Ease out expo
      const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress)

      displayValue.value = Math.floor(easeProgress * endValue)

      if (progress < 1) {
        requestAnimationFrame(update)
      } else {
        displayValue.value = endValue
      }
    }

    displayValue.value = 0
    requestAnimationFrame(update)
  }

  // Only animate once the element is actually on screen; skip entirely if the
  // user prefers reduced motion.
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  if (reduced) return

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        animate()
        observer.disconnect()
      }
    }, { threshold: 0.4 })

    if (counterRef.value) observer.observe(counterRef.value)
    else animate()
  } else {
    animate()
  }
})
</script>
