<template>
  <div class="absolute inset-0 z-0 w-full h-full">
    <ClientOnly>
      <TresCanvas alpha :dpr="[1, 2]">
        <TresPerspectiveCamera :position="[0, 0, 42]" :fov="55" :look-at="[0, 0, 0]" />
        <TresAmbientLight :intensity="1.2" />
        <TresDirectionalLight :position="[5, 10, 8]" :intensity="2.2" />
        <TresDirectionalLight :position="[-8, -3, -6]" :intensity="1" color="#36e4da" />

        <OrbitControls
          :enable-pan="false"
          :enable-zoom="false"
          :enable-damping="true"
          :min-azimuth-angle="-0.6"
          :max-azimuth-angle="0.6"
          :min-polar-angle="1.2"
          :max-polar-angle="1.9"
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
