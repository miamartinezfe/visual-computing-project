import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface ParticleSystemProps {
  count?: number
}

export function ParticleSystem({ count = 5000 }: ParticleSystemProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  
  const particles = useMemo(() => {
    const temp = []
    for (let i = 0; i < count; i++) {
      const t = Math.random() * 100
      const factor = 10 + Math.random() * 50
      const speed = 0.01 + Math.random() / 200
      const x = Math.random() * 10 - 5
      const y = Math.random() * 10 - 5
      const z = Math.random() * 10 - 5
      
      temp.push({ t, factor, speed, x, y, z })
    }
    return temp
  }, [count])

  const dummy = useMemo(() => new THREE.Object3D(), [])
  const colorArray = useMemo(() => {
    const colors = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const color = new THREE.Color()
      color.setHSL(Math.random(), 0.7, 0.5)
      colors[i * 3] = color.r
      colors[i * 3 + 1] = color.g
      colors[i * 3 + 2] = color.b
    }
    return colors
  }, [count])

  useFrame(() => {
    if (!meshRef.current) return
    
    particles.forEach((particle, i) => {
      let { t, factor, speed, x, y, z } = particle
      
      t = particle.t += speed / 2
      const a = Math.cos(t) + Math.sin(t * 1) / 10
      const b = Math.sin(t) + Math.cos(t * 2) / 10
      
      dummy.position.set(
        x + Math.cos((t / 10) * factor) + (Math.sin(t * 1) * factor) / 10,
        y + Math.sin((t / 10) * factor) + (Math.cos(t * 2) * factor) / 10,
        z + Math.cos((t / 10) * factor) + (Math.sin(t * 3) * factor) / 10
      )
      
      const scale = 0.5 + Math.sin(t * 2) * 0.2
      dummy.scale.set(scale, scale, scale)
      dummy.rotation.set(a * 2, b * 2, 0)
      dummy.updateMatrix()
      
      meshRef.current!.setMatrixAt(i, dummy.matrix)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]} position={[4, 2, 0]}>
      <dodecahedronGeometry args={[0.1, 0]}>
        <instancedBufferAttribute
          attach="attributes-color"
          args={[colorArray, 3]}
        />
      </dodecahedronGeometry>
      <meshPhongMaterial vertexColors />
    </instancedMesh>
  )
}
