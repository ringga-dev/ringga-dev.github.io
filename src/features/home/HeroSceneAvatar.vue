<template>
  <TresGroup ref="avatarRef" :position="[0, -2, 0]" :scale="1.1">
    <!-- Head -->
    <TresMesh :position="[0, 0, 0]">
      <TresSphereGeometry :args="[6, 48, 48]" />
      <TresMeshStandardMaterial
        color="#f1c9a5"
        :roughness="0.55"
        :metalness="0.05"
        :emissive="brandColor"
        :emissive-intensity="0.04"
      />
    </TresMesh>

    <!-- Neck -->
    <TresMesh :position="[0, -6.4, 0]">
      <TresCylinderGeometry :args="[2.1, 2.6, 2.6, 32]" />
      <TresMeshStandardMaterial color="#e3b891" :roughness="0.6" :metalness="0.05" />
    </TresMesh>

    <!-- Hair cap -->
    <TresMesh :position="[0, 1.6, -0.2]">
      <TresSphereGeometry :args="[6.15, 48, 48, 0, Math.PI * 2, 0, Math.PI * 0.55]" />
      <TresMeshStandardMaterial color="#2b2b32" :roughness="0.8" :metalness="0.1" />
    </TresMesh>

    <!-- Eyes -->
    <TresMesh v-for="eye in eyes" :key="'eye-' + eye.x" :position="[eye.x, eye.y, eye.z]">
      <TresSphereGeometry :args="[0.7, 24, 24]" />
      <TresMeshStandardMaterial color="#ffffff" :roughness="0.3" />
    </TresMesh>
    <TresMesh v-for="pupil in pupils" :key="'pupil-' + pupil.x" :position="[pupil.x, pupil.y, pupil.z]">
      <TresSphereGeometry :args="[0.32, 24, 24]" />
      <TresMeshStandardMaterial color="#1b1b1f" :roughness="0.2" />
    </TresMesh>

    <!-- Glasses (brand-tinted frame) -->
    <TresMesh v-for="g in glasses" :key="'g-' + g.x" :position="[g.x, g.y, g.z]" :rotation="[0, 0, 0]">
      <TresTorusGeometry :args="[1.15, 0.12, 16, 32]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.5" :roughness="0.3" :metalness="0.6" />
    </TresMesh>
    <TresMesh :position="[0, 0.7, 5.78]">
      <TresBoxGeometry :args="[1.6, 0.12, 0.2]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.5" :roughness="0.3" :metalness="0.6" />
    </TresMesh>

    <!-- Nose -->
    <TresMesh :position="[0, -0.8, 5.9]" :rotation="[Math.PI / 2, 0, 0]">
      <TresConeGeometry :args="[1.1, 2.2, 24]" />
      <TresMeshStandardMaterial color="#eab98c" :roughness="0.6" />
    </TresMesh>

    <!-- Mouth -->
    <TresMesh :position="[0, -3, 5.4]" :rotation="[Math.PI / 2, 0, 0]">
      <TresTorusGeometry :args="[1.5, 0.35, 16, 32, Math.PI]" />
      <TresMeshStandardMaterial color="#9c4a3c" :roughness="0.5" />
    </TresMesh>

    <!-- Ears -->
    <TresMesh v-for="ear in ears" :key="'ear-' + ear.x" :position="[ear.x, ear.y, ear.z]">
      <TresSphereGeometry :args="[1.1, 24, 24]" />
      <TresMeshStandardMaterial color="#f1c9a5" :roughness="0.55" />
    </TresMesh>

    <!-- Brand ring halo -->
    <TresMesh :position="[0, -2, -7]" :rotation="[Math.PI / 2.4, 0, 0]">
      <TresTorusGeometry :args="[9, 0.15, 16, 64]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.8" :roughness="0.3" :metalness="0.6" />
    </TresMesh>
  </TresGroup>
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef } from 'vue'

const brandColor = '#00dc82'

const eyes = [
  { x: -2.2, y: 0.8, z: 5.4 },
  { x: 2.2, y: 0.8, z: 5.4 },
]
const pupils = [
  { x: -2.2, y: 0.8, z: 5.95 },
  { x: 2.2, y: 0.8, z: 5.95 },
]
const glasses = [
  { x: -2.2, y: 0.8, z: 5.6 },
  { x: 2.2, y: 0.8, z: 5.6 },
]
const ears = [
  { x: -6, y: 0, z: 0 },
  { x: 6, y: 0, z: 0 },
]

const avatarRef = shallowRef()

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (avatarRef.value) avatarRef.value.rotation.y += delta * 0.25
})
</script>
