<template>
  <!-- Ambient wireframe sphere for depth -->
  <TresGroup ref="ambientRef">
    <TresMesh>
      <TresIcosahedronGeometry :args="[22, 1]" />
      <TresMeshBasicMaterial color="#00dc82" :wireframe="true" :transparent="true" :opacity="0.07" />
    </TresMesh>
  </TresGroup>

  <!-- The 3D model (OBJ), placed on the right -->
  <TresGroup :position="[0, -2, 0]" ref="modelGroup" />
</template>

<script setup>
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js'
import { useLoop } from '@tresjs/core'
import { Box3, Vector3, DoubleSide, MeshStandardMaterial } from 'three'
import { shallowRef, ref } from 'vue'

// Ganti ke '/models/orbiter bugship.obj' jika mau model kapal luar angkasa
const MODEL_URL = '/models/caiman-character.obj'

const modelGroup = shallowRef()
const ambientRef = shallowRef()

const loader = new OBJLoader()
loader.load(
  MODEL_URL,
  (obj) => {
    // Center & uniformly scale the model to a consistent size
    const box = new Box3().setFromObject(obj)
    const size = box.getSize(new Vector3())
    const center = box.getCenter(new Vector3())
    const maxDim = Math.max(size.x, size.y, size.z) || 1
    const computedScale = 18 / maxDim
    
    // Scale and center the object directly in Three.js
    obj.scale.set(computedScale, computedScale, computedScale)
    obj.position.set(-center.x * computedScale, -center.y * computedScale, -center.z * computedScale)

    // Make sure faces render even if the OBJ lacks proper normals/material setup
    const defaultMaterial = new MeshStandardMaterial({
      color: 0xffffff, 
      emissive: 0x00dc82, // Subtle brand color glow from inside
      emissiveIntensity: 0.15,
      roughness: 0.15, // Glossy finish
      metalness: 0.7, // High-tech metallic reflection
      side: DoubleSide,
    })

    obj.traverse((child) => {
      if (child.isMesh) {
        if (!child.geometry.attributes.normal) {
          child.geometry.computeVertexNormals()
        }
        child.material = defaultMaterial
      }
    })

    // Mount to the group directly using raw Three.js API
    if (modelGroup.value) {
      modelGroup.value.clear()
      modelGroup.value.add(obj)
      console.log('[HeroSceneModel] OBJ successfully mounted to scene!')
    }
  },
  (xhr) => {
    console.log(`[HeroSceneModel] ${(xhr.loaded / xhr.total * 100)}% loaded`)
  },
  (err) => {
    console.error('[HeroSceneModel] OBJ load error:', err)
  }
)

const { onBeforeRender } = useLoop()
onBeforeRender(({ delta }) => {
  if (modelGroup.value) modelGroup.value.rotation.y += delta * 0.25
  if (ambientRef.value) ambientRef.value.rotation.y -= delta * 0.04
})
</script>
