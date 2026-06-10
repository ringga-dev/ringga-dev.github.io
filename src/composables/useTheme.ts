import { ref, onMounted } from 'vue'

export const useTheme = () => {
  const isDark = ref(true)

  const toggleTheme = () => {
    isDark.value = !isDark.value
    updateTheme()
  }

  const updateTheme = () => {
    if (process.client) {
      const root = document.documentElement
      if (isDark.value) {
        root.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        root.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
    }
  }

  onMounted(() => {
    if (process.client) {
      const savedTheme = localStorage.getItem('theme')
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      // Default to dark mode if not set or if saved as dark
      isDark.value = savedTheme ? savedTheme === 'dark' : systemPrefersDark
      updateTheme()
    }
  })

  return {
    isDark,
    toggleTheme
  }
}
