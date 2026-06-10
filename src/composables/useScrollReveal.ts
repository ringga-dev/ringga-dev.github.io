import { onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'

export const useScrollReveal = () => {
  const route = useRoute()
  let observer: IntersectionObserver | null = null
  let revealTimeout: any = null

  const reveal = async () => {
    if (!process.client) return

    // Clean up existing observer and timeouts
    if (observer) observer.disconnect()
    if (revealTimeout) clearTimeout(revealTimeout)

    await nextTick()

    // Safety fallback: If elements don't reveal in 1.5s, force them
    revealTimeout = setTimeout(() => {
      document.querySelectorAll('.scroll-reveal:not(.reveal-active)').forEach(el => {
        el.classList.add('reveal-active')
      })
    }, 1500)

    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-active')
        }
      })
    }, {
      threshold: 0.05, // Lower threshold for better reliability
      rootMargin: '0px 0px -20px 0px'
    })

    const elements = document.querySelectorAll('.scroll-reveal')
    
    elements.forEach(el => {
      observer?.observe(el)
      
      // Immediate visibility check
      const rect = el.getBoundingClientRect()
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        el.classList.add('reveal-active')
      }
    })
  }

  watch(() => route.path, () => {
    // Reset and reveal on route change
    setTimeout(reveal, 150)
  })

  onMounted(() => {
    reveal()
    // Multiple retries for late-rendering components
    setTimeout(reveal, 500)
    setTimeout(reveal, 1200)
  })

  onUnmounted(() => {
    if (observer) observer.disconnect()
    if (revealTimeout) clearTimeout(revealTimeout)
  })

  return { reveal }
}
