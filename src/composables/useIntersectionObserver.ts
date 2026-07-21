/**
 * Composable for intersection observer animations
 * Emerald Zambrut Portfolio
 */

import { ref, onMounted, onUnmounted } from 'vue'

interface UseIntersectionObserverOptions {
  threshold?: number | number[]
  rootMargin?: string
  triggerOnce?: boolean
}

export function useIntersectionObserver(options: UseIntersectionObserverOptions = {}) {
  const {
    threshold = 0.1,
    rootMargin = '0px',
    triggerOnce = true
  } = options

  const targetRef = ref<HTMLElement | null>(null)
  const isVisible = ref(false)
  const hasTriggered = ref(false)

  let observer: IntersectionObserver | null = null

  const handleIntersection = (entries: IntersectionObserverEntry[]) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        isVisible.value = true
        
        if (triggerOnce && !hasTriggered.value) {
          hasTriggered.value = true
          // Unobserve after first trigger if triggerOnce is true
          if (observer) {
            observer.unobserve(entry.target)
          }
        }
      } else if (!triggerOnce) {
        isVisible.value = false
      }
    })
  }

  onMounted(() => {
    if (targetRef.value) {
      observer = new IntersectionObserver(handleIntersection, {
        threshold,
        rootMargin
      })
      
      observer.observe(targetRef.value)
    }
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  })

  return {
    targetRef,
    isVisible,
    hasTriggered
  }
}
