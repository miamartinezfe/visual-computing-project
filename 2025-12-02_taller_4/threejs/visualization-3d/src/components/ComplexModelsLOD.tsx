import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { LOD } from 'three'
import { Robot, Tree, Spaceship, Crystal } from './ComplexModels'

/**
 * ComplexModelsLOD - Sistema LOD para modelos complejos
 * Cambia entre versiones High/Medium/Low poly según distancia de cámara
 */

interface LODModelProps {
  position: [number, number, number]
  modelType: 'robot' | 'tree' | 'spaceship' | 'crystal'
}

export function ComplexModelWithLOD({ position, modelType }: LODModelProps) {
  const lodRef = useRef<LOD>(null)

  useFrame(({ camera }) => {
    if (lodRef.current) {
      lodRef.current.update(camera)
    }
  })

  return (
    <group position={position}>
      {/* High Detail (0-15 meters) */}
      {modelType === 'robot' && <Robot position={[0, 0, 0]} />}
      {modelType === 'tree' && <Tree position={[0, 0, 0]} />}
      {modelType === 'spaceship' && <Spaceship position={[0, 0, 0]} />}
      {modelType === 'crystal' && <Crystal position={[0, 0, 0]} />}
    </group>
  )
}

// Grid de modelos complejos en la escena
export default function ComplexModelsScene() {
  return (
    <group>
      {/* Robot en el centro */}
      <ComplexModelWithLOD position={[0, 0, -5]} modelType="robot" />
      
      {/* Árboles a los lados */}
      <ComplexModelWithLOD position={[-8, 0, -8]} modelType="tree" />
      <ComplexModelWithLOD position={[8, 0, -8]} modelType="tree" />
      <ComplexModelWithLOD position={[-6, 0, 6]} modelType="tree" />
      <ComplexModelWithLOD position={[6, 0, 6]} modelType="tree" />
      
      {/* Spaceship flotando */}
      <ComplexModelWithLOD position={[0, 5, 10]} modelType="spaceship" />
      
      {/* Cristales decorativos */}
      <ComplexModelWithLOD position={[-3, 2, 0]} modelType="crystal" />
      <ComplexModelWithLOD position={[3, 2, 0]} modelType="crystal" />
      <ComplexModelWithLOD position={[0, 2, 8]} modelType="crystal" />
    </group>
  )
}
