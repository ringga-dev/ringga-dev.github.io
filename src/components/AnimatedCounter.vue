<template>
  <span ref="counterRef">{{ displayValue }}</span>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

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

const displayValue = ref(0)
const counterRef = ref(null)
const hasAnimated = ref(false)

const animate = () => {
  if (hasAnimated.value) return
  hasAnimated.value = true
  
  const startValue = 0
  const endValue = parseInt(props.target)
  const startTime = performance.now()
  
  const update = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / props.duration, 1)
    
    // Ease out expo
    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress)
    
    displayValue.value = Math.floor(easeProgress * (endValue - startValue) + startValue)
    
    if (progress < 1) {
      requestAnimationFrame(update)
    } else {
      displayValue.value = endValue
    }
  }
  
  requestAnimationFrame(update)
}

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      animate()
      observer.disconnect()
    }
  }, { threshold: 0.5 })
  
  if (counterRef.value) {
    observer.observe(counterRef.value)
  }
})
</script>
