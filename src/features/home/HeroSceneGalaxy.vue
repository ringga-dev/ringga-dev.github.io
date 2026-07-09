<template>
  <TresGroup ref="galaxyRef" :position="[0, 0, 0]" :rotation="[Math.PI / 5, 0, 0]">
    <!-- Glowing core -->
    <TresMesh>
      <TresSphereGeometry :args="[2.2, 32, 32]" />
      <TresMeshBasicMaterial :color="coreColor" :transparent="true" :opacity="0.9" />
    </TresMesh>
    <TresPointLight :position="[0, 0, 0]" :color="coreColor" :intensity="6" :distance="40" />
  </TresGroup>
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef, onMounted } from 'vue'
import * as THREE from 'three'

const coreColor = '#fff3c4'
const insideColor = '#5b8cff'
const outsideColor = '#ff7b3d'

const COUNT = 9000
const RADIUS = 16
const BRANCHES = 4
const SPIN = 1.1
const RANDOMNESS = 0.45
const RANDOMNESS_POWER = 2.6

const galaxyRef = shallowRef()

onMounted(() => {
  if (!galaxyRef.value) return

  const positions = new Float32Array(COUNT * 3)
  const colors = new Float32Array(COUNT * 3)
  const cIn = new THREE.Color(insideColor)
  const cOut = new THREE.Color(outsideColor)
  const mixed = new THREE.Color()

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

    mixed.copy(cIn).lerp(cOut, radius / RADIUS)
    colors[i3] = mixed.r
    colors[i3 + 1] = mixed.g
    colors[i3 + 2] = mixed.b
  }

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 0.28,
    sizeAttenuation: true,
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  })

  const points = new THREE.Points(geometry, material)
  galaxyRef.value.add(points)
})

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (galaxyRef.value) galaxyRef.value.rotation.y += delta * 0.08
})
</script>
