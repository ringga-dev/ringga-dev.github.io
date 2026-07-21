/**
 * Image optimization utilities for lazy loading and responsive images
 * Emerald Zambrut Portfolio
 */

import { ref, onMounted, onUnmounted } from 'vue'

interface UseLazyImageOptions {
  rootMargin?: string
  threshold?: number
  placeholder?: string
}

export function useLazyImage(options: UseLazyImageOptions = {}) {
  const {
    rootMargin = '50px',
    threshold = 0.1,
    placeholder = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"%3E%3Crect fill="%231a1a1a" width="400" height="300"/%3E%3C/svg%3E'
  } = options

  const imageRef = ref<HTMLImageElement | null>(null)
  const isLoaded = ref(false)
  const isInView = ref(false)
  const currentSrc = ref(placeholder)
  const error = ref(false)

  let observer: IntersectionObserver | null = null

  const loadImage = () => {
    if (!imageRef.value || !imageRef.value.dataset.src) return

    const img = new Image()
    img.src = imageRef.value.dataset.src as string
    
    img.onload = () => {
      if (imageRef.value) {
        imageRef.value.src = img.src
        isLoaded.value = true
        isInView.value = true
      }
    }
    
    img.onerror = () => {
      error.value = true
      console.warn('Failed to load image:', imageRef.value?.dataset.src)
    }
  }

  const handleIntersection = (entries: IntersectionObserverEntry[]) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        loadImage()
        if (observer) {
          observer.unobserve(entry.target)
        }
      }
    })
  }

  onMounted(() => {
    if (imageRef.value) {
      observer = new IntersectionObserver(handleIntersection, {
        rootMargin,
        threshold
      })
      
      observer.observe(imageRef.value)
    }
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  })

  return {
    imageRef,
    isLoaded,
    isInView,
    currentSrc,
    error
  }
}

/**
 * Generate responsive image sources
 */
export function generateResponsiveSources(
  baseUrl: string,
  sizes: number[] = [320, 640, 768, 1024, 1280, 1920],
  format: 'webp' | 'avif' | 'jpg' = 'webp'
): { srcset: string; sizes: string } {
  const srcset = sizes
    .map(size => `${baseUrl.replace(/\.(jpg|png|webp|avif)$/, '')}-${size}.${format} ${size}w`)
    .join(', ')
  
  const sizesAttr = `(max-width: ${sizes[sizes.length - 1]}px) 100vw, ${sizes[sizes.length - 1]}px`
  
  return {
    srcset,
    sizes: sizesAttr
  }
}

/**
 * Get optimized image URL with query params
 */
export function getOptimizedImageUrl(
  url: string,
  options: {
    width?: number
    height?: number
    quality?: number
    format?: 'webp' | 'avif' | 'jpg'
  } = {}
): string {
  const {
    width = 800,
    height,
    quality = 80,
    format = 'webp'
  } = options

  // If it's a CDN URL (Cloudinary, Imgix, etc.), add transformation params
  if (url.includes('cloudinary.com') || url.includes('imgix.net')) {
    // Add CDN-specific transformations
    return url
  }

  // For local images or generic URLs, return as-is
  // In production, you'd want to process these with an image optimizer
  return url
}

/**
 * Preload critical images
 */
export function preloadImages(urls: string[]): void {
  urls.forEach(url => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'image'
    link.href = url
    document.head.appendChild(link)
  })
}

/**
 * Blurhash placeholder generator (simplified)
 */
export function createBlurPlaceholder(color: string = '#1a1a1a'): string {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">
    <rect fill="${color}" width="1" height="1"/>
  </svg>`
  return `data:image/svg+xml;base64,${btoa(svg)}`
}
