import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * ComplexModels Component - Modelos 3D complejos con materiales PBR
 * Implementa geometría procedural avanzada con texturas y materiales realistas
 */

// Robot procedural con PBR materials
export function Robot({ position = [0, 0, 0] }: { position?: [number, number, number] }) {
  const groupRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    if (groupRef.current) {
      // Animación de balanceo sutil
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1
    }
  })

  return (
    <group ref={groupRef} position={position}>
      {/* Cuerpo */}
      <mesh position={[0, 1.5, 0]} castShadow>
        <boxGeometry args={[1, 1.5, 0.8]} />
        <meshStandardMaterial
          color="#4a5568"
          metalness={0.8}
          roughness={0.2}
          envMapIntensity={1.5}
        />
      </mesh>

      {/* Cabeza */}
      <mesh position={[0, 2.6, 0]} castShadow>
        <boxGeometry args={[0.8, 0.8, 0.8]} />
        <meshStandardMaterial
          color="#2d3748"
          metalness={0.9}
          roughness={0.1}
          emissive="#3b82f6"
          emissiveIntensity={0.2}
        />
      </mesh>

      {/* Ojos (emisivos) */}
      <mesh position={[-0.2, 2.6, 0.41]}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshBasicMaterial color="#00ffff" />
      </mesh>
      <mesh position={[0.2, 2.6, 0.41]}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshBasicMaterial color="#00ffff" />
      </mesh>

      {/* Brazos */}
      <mesh position={[-0.7, 1.3, 0]} castShadow>
        <boxGeometry args={[0.3, 1, 0.3]} />
        <meshStandardMaterial
          color="#4a5568"
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>
      <mesh position={[0.7, 1.3, 0]} castShadow>
        <boxGeometry args={[0.3, 1, 0.3]} />
        <meshStandardMaterial
          color="#4a5568"
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>

      {/* Piernas */}
      <mesh position={[-0.3, 0.4, 0]} castShadow>
        <boxGeometry args={[0.3, 0.8, 0.3]} />
        <meshStandardMaterial
          color="#2d3748"
          metalness={0.6}
          roughness={0.4}
        />
      </mesh>
      <mesh position={[0.3, 0.4, 0]} castShadow>
        <boxGeometry args={[0.3, 0.8, 0.3]} />
        <meshStandardMaterial
          color="#2d3748"
          metalness={0.6}
          roughness={0.4}
        />
      </mesh>
    </group>
  )
}

// Árbol procedural estilizado
export function Tree({ position = [0, 0, 0] }: { position?: [number, number, number] }) {
  return (
    <group position={position}>
      {/* Tronco */}
      <mesh position={[0, 1, 0]} castShadow>
        <cylinderGeometry args={[0.3, 0.4, 2, 8]} />
        <meshStandardMaterial
          color="#8b4513"
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>

      {/* Copa del árbol - nivel inferior */}
      <mesh position={[0, 2.5, 0]} castShadow>
        <coneGeometry args={[1.5, 2, 8]} />
        <meshStandardMaterial
          color="#2d5016"
          roughness={0.8}
          metalness={0}
        />
      </mesh>

      {/* Copa del árbol - nivel medio */}
      <mesh position={[0, 3.5, 0]} castShadow>
        <coneGeometry args={[1.2, 1.5, 8]} />
        <meshStandardMaterial
          color="#3a6622"
          roughness={0.8}
          metalness={0}
        />
      </mesh>

      {/* Copa del árbol - nivel superior */}
      <mesh position={[0, 4.3, 0]} castShadow>
        <coneGeometry args={[0.8, 1, 8]} />
        <meshStandardMaterial
          color="#4a7c2e"
          roughness={0.8}
          metalness={0}
        />
      </mesh>
    </group>
  )
}

// Nave espacial con materiales metálicos
export function Spaceship({ position = [0, 0, 0] }: { position?: [number, number, number] }) {
  const groupRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    if (groupRef.current) {
      // Rotación lenta
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.3
      // Hover effect
      groupRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 2) * 0.1
    }
  })

  return (
    <group ref={groupRef} position={position}>
      {/* Cuerpo principal */}
      <mesh castShadow>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          color="#e5e7eb"
          metalness={0.95}
          roughness={0.1}
          envMapIntensity={2}
        />
      </mesh>

      {/* Cabina */}
      <mesh position={[0, 0.6, 0]} castShadow>
        <sphereGeometry args={[0.5, 32, 32, 0, Math.PI * 2, 0, Math.PI / 2]} />
        <meshStandardMaterial
          color="#3b82f6"
          metalness={0.1}
          roughness={0.1}
          transparent
          opacity={0.8}
          emissive="#3b82f6"
          emissiveIntensity={0.3}
        />
      </mesh>

      {/* Alas */}
      <mesh position={[-1.5, 0, 0]} rotation={[0, 0, Math.PI / 6]} castShadow>
        <boxGeometry args={[1, 0.1, 0.5]} />
        <meshStandardMaterial
          color="#dc2626"
          metalness={0.9}
          roughness={0.2}
        />
      </mesh>
      <mesh position={[1.5, 0, 0]} rotation={[0, 0, -Math.PI / 6]} castShadow>
        <boxGeometry args={[1, 0.1, 0.5]} />
        <meshStandardMaterial
          color="#dc2626"
          metalness={0.9}
          roughness={0.2}
        />
      </mesh>

      {/* Motores */}
      <mesh position={[-1, -0.4, -0.3]}>
        <cylinderGeometry args={[0.15, 0.2, 0.6, 8]} />
        <meshStandardMaterial
          color="#1e293b"
          metalness={0.8}
          roughness={0.3}
          emissive="#ef4444"
          emissiveIntensity={0.5}
        />
      </mesh>
      <mesh position={[1, -0.4, -0.3]}>
        <cylinderGeometry args={[0.15, 0.2, 0.6, 8]} />
        <meshStandardMaterial
          color="#1e293b"
          metalness={0.8}
          roughness={0.3}
          emissive="#ef4444"
          emissiveIntensity={0.5}
        />
      </mesh>

      {/* Efecto de llama de motores */}
      <pointLight position={[-1, -0.7, -0.3]} color="#ff6b00" intensity={2} distance={3} />
      <pointLight position={[1, -0.7, -0.3]} color="#ff6b00" intensity={2} distance={3} />
    </group>
  )
}

// Cristal decorativo con refracción
export function Crystal({ position = [0, 0, 0] }: { position?: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.5
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2
    }
  })

  return (
    <mesh ref={meshRef} position={position} castShadow>
      <octahedronGeometry args={[0.8, 0]} />
      <meshStandardMaterial
        color="#a78bfa"
        metalness={0.1}
        roughness={0.1}
        transparent
        opacity={0.9}
        emissive="#8b5cf6"
        emissiveIntensity={0.4}
        envMapIntensity={2}
      />
    </mesh>
  )
}
