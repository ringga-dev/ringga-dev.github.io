/**
 * useLightbox composable - Nuxt 4 SSR-safe lightbox state management
 * Uses useState for SSR hydration safety instead of raw ref()
 */
import { computed, onMounted, onUnmounted } from 'vue'

export interface LightboxItem {
  id: number
  title: string
  category: string
  image: string
  description?: string
}

export const useLightbox = (itemsGetter: () => LightboxItem[]) => {
  // SSR-safe state via Nuxt's useState
  const activeIndex = useState<number>('lightbox-active-index', () => -1)
  const isTransitioning = useState<boolean>('lightbox-transitioning', () => false)
  const direction = useState<'next' | 'prev' | 'none'>('lightbox-direction', () => 'none')

  const isOpen = computed(() => activeIndex.value >= 0)

  const currentItem = computed<LightboxItem | null>(() => {
    const items = itemsGetter()
    if (activeIndex.value >= 0 && activeIndex.value < items.length) {
      return items[activeIndex.value]
    }
    return null
  })

  const totalItems = computed(() => itemsGetter().length)

  const open = (id: number) => {
    const idx = itemsGetter().findIndex(item => item.id === id)
    if (idx !== -1) {
      direction.value = 'none'
      activeIndex.value = idx
      if (import.meta.client) {
        document.body.style.overflow = 'hidden'
      }
    }
  }

  const close = () => {
    activeIndex.value = -1
    direction.value = 'none'
    if (import.meta.client) {
      document.body.style.overflow = ''
    }
  }

  const next = () => {
    const items = itemsGetter()
    if (items.length === 0 || isTransitioning.value) return
    isTransitioning.value = true
    direction.value = 'next'
    activeIndex.value = (activeIndex.value + 1) % items.length
    setTimeout(() => { isTransitioning.value = false }, 350)
  }

  const prev = () => {
    const items = itemsGetter()
    if (items.length === 0 || isTransitioning.value) return
    isTransitioning.value = true
    direction.value = 'prev'
    activeIndex.value = (activeIndex.value - 1 + items.length) % items.length
    setTimeout(() => { isTransitioning.value = false }, 350)
  }

  // Keyboard handler
  const handleKeyDown = (e: KeyboardEvent) => {
    if (!isOpen.value) return
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault()
        next()
        break
      case 'ArrowLeft':
        e.preventDefault()
        prev()
        break
      case 'Escape':
        e.preventDefault()
        close()
        break
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
    if (isOpen.value) {
      document.body.style.overflow = ''
    }
  })

  return {
    activeIndex,
    isOpen,
    currentItem,
    totalItems,
    direction,
    isTransitioning,
    open,
    close,
    next,
    prev,
  }
}
