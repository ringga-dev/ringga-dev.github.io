<template>
  <primitive v-if="galaxy" :object="galaxy" />
</template>

<script setup>
import { useLoop } from '@tresjs/core'
import { shallowRef, onMounted } from 'vue'
import * as THREE from 'three'

const galaxy = shallowRef(null)
const RADIUS = 19
const BRANCHES = 6

function spiralAngle(i, radius) {
  const branch = i % BRANCHES
  const branchAngle = (branch / BRANCHES) * Math.PI * 2 + (branch % 2 === 0 ? 0.3 : -0.2)
  return branchAngle + Math.log(radius + 1.2) * 2.6
}

onMounted(() => {
  const root = new THREE.Group()
  root.rotation.set(Math.PI / 3.2, 0, 0)

  const dotTex = makeDotTexture()
  const glowTex = makeGlowTexture()

  const gauss = () => {
    let u = 0, v = 0
    while (u === 0) u = Math.random()
    while (v === 0) v = Math.random()
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v)
  }

  // ---- bright core point light ----
  const coreLight = new THREE.PointLight(0xfff0c0, 6, 70, 1.3)
  root.add(coreLight)

  // ============ DENSE STAR FIELD (3 layer PointsMaterial) ============
  const LAYERS = [
    { count: 90000, size: 0.16 },
    { count: 22000, size: 0.3 },
    { count: 8000, size: 0.55 },
  ]
  const cCore = new THREE.Color('#fff4d6')
  const cBlue = new THREE.Color('#3fa9ff')
  const cIndigo = new THREE.Color('#7b6bff')
  const cCopper = new THREE.Color('#a85a32')
  const mixed = new THREE.Color()

  const starData = []
  LAYERS.forEach((layer, layerIdx) => {
    const positions = new Float32Array(layer.count * 3)
    const colors = new Float32Array(layer.count * 3)
    for (let i = 0; i < layer.count; i++) {
      const i3 = i * 3
      const radius = Math.pow(Math.random(), 2.2) * RADIUS
      const angle = spiralAngle(i, radius)
      const armWidth = 0.18 + radius * 0.045
      const off = gauss() * armWidth
      const wobble = Math.sin(radius * 0.6 + i * 0.0001) * 0.4 + gauss() * 0.25
      const inArm = Math.random() > 0.25
      const jitter = inArm ? 0 : gauss() * RADIUS * 0.4
      const radial = radius + gauss() * 0.4 + jitter
      const a = angle + wobble + (inArm ? 0 : Math.PI * Math.random())
      const x = Math.cos(a) * radial - Math.sin(a) * off
      const z = Math.sin(a) * radial + Math.cos(a) * off
      const y = gauss() * (0.9 - (radius / RADIUS) * 0.6)

      const t = radius / RADIUS
      const roll = Math.random()
      if (t < 0.35) mixed.copy(cCore).lerp(cBlue, t / 0.35)
      else mixed.copy(roll < 0.5 ? cBlue : cIndigo)
      if (roll < 0.1) mixed.copy(cCopper).lerp(cCore, 0.4)
      const v = 0.8 + Math.random() * 0.2

      positions[i3] = x; positions[i3 + 1] = y; positions[i3 + 2] = z
      colors[i3] = mixed.r * v; colors[i3 + 1] = mixed.g * v; colors[i3 + 2] = mixed.b * v

      // hanya layer terkecil (indeks 2) yang dianimasikan swirl -> ringan & aman
      if (layerIdx === 2) {
        starData.push({ geo: null, positions, i3, radius: radial, angle: a, y, inSpeed: 0.6 + Math.random() * 0.8 })
      }
    }
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    const mat = new THREE.PointsMaterial({
      size: layer.size, map: dotTex, alphaTest: 0.02, transparent: true,
      vertexColors: true, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true,
    })
    const points = new THREE.Points(geo, mat)
    root.add(points)
    // simpan geo ke data swirl setelah points dibuat
    if (layerIdx === 2) {
      for (const sd of starData) sd.geo = geo
    }
  })

  // ============ DUST LANES (asymmetric, opaque dark) ============
  const DUST_COUNT = 14000
  const dPos = new Float32Array(DUST_COUNT * 3)
  for (let i = 0; i < DUST_COUNT; i++) {
    const i3 = i * 3
    const t = 0.25 + Math.random() * 0.75
    const radius = t * RADIUS
    const angle = spiralAngle(i, radius) + 0.25 + gauss() * 0.3
    const scatter = () => gauss() * radius * 0.3
    dPos[i3] = Math.cos(angle) * radius + scatter()
    dPos[i3 + 1] = (Math.random() - 0.5) * 0.9
    dPos[i3 + 2] = Math.sin(angle) * radius + scatter()
  }
  const dustGeo = new THREE.BufferGeometry()
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dPos, 3))
  root.add(new THREE.Points(dustGeo, new THREE.PointsMaterial({
    size: 0.9, map: glowTex, color: new THREE.Color('#2a160c'),
    transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.NormalBlending,
  })))

  // ============ FIELD STARS ============
  const FIELD = 3000
  const fPos = new Float32Array(FIELD * 3)
  for (let i = 0; i < FIELD; i++) {
    const i3 = i * 3
    const r = 30 + Math.random() * 45
    const th = Math.random() * Math.PI * 2
    const ph = Math.acos(2 * Math.random() - 1)
    fPos[i3] = r * Math.sin(ph) * Math.cos(th)
    fPos[i3 + 1] = r * Math.cos(ph) * 0.6
    fPos[i3 + 2] = r * Math.sin(ph) * Math.sin(th)
  }
  const fGeo = new THREE.BufferGeometry()
  fGeo.setAttribute('position', new THREE.BufferAttribute(fPos, 3))
  root.add(new THREE.Points(fGeo, new THREE.PointsMaterial({
    size: 0.18, map: dotTex, color: new THREE.Color('#cfe0ff'),
    transparent: true, opacity: 0.7, depthWrite: false, blending: THREE.AdditiveBlending,
  })))

  // ============ COSMIC HAZE (randomized thickness, swirling) ============
  const hazeSprites = []
  const hazeLayers = [
    { count: 320, baseSize: 8, opacity: 0.025, tint: '#4f6bff' },
    { count: 230, baseSize: 12, opacity: 0.016, tint: '#ff7b9c' },
    { count: 160, baseSize: 19, opacity: 0.009, tint: '#7a5bff' },
  ]
  hazeLayers.forEach((layer) => {
    for (let i = 0; i < layer.count; i++) {
      const t = Math.pow(Math.random(), 0.7)
      const radius = t * RADIUS * 1.05
      const angle = spiralAngle(i, radius) * 0.92 + gauss() * 0.4
      const hc = new THREE.Color(layer.tint).lerp(new THREE.Color('#ffd9a0'), Math.random() * 0.3)
      const sizeVar = layer.baseSize * (0.4 + Math.random() * 1.6)
      const opVar = layer.opacity * (0.4 + Math.random() * 1.8)
      const mat = new THREE.SpriteMaterial({
        map: glowTex, color: hc, transparent: true, opacity: opVar,
        depthWrite: false, blending: THREE.AdditiveBlending,
      })
      const s = new THREE.Sprite(mat)
      s.position.set(Math.cos(angle) * radius, (Math.random() - 0.5) * 1.3, Math.sin(angle) * radius)
      s.scale.set(sizeVar, sizeVar * (0.5 + Math.random() * 0.8), sizeVar)
      root.add(s)
      hazeSprites.push({ sprite: s, radius, angle })
    }
  })

  // ============ SATELLITE GALAXIES ============
  addSatellite(root, { pos: [16, 3, -6], size: 3.2, tint: '#ffd9a0' })
  addSatellite(root, { pos: [-15, -4, 4], size: 4.5, tint: '#c9b6ff' })

  // ============ BULGE / CORE GLOW ============
  const coreSprites = [
    { size: 5, color: '#fff6d8', opacity: 0.98 },
    { size: 10, color: '#ffe6a0', opacity: 0.55 },
    { size: 18, color: '#ffcf7a', opacity: 0.3 },
    { size: 34, color: '#88aaff', opacity: 0.18 },
  ]
  coreSprites.forEach((c) => {
    const m = new THREE.SpriteMaterial({
      map: glowTex, color: c.color, transparent: true, opacity: c.opacity,
      depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const s = new THREE.Sprite(m); s.scale.set(c.size, c.size, c.size)
    root.add(s)
  })
  const bulge = new THREE.Sprite(new THREE.SpriteMaterial({
    map: dotTex, color: new THREE.Color('#fff8e0'), transparent: true, opacity: 1,
    depthWrite: false, blending: THREE.AdditiveBlending,
  }))
  bulge.scale.set(3.5, 3.5, 3.5)
  root.add(bulge)

  // ============ HORIZONTAL LENS FLARE ============
  const flare = new THREE.Sprite(new THREE.SpriteMaterial({
    map: makeFlareTexture(), color: new THREE.Color('#fff2c0'), transparent: true,
    opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
  }))
  flare.scale.set(60, 1.4, 1)
  root.add(flare)

  galaxy.value = root
  // expose for animation
  galaxy.value.__haze = hazeSprites
  galaxy.value.__stars = starData
})

function addSatellite(root, { pos, size, tint }) {
  const mat = new THREE.SpriteMaterial({
    map: makeGlowTexture(), color: new THREE.Color(tint), transparent: true,
    opacity: 0.5, depthWrite: false, blending: THREE.AdditiveBlending,
  })
  const s = new THREE.Sprite(mat)
  s.position.set(...pos); s.scale.set(size, size * 0.7, size)
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
  ctx.fillStyle = g; ctx.fillRect(0, 0, size, size)
  const tex = new THREE.CanvasTexture(canvas); tex.needsUpdate = true
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
  ctx.fillStyle = g; ctx.fillRect(0, 0, size, size)
  const tex = new THREE.CanvasTexture(canvas); tex.needsUpdate = true
  return tex
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
  ctx.fillStyle = g; ctx.fillRect(0, h / 2 - 2, w, 4)
  const tex = new THREE.CanvasTexture(canvas); tex.needsUpdate = true
  return tex
}

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  const g = galaxy.value
  if (!g) return
  // unified swirl: whole galaxy rotates as one (no divergence, no double image)
  g.rotation.y += delta * 0.08
})
</script>
