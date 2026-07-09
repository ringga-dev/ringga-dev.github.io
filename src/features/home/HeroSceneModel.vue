<template>
  <!-- Ambient wireframe sphere for depth -->
  <TresGroup ref="ambientRef">
    <TresMesh>
      <TresIcosahedronGeometry :args="[22, 1]" />
      <TresMeshBasicMaterial color="#00dc82" :wireframe="true" :transparent="true" :opacity="0.07" />
    </TresMesh>
  </TresGroup>

  <!-- Milky Way galaxy -->
  <HeroSceneGalaxy />
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef } from 'vue'
import HeroSceneGalaxy from '~/features/home/HeroSceneGalaxy.vue'

const ambientRef = shallowRef()

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (ambientRef.value) ambientRef.value.rotation.y -= delta * 0.04
})
</script>
