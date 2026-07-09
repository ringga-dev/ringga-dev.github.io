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
  const cBlue = new THREE.Color('#3fa9ff') // electric blue
  const cIndigo = new THREE.Color('#7b6bff') // cyan-indigo
  const cWhite = new THREE.Color('#fff8e8')
  const cCopper = new THREE.Color('#a85a32') // copper dust
  const cCharcoal = new THREE.Color('#3a322c') // charcoal dust
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

    // color: white-hot near core -> electric blue/indigo in arms
    const roll = Math.random()
    if (t < 0.4) mixed.copy(cWhite).lerp(cBlue, t / 0.4)
    else mixed.copy(roll < 0.5 ? cBlue : cIndigo)
    if (roll < 0.12) mixed.copy(cCopper).lerp(cWhite, 0.35)

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
    const dustCol = Math.random() < 0.6 ? '#2a160c' : '#241f1a' // copper / charcoal
    const mat = new THREE.SpriteMaterial({
      map: glowTex,
      color: new THREE.Color(dustCol),
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

  // ============ GAS FILAMENTS (spiral streams flowing to center) ============
  for (let i = 0; i < 700; i++) {
    const t = Math.pow(Math.random(), 1.3)
    const radius = 2 + t * (RADIUS * 0.9)
    const angle = spiralAngle(i, radius, 6) + Math.PI // counter-flow subtle
    const x = Math.cos(angle) * radius
    const y = (Math.random() - 0.5) * 0.5 * (1 - t)
    const z = Math.sin(angle) * radius
    const mat = new THREE.SpriteMaterial({
      map: glowTex, color: new THREE.Color('#5a7bff'), transparent: true,
      opacity: 0.06 + (1 - t) * 0.12, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.position.set(x, y, z)
    const sz = 0.6 + (1 - t) * 1.5
    s.scale.set(sz, sz * 0.35, sz)
    root.add(s)
  }

  // ============ SATELLITE GALAXIES (M32 / M110) ============
  addSatellite(root, { pos: [16, 3, -6], size: 3.2, tint: '#ffd9a0' })
  addSatellite(root, { pos: [-15, -4, 4], size: 4.5, tint: '#c9b6ff' })

  // ============ DOUBLE NUCLEUS (Andromeda's odd core) ============
  // oval ring of old RED stars surrounding a small blue disk
  for (let i = 0; i < 220; i++) {
    const a = (i / 220) * Math.PI * 2
    const ex = 2.6 // oval eccentricity
    const x = Math.cos(a) * ex
    const z = Math.sin(a) * 1.5
    const y = (Math.random() - 0.5) * 0.3
    const mat = new THREE.SpriteMaterial({
      map: dotTex, color: new THREE.Color('#ff5a3c'), transparent: true,
      opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.position.set(x, y, z)
    const sz = 0.3 + Math.random() * 0.25
    s.scale.set(sz, sz, sz)
    root.add(s)
  }
  // small inner blue disk (young stars around the black hole)
  for (let i = 0; i < 160; i++) {
    const r = Math.random() * 1.4
    const a = Math.random() * Math.PI * 2
    const mat = new THREE.SpriteMaterial({
      map: dotTex, color: new THREE.Color('#9fe0ff'), transparent: true,
      opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(mat)
    s.position.set(Math.cos(a) * r, (Math.random() - 0.5) * 0.2, Math.sin(a) * r)
    const sz = 0.25 + Math.random() * 0.2
    s.scale.set(sz, sz, sz)
    root.add(s)
  }

  // ============ ACCRETION DISK + EVENT HORIZON (dramatic center) ============
  addBlackHole(root, glowTex, dotTex)

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

  // ============ HORIZONTAL LENS FLARE (thin, across core) ============
  const flareMat = new THREE.SpriteMaterial({
    map: makeFlareTexture(), color: new THREE.Color('#fff2c0'), transparent: true,
    opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
  })
  const flare = new THREE.Sprite(flareMat)
  flare.scale.set(60, 1.4, 1)
  root.add(flare)
})

function addBlackHole(root, glowTex, dotTex) {
  // Accretion disk: hot orange-red spinning ring (flat)
  const disk = new THREE.Mesh(
    new THREE.RingGeometry(0.9, 2.6, 64),
    new THREE.MeshBasicMaterial({
      color: new THREE.Color('#ff5a1e'),
      transparent: true,
      opacity: 0.9,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    })
  )
  disk.rotation.x = Math.PI / 2
  root.add(disk)

  // gravitational lensing glow ring (bright edge)
  const lens = new THREE.Mesh(
    new THREE.RingGeometry(2.6, 3.0, 64),
    new THREE.MeshBasicMaterial({
      color: new THREE.Color('#ffd27a'),
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    })
  )
  lens.rotation.x = Math.PI / 2
  root.add(lens)

  // Event horizon: perfect black sphere absorbing light
  const bh = new THREE.Mesh(
    new THREE.SphereGeometry(0.85, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0x000000 })
  )
  root.add(bh)

  // vertical lensed light (top/bottom arcs) for dramatic distortion look
  const arcMat = new THREE.SpriteMaterial({
    map: glowTex, color: new THREE.Color('#ff8a3c'), transparent: true,
    opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
  })
  const arcTop = new THREE.Sprite(arcMat)
  arcTop.position.set(0, 1.6, 0); arcTop.scale.set(2.5, 3, 1)
  root.add(arcTop)
  const arcBot = new THREE.Sprite(arcMat.clone())
  arcBot.position.set(0, -1.6, 0); arcBot.scale.set(2.5, 3, 1)
  root.add(arcBot)
}

function makeFlareTexture() {
  const w = 256, h = 32
  const canvas = document.createElement('canvas')
  canvas.width = w; canvas.height = h
  const ctx = canvas.getContext('2d')
  const g = ctx.createLinearGradient(0, 0, w, 0)
  g.addColorStop(0.0, 'rgba(255,240,190,0)')
  g.addColorStop(0.5, 'rgba(255,242,200,0.7)')
  g.addColorStop(1.0, 'rgba(255,240,190,0)')
  ctx.fillStyle = g
  ctx.fillRect(0, h / 2 - 2, w, 4)
  const tex = new THREE.CanvasTexture(canvas)
  tex.needsUpdate = true
  return tex
}

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
