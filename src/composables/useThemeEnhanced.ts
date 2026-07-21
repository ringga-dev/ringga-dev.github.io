/**
 * Theme management composable with persistence
 * Emerald Zambrut Portfolio
 */

import { ref, computed, onMounted, watch } from 'vue'

type Theme = 'light' | 'dark'

interface UseThemeReturn {
  theme: Ref<Theme>
  isDark: ComputedRef<boolean>
  isLight: ComputedRef<boolean>
  toggleTheme: () => void
  setTheme: (theme: Theme) => void
}

export function useTheme(): UseThemeReturn {
  const STORAGE_KEY = 'emerald-zambrut-theme'
  
  // Initialize with system preference or stored value
  const getInitialTheme = (): Theme => {
    if (import.meta.client) {
      const stored = localStorage.getItem(STORAGE_KEY) as Theme | null
      if (stored && ['light', 'dark'].includes(stored)) {
        return stored
      }
      
      // Check system preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark'
      }
    }
    return 'light'
  }

  const theme = ref<Theme>(getInitialTheme())

  const isDark = computed(() => theme.value === 'dark')
  const isLight = computed(() => theme.value === 'light')

  const applyTheme = (newTheme: Theme) => {
    if (import.meta.client) {
      const html = document.documentElement
      
      if (newTheme === 'dark') {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
      
      // Update meta theme-color
      const metaThemeColor = document.querySelector('meta[name="theme-color"]')
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', newTheme === 'dark' ? '#0f172a' : '#ffffff')
      }
    }
  }

  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
    
    if (import.meta.client) {
      localStorage.setItem(STORAGE_KEY, newTheme)
      applyTheme(newTheme)
    }
  }

  const toggleTheme = () => {
    setTheme(theme.value === 'light' ? 'dark' : 'light')
  }

  // Watch for system theme changes
  onMounted(() => {
    applyTheme(theme.value)

    if (import.meta.client) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      
      const handleChange = (e: MediaQueryListEvent) => {
        // Only update if user hasn't manually set a preference
        const stored = localStorage.getItem(STORAGE_KEY)
        if (!stored) {
          setTheme(e.matches ? 'dark' : 'light')
        }
      }

      mediaQuery.addEventListener('change', handleChange)

      // Cleanup
      onUnmounted(() => {
        mediaQuery.removeEventListener('change', handleChange)
      })
    }
  })

  // Apply theme whenever it changes
  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  }, { immediate: true })

  return {
    theme,
    isDark,
    isLight,
    toggleTheme,
    setTheme
  }
}
