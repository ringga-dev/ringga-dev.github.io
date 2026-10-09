<template>
  <div ref="wrap" class="absolute inset-0 z-0 w-full h-full">
    <ClientOnly>
      <TresCanvas v-if="active" alpha :dpr="dpr">
        <TresPerspectiveCamera :position="[0, 0, 42]" :fov="55" :look-at="[0, 0, 0]" />
        <TresAmbientLight :intensity="0.6" />

        <OrbitControls
          :enable-pan="false"
          :enable-zoom="true"
          :enable-damping="true"
          :min-distance="8"
          :max-distance="120"
        />

        <HeroSceneModel />
      </TresCanvas>
    </ClientOnly>
  </div>
</template>

<script setup>
import { OrbitControls } from '@tresjs/cientos'
import HeroSceneModel from '~/features/home/HeroSceneModel.vue'
import { onMounted, onBeforeUnmount, ref } from 'vue'

const wrap = ref(null)
const active = ref(false)

// Three.js is the single most expensive thing on this page (~264 KB gzipped and
// 120k GPU particles). Render it only while the hero is actually on screen and
// the tab is visible, otherwise the render loop burns battery and steals frames
// from scrolling on every other section.
const dpr = typeof window !== 'undefined' && window.innerWidth < 768 ? [1, 1] : [1, 2]

let io = null
const onVisibility = () => {
  if (document.hidden) active.value = false
  else if (io) evaluate()
}

const evaluate = () => {
  if (document.hidden) { active.value = false; return }
  const el = wrap.value
  if (!el) return
  const r = el.getBoundingClientRect()
  active.value = r.bottom > 0 && r.top < window.innerHeight
}

onMounted(() => {
  active.value = true
  document.addEventListener('visibilitychange', onVisibility)
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver(evaluate, { rootMargin: '200px 0px' })
    if (wrap.value) io.observe(wrap.value)
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('visibilitychange', onVisibility)
  if (io) io.disconnect()
})
</script>
