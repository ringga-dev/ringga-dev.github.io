/**
 * Composable for custom cursor with magnetic effect
 * Emerald Zambrut Portfolio
 */

import { ref, onMounted, onUnmounted } from 'vue'

interface CursorPosition {
  x: number
  y: number
}

export function useCustomCursor() {
  const cursorX = ref(0)
  const cursorY = ref(0)
  const isHovering = ref(false)
  const isActive = ref(false)

  const handleMouseMove = (e: MouseEvent) => {
    cursorX.value = e.clientX
    cursorY.value = e.clientY
  }

  const handleMouseOver = () => {
    isHovering.value = true
  }

  const handleMouseOut = () => {
    isHovering.value = false
  }

  const handleClick = () => {
    isActive.value = true
    setTimeout(() => {
      isActive.value = false
    }, 150)
  }

  onMounted(() => {
    window.addEventListener('mousemove', handleMouseMove)
    
    // Add hover effect to interactive elements
    const interactiveElements = document.querySelectorAll('a, button, [role="button"]')
    interactiveElements.forEach(el => {
      el.addEventListener('mouseenter', handleMouseOver)
      el.addEventListener('mouseleave', handleMouseOut)
      el.addEventListener('click', handleClick)
    })
  })

  onUnmounted(() => {
    window.removeEventListener('mousemove', handleMouseMove)
    
    const interactiveElements = document.querySelectorAll('a, button, [role="button"]')
    interactiveElements.forEach(el => {
      el.removeEventListener('mouseenter', handleMouseOver)
      el.removeEventListener('mouseleave', handleMouseOut)
      el.removeEventListener('click', handleClick)
    })
  })

  return {
    cursorX,
    cursorY,
    isHovering,
    isActive
  }
}
