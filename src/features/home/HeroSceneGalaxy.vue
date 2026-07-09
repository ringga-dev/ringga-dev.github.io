<template>
  <TresGroup ref="galaxyRef" :position="[0, 0, 0]" :rotation="[Math.PI / 3.2, 0, 0]">
    <TresPointLight :position="[0, 0, 0]" :color="'#fff0c0'" :intensity="6" :distance="70" :decay="1.3" />
    <TresAmbientLight :color="'#2a3560'" :intensity="0.5" />
    <TresDirectionalLight :position="[0, 0, -20]" :color="'#6fa8ff'" :intensity="1.0" />
  </TresGroup>
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef, onMounted } from 'vue'
import * as THREE from 'three'

const galaxyRef = shallowRef()

const RADIUS = 19

function spiralAngle(i, radius, branches) {
  const branchAngle = ((i % branches) / branches) * Math.PI * 2
  const spinAngle = Math.log(radius + 1.2) * 2.6
  return branchAngle + spinAngle
}

onMounted(() => {
  const root = galaxyRef.value
  if (!root) return

  const dotTex = makeDotTexture()
  const glowTex = makeGlowTexture()

  // ============ FIELD STARS (background, deep space) ============
  for (let i = 0; i < 1500; i++) {
    const r = 30 + Math.random() * 40
    const theta = Math.random() * Math.PI * 2
    const phi = Math.acos(2 * Math.random() - 1)
    const x = r * Math.sin(phi) * Math.cos(theta)
    const y = r * Math.cos(phi) * 0.6
    const z = r * Math.sin(phi) * Math.sin(theta)
    const tint = Math.random() < 0.5 ? '#ffffff' : (Math.random() < 0.5 ? '#bcd2ff' : '#ffe6c0')
    const size = 0.15 + Math.random() * 0.5
    const mat = new THREE.SpriteMaterial({
      map: dotTex, color: new THREE.Color(tint), transparent: true,
      opacity: 0.4 + Math.random() * 0.6, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.position.set(x, y, z)
    s.scale.set(size, size, size)
    root.add(s)
  }

  // ============ SPIRAL ARMS (blue/white stars + dust lanes) ============
  const STAR_COUNT = 4500
  const BRANCHES = 6
  const cBlue = new THREE.Color('#9fc4ff')
  const cWhite = new THREE.Color('#fff8e8')
  const cBrown = new THREE.Color('#b5713a')
  const mixed = new THREE.Color()

  for (let i = 0; i < STAR_COUNT; i++) {
    const t = Math.pow(Math.random(), 1.7)
    const radius = t * RADIUS
    const angle = spiralAngle(i, radius, BRANCHES)

    const scatter = () =>
      Math.pow(Math.random(), 3.0) * (Math.random() < 0.5 ? 1 : -1) * radius * 0.4

    const x = Math.cos(angle) * radius + scatter()
    const y = (Math.random() - 0.5) * (1.4 - t * 1.0) + scatter() * 0.2
    const z = Math.sin(angle) * radius + scatter()

    // color: white-hot near core -> blue in arms, with occasional brown (dust glow)
    const roll = Math.random()
    if (t < 0.4) mixed.copy(cWhite).lerp(cBlue, t / 0.4)
    else mixed.copy(cBlue)
    if (roll < 0.12) mixed.copy(cBrown).lerp(cWhite, 0.4)

    const v = 0.85 + Math.random() * 0.15
    const size = 0.3 + Math.random() * 0.55
    const mat = new THREE.SpriteMaterial({
      map: dotTex, color: new THREE.Color(mixed.r * v, mixed.g * v, mixed.b * v),
      transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.position.set(x, y, z)
    s.scale.set(size, size, size)
    root.add(s)
  }

  // ============ DUST LANES (opaque dark, along arms) ============
  const DUST_COUNT = 2200
  for (let i = 0; i < DUST_COUNT; i++) {
    const t = 0.25 + Math.random() * 0.75
    const radius = t * RADIUS
    const angle = spiralAngle(i, radius, BRANCHES) + 0.25 // offset to sit between star bands
    const scatter = () =>
      Math.pow(Math.random(), 2.2) * (Math.random() < 0.5 ? 1 : -1) * radius * 0.35

    const x = Math.cos(angle) * radius + scatter()
    const y = (Math.random() - 0.5) * 0.9
    const z = Math.sin(angle) * radius + scatter()

    const size = 0.8 + Math.random() * 2.2
    const mat = new THREE.SpriteMaterial({
      map: glowTex,
      color: new THREE.Color('#1a0f0a'),
      transparent: true,
      opacity: 0.55 + Math.random() * 0.3, // opaque-ish, dark
      depthWrite: false,
      blending: THREE.NormalBlending, // NOT additive -> reads as dark matter
    })
    const s = new THREE.Sprite(mat)
    s.position.set(x, y, z)
    s.scale.set(size, size * 0.5, size)
    root.add(s)
  }

  // ============ COSMIC HAZE (soft blue/pink glow) ============
  const hazeLayers = [
    { count: 320, size: 8, opacity: 0.028, tint: '#4f6bff' },
    { count: 230, size: 12, opacity: 0.018, tint: '#ff7b9c' },
    { count: 160, size: 19, opacity: 0.01, tint: '#7a5bff' },
  ]
  hazeLayers.forEach((layer) => {
    for (let i = 0; i < layer.count; i++) {
      const t = Math.pow(Math.random(), 0.7)
      const radius = t * RADIUS * 1.05
      const angle = spiralAngle(i, radius, BRANCHES) * 0.92
      const x = Math.cos(angle) * radius + (Math.random() - 0.5) * radius * 0.6
      const y = (Math.random() - 0.5) * 1.3
      const z = Math.sin(angle) * radius + (Math.random() - 0.5) * radius * 0.6
      const hc = new THREE.Color(layer.tint).lerp(new THREE.Color('#ffd9a0'), Math.random() * 0.3)
      const mat = new THREE.SpriteMaterial({
        map: glowTex, color: hc, transparent: true, opacity: layer.opacity,
        depthWrite: false, blending: THREE.AdditiveBlending,
      })
      const s = new THREE.Sprite(mat)
      s.position.set(x, y, z)
      s.scale.set(layer.size, layer.size, layer.size)
      root.add(s)
    }
  })

  // ============ SATELLITE GALAXIES (M32 / M110) ============
  addSatellite(root, { pos: [16, 3, -6], size: 3.2, tint: '#ffd9a0' })
  addSatellite(root, { pos: [-15, -4, 4], size: 4.5, tint: '#c9b6ff' })

  // ============ BULGE / CORE (bright yellow-white, strong glow) ============
  const coreSprites = [
    { size: 5, color: '#fff6d8', opacity: 0.98 },
    { size: 10, color: '#ffe6a0', opacity: 0.55 },
    { size: 18, color: '#ffcf7a', opacity: 0.3 },
    { size: 34, color: '#88aaff', opacity: 0.18 },
  ]
  coreSprites.forEach((c) => {
    const mat = new THREE.SpriteMaterial({
      map: glowTex, color: c.color, transparent: true, opacity: c.opacity,
      depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.scale.set(c.size, c.size, c.size)
    root.add(s)
  })
  // small solid bulge center
  const bulgeMat = new THREE.SpriteMaterial({
    map: dotTex, color: new THREE.Color('#fff8e0'), transparent: true, opacity: 1,
    depthWrite: false, blending: THREE.AdditiveBlending,
  })
  const bulge = new THREE.Sprite(bulgeMat)
  bulge.scale.set(3.5, 3.5, 3.5)
  root.add(bulge)
})

function addSatellite(root, { pos, size, tint }) {
  const mat = new THREE.SpriteMaterial({
    map: makeGlowTexture(), color: new THREE.Color(tint), transparent: true,
    opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
  })
  const s = new THREE.Sprite(mat)
  s.position.set(...pos)
  s.scale.set(size, size * 0.7, size) // oval
  root.add(s)
}

function makeDotTexture() {
  const size = 64
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')
  const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2)
  g.addColorStop(0, 'rgba(255,255,255,1)')
  g.addColorStop(0.35, 'rgba(255,255,255,0.85)')
  g.addColorStop(0.7, 'rgba(255,255,255,0.18)')
  g.addColorStop(1, 'rgba(255,255,255,0)')
  ctx.fillStyle = g
  ctx.fillRect(0, 0, size, size)
  const tex = new THREE.CanvasTexture(canvas)
  tex.needsUpdate = true
  return tex
}

function makeGlowTexture() {
  const size = 256
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')
  const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2)
  g.addColorStop(0.0, 'rgba(255,255,255,1)')
  g.addColorStop(0.2, 'rgba(255,244,214,0.7)')
  g.addColorStop(0.5, 'rgba(255,214,150,0.2)')
  g.addColorStop(1.0, 'rgba(255,200,120,0)')
  ctx.fillStyle = g
  ctx.fillRect(0, 0, size, size)
  const tex = new THREE.CanvasTexture(canvas)
  tex.needsUpdate = true
  return tex
}

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (galaxyRef.value) galaxyRef.value.rotation.y += delta * 0.05
})
</script>
