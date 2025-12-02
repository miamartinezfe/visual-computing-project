import { useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Text } from '@react-three/drei'
import { Mesh } from 'three'
import { getLODLevel, DEFAULT_LOD_LEVELS, getSphereTriangleCount } from '../utils/lodManager'

interface LODSphereProps {
  position: [number, number, number]
  color: string
}

/**
 * LOD Sphere component that changes detail based on camera distance
 */
function LODSphere({ position, color }: LODSphereProps) {
  const meshRef = useRef<Mesh>(null)
  const [currentLOD, setCurrentLOD] = useState(DEFAULT_LOD_LEVELS[0])
  const [distance, setDistance] = useState(0)
  const { camera } = useThree()

  useFrame(() => {
    if (!meshRef.current) return

    // Calculate distance from camera to object
    const dist = camera.position.distanceTo(meshRef.current.position)
    setDistance(dist)

    // Get appropriate LOD level
    const lodLevel = getLODLevel(dist)
    
    // Update LOD if it changed
    if (lodLevel.segments !== currentLOD.segments) {
      setCurrentLOD(lodLevel)
    }
  })

  const triangleCount = getSphereTriangleCount(currentLOD.segments)

  return (
    <group position={position}>
      <mesh ref={meshRef} castShadow receiveShadow>
        <sphereGeometry args={[0.5, currentLOD.segments, currentLOD.segments]} />
        <meshStandardMaterial 
          color={color as any} 
          roughness={0.3} 
          metalness={0.7}
        />
      </mesh>
      
      {/* LOD info label */}
      <Text
        position={[0, 1, 0]}
        fontSize={0.15}
        color="white"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {`LOD: ${currentLOD.label}\n${currentLOD.segments}×${currentLOD.segments}\n${triangleCount} tris\n${distance.toFixed(1)}m`}
      </Text>
    </group>
  )
}

interface LODBoxProps {
  position: [number, number, number]
  color: string
}

/**
 * LOD Box component with dynamic detail levels
 */
function LODBox({ position, color }: LODBoxProps) {
  const meshRef = useRef<Mesh>(null)
  const [currentLOD, setCurrentLOD] = useState(DEFAULT_LOD_LEVELS[0])
  const [distance, setDistance] = useState(0)
  const { camera } = useThree()

  useFrame(() => {
    if (!meshRef.current) return

    const dist = camera.position.distanceTo(meshRef.current.position)
    setDistance(dist)

    const lodLevel = getLODLevel(dist)
    
    if (lodLevel.segments !== currentLOD.segments) {
      setCurrentLOD(lodLevel)
    }
  })

  const segs = Math.max(1, Math.floor(currentLOD.segments / 16)) // Scale down for box

  return (
    <group position={position}>
      <mesh ref={meshRef} castShadow receiveShadow>
        <boxGeometry args={[1, 1, 1, segs, segs, segs]} />
        <meshStandardMaterial 
          color={color as any} 
          roughness={0.4} 
          metalness={0.6}
        />
      </mesh>
      
      <Text
        position={[0, 1, 0]}
        fontSize={0.15}
        color="white"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {`LOD: ${currentLOD.label}\n${segs}×${segs}×${segs}\n${distance.toFixed(1)}m`}
      </Text>
    </group>
  )
}

/**
 * Main component demonstrating LOD system with multiple objects
 * Objects automatically reduce detail as camera moves away
 */
export default function OptimizedModels() {
  // Create a grid of spheres at different positions
  const spherePositions: Array<{ pos: [number, number, number], color: string }> = [
    { pos: [0, 0.5, 0], color: '#3b82f6' },      // Center - Blue
    { pos: [3, 0.5, 0], color: '#ef4444' },      // Right - Red
    { pos: [-3, 0.5, 0], color: '#10b981' },     // Left - Green
    { pos: [0, 0.5, 3], color: '#f59e0b' },      // Back - Orange
    { pos: [0, 0.5, -3], color: '#8b5cf6' },     // Front - Purple
    { pos: [3, 0.5, 3], color: '#ec4899' },      // Back-Right - Pink
    { pos: [-3, 0.5, 3], color: '#06b6d4' },     // Back-Left - Cyan
    { pos: [3, 0.5, -3], color: '#eab308' },     // Front-Right - Yellow
    { pos: [-3, 0.5, -3], color: '#14b8a6' },    // Front-Left - Teal
  ]

  const boxPositions: Array<{ pos: [number, number, number], color: string }> = [
    { pos: [6, 0.5, 0], color: '#f97316' },
    { pos: [-6, 0.5, 0], color: '#84cc16' },
    { pos: [0, 0.5, 6], color: '#06b6d4' },
  ]

  return (
    <group>
      {/* Render LOD Spheres */}
      {spherePositions.map((item, index) => (
        <LODSphere
          key={`sphere-${index}`}
          position={item.pos}
          color={item.color}
        />
      ))}

      {/* Render LOD Boxes */}
      {boxPositions.map((item, index) => (
        <LODBox
          key={`box-${index}`}
          position={item.pos}
          color={item.color}
        />
      ))}

      {/* Information panel */}
      <Text
        position={[0, 3, 0]}
        fontSize={0.3}
        color="#60a5fa"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.03}
        outlineColor="#000000"
      >
        LOD SYSTEM ACTIVE
      </Text>

      <Text
        position={[0, 2.5, 0]}
        fontSize={0.15}
        color="white"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {`Move camera to see detail levels change\nHigh: 0-10m | Medium: 10-20m | Low: 20m+`}
      </Text>
    </group>
  )
}
