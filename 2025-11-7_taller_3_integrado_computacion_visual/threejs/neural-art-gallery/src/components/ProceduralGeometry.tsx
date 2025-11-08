import { useMemo } from 'react'
import * as THREE from 'three'

export function ProceduralGeometry() {
  // Generate spiral geometry
  const spiralGeometry = useMemo(() => {
    const points = []
    const turns = 3
    const pointsCount = 100
    
    for (let i = 0; i < pointsCount; i++) {
      const t = (i / pointsCount) * turns * Math.PI * 2
      const radius = t * 0.1
      const x = Math.cos(t) * radius
      const y = t * 0.1
      const z = Math.sin(t) * radius
      points.push(new THREE.Vector3(x, y, z))
    }
    
    return new THREE.BufferGeometry().setFromPoints(points)
  }, [])

  // Generate parametric torus
  const torusKnotGeometry = useMemo(() => {
    return new THREE.TorusKnotGeometry(0.8, 0.2, 100, 16, 2, 3)
  }, [])

  return (
    <group position={[0, 0, -6]}>
      {/* Spiral */}
      <line geometry={spiralGeometry}>
        <lineBasicMaterial color="#ff6b6b" linewidth={2} />
      </line>

      {/* Torus Knot */}
      <mesh position={[2, 1, 0]} rotation={[0, 0, 0]} castShadow>
        <primitive object={torusKnotGeometry} />
        <meshStandardMaterial 
          color="#4ecdc4" 
          roughness={0.3} 
          metalness={0.7}
          wireframe={false}
        />
      </mesh>

      {/* Icosahedron */}
      <mesh position={[-2, 1, 0]} castShadow>
        <icosahedronGeometry args={[1, 1]} />
        <meshStandardMaterial 
          color="#45b7d1" 
          roughness={0.2} 
          metalness={0.9}
        />
      </mesh>
    </group>
  )
}
