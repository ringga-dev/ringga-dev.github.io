<template>
  <TresGroup ref="galaxyRef" :position="[0, 0, 0]" :rotation="[Math.PI / 5, 0, 0]">
    <!-- Glowing core -->
    <TresMesh>
      <TresSphereGeometry :args="[2.2, 32, 32]" />
      <TresMeshBasicMaterial :color="coreColor" :transparent="true" :opacity="0.9" />
    </TresMesh>
    <TresPointLight :position="[0, 0, 0]" :color="coreColor" :intensity="6" :distance="40" />

    <!-- Spiral arms built from instanced points -->
    <TresPoints :position="[0, 0, 0]">
      <TresBufferGeometry :attributes="attributes" />
      <TresPointsMaterial
        :size="0.28"
        :size-attenuation="true"
        :vertex-colors="true"
        :transparent="true"
        :opacity="0.9"
        :depth-write="false"
        :blending="2"
      />
    </TresPoints>
  </TresGroup>
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef } from 'vue'

const coreColor = '#fff3c4'
const insideColor = '#5b8cff'
const outsideColor = '#ff7b3d'

const COUNT = 9000
const RADIUS = 16
const BRANCHES = 4
const SPIN = 1.1
const RANDOMNESS = 0.45
const RANDOMNESS_POWER = 2.6

const positions = new Float32Array(COUNT * 3)
const colors = new Float32Array(COUNT * 3)

const cIn = hexToRgb(insideColor)
const cOut = hexToRgb(outsideColor)

for (let i = 0; i < COUNT; i++) {
  const i3 = i * 3
  const radius = Math.pow(Math.random(), 1.4) * RADIUS
  const branchAngle = ((i % BRANCHES) / BRANCHES) * Math.PI * 2
  const spinAngle = radius * SPIN

  const rand = () =>
    Math.pow(Math.random(), RANDOMNESS_POWER) *
    (Math.random() < 0.5 ? 1 : -1) *
    RANDOMNESS *
    radius

  const rx = rand()
  const ry = rand() * 0.4
  const rz = rand()

  positions[i3] = Math.cos(branchAngle + spinAngle) * radius + rx
  positions[i3 + 1] = ry
  positions[i3 + 2] = Math.sin(branchAngle + spinAngle) * radius + rz

  const mixed = mix(cIn, cOut, radius / RADIUS)
  colors[i3] = mixed.r
  colors[i3 + 1] = mixed.g
  colors[i3 + 2] = mixed.b
}

const attributes = {
  position: { array: positions, itemSize: 3 },
  color: { array: colors, itemSize: 3 },
}

function hexToRgb(hex) {
  const n = parseInt(hex.replace('#', ''), 16)
  return { r: ((n >> 16) & 255) / 255, g: ((n >> 8) & 255) / 255, b: (n & 255) / 255 }
}
function mix(a, b, t) {
  return {
    r: a.r + (b.r - a.r) * t,
    g: a.g + (b.g - a.g) * t,
    b: a.b + (b.b - a.b) * t,
  }
}

const galaxyRef = shallowRef()

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (galaxyRef.value) galaxyRef.value.rotation.y += delta * 0.08
})
</script>
