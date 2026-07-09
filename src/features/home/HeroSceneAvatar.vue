<template>
  <TresGroup ref="avatarRef" :position="[0, -2, 0]" :scale="1.05">
    <!-- Head (slightly elongated for a natural skull shape) -->
    <TresMesh :position="[0, 0, 0]" :scale="[1, 1.18, 1.05]">
      <TresSphereGeometry :args="[6, 64, 64]" />
      <TresMeshStandardMaterial
        color="#f3cba8"
        :roughness="0.45"
        :metalness="0.04"
        :emissive="brandColor"
        :emissive-intensity="0.03"
      />
    </TresMesh>

    <!-- Jaw / chin (tapered lower face) -->
    <TresMesh :position="[0, -3.4, 0.6]" :scale="[0.82, 0.7, 0.85]">
      <TresSphereGeometry :args="[4, 48, 48]" />
      <TresMeshStandardMaterial color="#f0c4a0" :roughness="0.5" :metalness="0.04" />
    </TresMesh>

    <!-- Cheeks (soft volume) -->
    <TresMesh v-for="cheek in cheeks" :key="'cheek-' + cheek.x" :position="[cheek.x, cheek.y, cheek.z]" :scale="[1, 0.8, 0.7]">
      <TresSphereGeometry :args="[1.8, 32, 32]" />
      <TresMeshStandardMaterial color="#f0c4a0" :roughness="0.5" :metalness="0.03" />
    </TresMesh>

    <!-- Neck -->
    <TresMesh :position="[0, -7.2, 0]">
      <TresCylinderGeometry :args="[2.0, 2.7, 3, 40]" />
      <TresMeshStandardMaterial color="#e7bd98" :roughness="0.55" :metalness="0.04" />
    </TresMesh>

    <!-- Hair (cap + slight volume, using a half sphere slightly larger than head) -->
    <TresMesh :position="[0, 1.4, -0.3]" :scale="[1.02, 1.2, 1.05]">
      <TresSphereGeometry :args="[6.05, 64, 64, 0, Math.PI * 2, 0, Math.PI * 0.58]" />
      <TresMeshStandardMaterial color="#2c2c34" :roughness="0.85" :metalness="0.12" />
    </TresMesh>

    <!-- Eyebrows -->
    <TresMesh v-for="brow in brows" :key="'brow-' + brow.x" :position="[brow.x, brow.y, brow.z]" :rotation="[0, 0, brow.r]" :scale="[1.6, 0.3, 0.3]">
      <TresCylinderGeometry :args="[0.5, 0.5, 1, 16]" />
      <TresMeshStandardMaterial color="#3a2a1c" :roughness="0.8" />
    </TresMesh>

    <!-- Eyes (sclera) -->
    <TresMesh v-for="eye in eyes" :key="'eye-' + eye.x" :position="[eye.x, eye.y, eye.z]">
      <TresSphereGeometry :args="[0.78, 32, 32]" />
      <TresMeshStandardMaterial color="#fbfbfb" :roughness="0.25" :metalness="0.05" />
    </TresMesh>
    <!-- Iris -->
    <TresMesh v-for="iris in irises" :key="'iris-' + iris.x" :position="[iris.x, iris.y, iris.z]">
      <TresSphereGeometry :args="[0.42, 32, 32]" />
      <TresMeshStandardMaterial color="#2f6f4f" :roughness="0.2" :metalness="0.1" />
    </TresMesh>
    <!-- Pupils -->
    <TresMesh v-for="pupil in pupils" :key="'pupil-' + pupil.x" :position="[pupil.x, pupil.y, pupil.z]">
      <TresSphereGeometry :args="[0.2, 24, 24]" />
      <TresMeshStandardMaterial color="#15151a" :roughness="0.15" />
    </TresMesh>

    <!-- Glasses frame (brand-tinted, thin & smooth) -->
    <TresMesh v-for="g in glasses" :key="'g-' + g.x" :position="[g.x, g.y, g.z]">
      <TresTorusGeometry :args="[1.25, 0.09, 20, 48]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.45" :roughness="0.25" :metalness="0.7" />
    </TresMesh>
    <TresMesh :position="[0, 0.85, 5.82]">
      <TresBoxGeometry :args="[1.7, 0.09, 0.18]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.45" :roughness="0.25" :metalness="0.7" />
    </TresMesh>

    <!-- Nose (smooth tapered, two stacked spheres + tip) -->
    <TresMesh :position="[0, -0.4, 5.6]" :scale="[0.9, 1.2, 0.9]">
      <TresSphereGeometry :args="[0.95, 32, 32]" />
      <TresMeshStandardMaterial color="#eebf99" :roughness="0.5" />
    </TresMesh>
    <TresMesh :position="[0, -1.3, 5.95]" :scale="[0.7, 0.6, 0.7]">
      <TresSphereGeometry :args="[0.9, 32, 32]" />
      <TresMeshStandardMaterial color="#eebf99" :roughness="0.5" />
    </TresMesh>

    <!-- Mouth (soft, gentle smile) -->
    <TresMesh :position="[0, -3.2, 5.45]" :rotation="[Math.PI / 2, 0, 0]">
      <TresTorusGeometry :args="[1.3, 0.28, 20, 40, Math.PI]" />
      <TresMeshStandardMaterial color="#a85142" :roughness="0.45" />
    </TresMesh>

    <!-- Ears (rounded, attached smoothly) -->
    <TresMesh v-for="ear in ears" :key="'ear-' + ear.x" :position="[ear.x, ear.y, ear.z]" :scale="[0.7, 1, 0.6]">
      <TresSphereGeometry :args="[1.2, 32, 32]" />
      <TresMeshStandardMaterial color="#f0c4a0" :roughness="0.5" />
    </TresMesh>

    <!-- Brand ring halo (soft glow, sits behind) -->
    <TresMesh :position="[0, -2, -7.5]" :rotation="[Math.PI / 2.4, 0, 0]">
      <TresTorusGeometry :args="[9.2, 0.12, 20, 80]" />
      <TresMeshStandardMaterial :color="brandColor" :emissive="brandColor" :emissive-intensity="0.75" :roughness="0.3" :metalness="0.6" />
    </TresMesh>
  </TresGroup>
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef } from 'vue'

const brandColor = '#00dc82'

const eyes = [
  { x: -2.3, y: 0.9, z: 5.45 },
  { x: 2.3, y: 0.9, z: 5.45 },
]
const irises = [
  { x: -2.3, y: 0.9, z: 5.9 },
  { x: 2.3, y: 0.9, z: 5.9 },
]
const pupils = [
  { x: -2.3, y: 0.9, z: 6.05 },
  { x: 2.3, y: 0.9, z: 6.05 },
]
const brows = [
  { x: -2.3, y: 2.0, z: 5.5, r: 0.15 },
  { x: 2.3, y: 2.0, z: 5.5, r: -0.15 },
]
const glasses = [
  { x: -2.3, y: 0.9, z: 5.62 },
  { x: 2.3, y: 0.9, z: 5.62 },
]
const cheeks = [
  { x: -3.4, y: -1.4, z: 4.6 },
  { x: 3.4, y: -1.4, z: 4.6 },
]
const ears = [
  { x: -6.1, y: 0.2, z: 0 },
  { x: 6.1, y: 0.2, z: 0 },
]

const avatarRef = shallowRef()

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (avatarRef.value) avatarRef.value.rotation.y += delta * 0.25
})
</script>
