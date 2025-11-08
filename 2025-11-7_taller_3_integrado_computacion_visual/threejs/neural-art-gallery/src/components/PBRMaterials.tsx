import { useControls } from 'leva'

export function PBRMaterials() {
  const { roughness, metalness, color } = useControls('PBR Materials', {
    roughness: { value: 0.5, min: 0, max: 1, step: 0.01 },
    metalness: { value: 0.8, min: 0, max: 1, step: 0.01 },
    color: { value: '#ff6030' }
  })

  return (
    <group position={[-4, 0, 0]}>
      {/* Sphere - High Metalness */}
      <mesh position={[0, 0, 0]} castShadow>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial
          color={color}
          roughness={roughness}
          metalness={metalness}
          envMapIntensity={1.5}
        />
      </mesh>

      {/* Box - Medium Roughness */}
      <mesh position={[0, 0, -3]} castShadow>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <meshStandardMaterial
          color="#4ecdc4"
          roughness={roughness * 0.5}
          metalness={metalness * 0.6}
        />
      </mesh>

      {/* Torus - Low Metalness */}
      <mesh position={[0, 0, 3]} rotation={[Math.PI / 4, 0, 0]} castShadow>
        <torusGeometry args={[0.8, 0.3, 32, 64]} />
        <meshStandardMaterial
          color="#45b7d1"
          roughness={roughness * 1.2}
          metalness={metalness * 0.3}
        />
      </mesh>
    </group>
  )
}
