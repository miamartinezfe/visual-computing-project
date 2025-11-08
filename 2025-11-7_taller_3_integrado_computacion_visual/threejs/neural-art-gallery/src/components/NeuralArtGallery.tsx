import { OrbitControls, Environment, PerspectiveCamera } from '@react-three/drei'
import { useControls } from 'leva'
import { PBRMaterials } from './PBRMaterials'
import { WaveShaderPlane } from './WaveShaderPlane'
import { ParticleSystem } from './ParticleSystem'
import { ProceduralGeometry } from './ProceduralGeometry'
import { LightingSystem } from './LightingSystem'

export function NeuralArtGallery() {
  const { 
    cameraType,
    showPBR,
    showShader,
    showParticles,
    showProcedural,
    lightingPreset 
  } = useControls('Gallery Controls', {
    cameraType: { 
      value: 'perspective', 
      options: ['perspective', 'orthographic'],
      label: 'Camera Type'
    },
    lightingPreset: {
      value: 'studio',
      options: ['studio', 'sunset', 'night', 'dawn'],
      label: 'Lighting Preset'
    },
    showPBR: { value: true, label: 'Show PBR Materials' },
    showShader: { value: true, label: 'Show Wave Shader' },
    showParticles: { value: true, label: 'Show Particles' },
    showProcedural: { value: true, label: 'Show Procedural Geometry' }
  })

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 5, 10]} fov={50} />
      <OrbitControls 
        enableDamping 
        dampingFactor={0.05}
        minDistance={3}
        maxDistance={20}
      />

      <LightingSystem preset={lightingPreset} />
      <Environment preset={lightingPreset} background />

      {/* Floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]} receiveShadow>
        <planeGeometry args={[30, 30]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.8} />
      </mesh>

      {/* Modules */}
      {showPBR && <PBRMaterials />}
      {showShader && <WaveShaderPlane />}
      {showParticles && <ParticleSystem count={5000} />}
      {showProcedural && <ProceduralGeometry />}
    </>
  )
}
