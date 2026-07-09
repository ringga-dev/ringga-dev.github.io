<template>
  <TresGroup ref="rootRef" :position="[0, -4, 0]" :scale="avatarScale">
    <!--
      Drop your Ready Player Me export at: public/models/ringga-avatar.glb
      Create your avatar for free at https://readyplayer.me
      Tip: enable "Half-body" + "Mesh LOD 0 (high)" for best realism.
    -->
    <GLTFModel v-if="url" :path="url" :scale="1" @load="onLoad" />
  </TresGroup>
</template>

<script setup>
import { useGLTF } from '@tresjs/cientos'
import { useLoop } from '@tresjs/core'
import { shallowRef } from 'vue'

// Ganti nama file kalau Anda pakai nama lain
const url = '/models/ringga-avatar.glb'

const avatarScale = 6
const rootRef = shallowRef()

// useGLTF preloads & caches the model
useGLTF(url, { draco: true })

function onLoad(gltf) {
  console.log('[HeroSceneAvatarGLB] model loaded:', gltf)
}

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (rootRef.value) rootRef.value.rotation.y += delta * 0.25
})
</script>
