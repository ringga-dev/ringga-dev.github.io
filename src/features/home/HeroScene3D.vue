<template>
  <div class="absolute inset-0 z-0 w-full h-full">
    <ClientOnly>
      <TresCanvas alpha :dpr="[1, 2]">
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
</script>
