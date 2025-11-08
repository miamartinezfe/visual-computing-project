import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface LightingSystemProps {
  preset: string
}

export function LightingSystem({ preset }: LightingSystemProps) {
  const keyLightRef = useRef<THREE.DirectionalLight>(null)
  
  const presets: Record<string, { 
    keyPos: [number, number, number]
    keyColor: string
    intensity: number 
  }> = {
    studio: { 
      keyPos: [5, 8, 5], 
      keyColor: '#ffffff', 
      intensity: 1.5 
    },
    sunset: { 
      keyPos: [10, 3, -5], 
      keyColor: '#ff9966', 
      intensity: 1.8 
    },
    night: { 
      keyPos: [2, 10, 2], 
      keyColor: '#6699ff', 
      intensity: 1.0 
    },
    dawn: {
      keyPos: [8, 4, 8],
      keyColor: '#ffccaa',
      intensity: 1.3
    }
  }

  const current = presets[preset] || presets.studio

  // Animate key light
  useFrame((state) => {
    if (keyLightRef.current) {
      const t = state.clock.elapsedTime * 0.3
      keyLightRef.current.position.x = Math.cos(t) * 8
      keyLightRef.current.position.z = Math.sin(t) * 8
    }
  })

  return (
    <>
      {/* Key Light */}
      <directionalLight
        ref={keyLightRef}
        position={current.keyPos}
        intensity={current.intensity}
        color={current.keyColor}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-far={50}
        shadow-camera-left={-15}
        shadow-camera-right={15}
        shadow-camera-top={15}
        shadow-camera-bottom={-15}
      />

      {/* Fill Light */}
      <directionalLight
        position={[-5, 5, -5]}
        intensity={0.5}
        color="#b3d9ff"
      />

      {/* Rim Light */}
      <directionalLight
        position={[0, 8, -10]}
        intensity={0.8}
        color="#ffffff"
      />

      {/* Ambient Light */}
      <ambientLight intensity={0.2} />

      {/* Hemisphere Light for sky effect */}
      <hemisphereLight
        intensity={0.3}
        color="#ffffff"
        groundColor="#444444"
      />
    </>
  )
}
