import { Canvas } from '@react-three/fiber'
import { OrbitControls, Grid, Environment } from '@react-three/drei'
import { Suspense, useState } from 'react'
import LightingOptimized from './LightingOptimized.tsx'
import PerformanceMonitor from './PerformanceMonitor.tsx'
import DynamicOverlay from './DynamicOverlay.tsx'
import OptimizedModels from './OptimizedModels.tsx'
import LODMetrics from './LODMetrics.tsx'
import ARScene from '../ar/ARScene.tsx'
import ComplexModelsScene from './ComplexModelsLOD.tsx'
import PostProcessingEffects, { PostProcessingToggle } from './PostProcessingEffects.tsx'

/**
 * Main 3D scene component with optimized rendering and AR support
 * Implements performance monitoring, optimized lighting, and AR.js integration
 */

interface SceneProps {
  isARMode?: boolean
}

export default function Scene({ isARMode = false }: SceneProps) {
  const [postProcessingEnabled, setPostProcessingEnabled] = useState(true)

  return (
    <>
      <Canvas
        shadows={!isARMode}
        camera={{ position: isARMode ? [0, 0, 0] : [5, 5, 5], fov: 50 }}
        gl={{
          antialias: true,
          powerPreference: 'high-performance',
          alpha: isARMode, // Transparent only in AR
        }}
        dpr={[1, 2]} // Adaptive pixel ratio for performance
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: isARMode ? 'transparent' : '#000', // Black in 3D mode
          zIndex: isARMode ? 10 : 1,
          pointerEvents: 'auto',
        }}
      >
        <Suspense fallback={null}>
          {isARMode ? (
            /* AR Mode */
            <>
              <ARScene
                onMarkerFound={(id) => console.log(`Marker ${id} found`)}
                onMarkerLost={(id) => console.log(`Marker ${id} lost`)}
              />
              <ambientLight intensity={0.5} />
              <directionalLight position={[5, 5, 5]} intensity={0.8} />
            </>
          ) : (
            /* 3D Visualization Mode */
            <>
              {/* Performance monitoring - MUST be inside Canvas */}
              <PerformanceMonitor />
              <LODMetrics />

              {/* Environment and lighting */}
              <Environment preset="city" />
              <LightingOptimized />

              {/* Grid helper */}
              <Grid
                args={[30, 30]}
                cellSize={0.5}
                cellThickness={0.5}
                cellColor="#6b7280"
                sectionSize={2}
                sectionThickness={1}
                sectionColor="#374151"
                fadeDistance={30}
                fadeStrength={1}
                infiniteGrid
              />

              {/* LOD Optimized Models */}
              <OptimizedModels />

              {/* Complex 3D Models with PBR Materials */}
              <ComplexModelsScene />

              {/* Ground plane */}
              <mesh receiveShadow rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
                <planeGeometry args={[50, 50]} />
                <meshStandardMaterial 
                    color={"rgb(31, 41, 55)"} 
                    roughness={0.8} 
                    metalness={0.2} 
                    // Optimizaciones adicionales:
                    shadowSide={2} // DoubleSide para sombras
                    toneMapped={false} // Mejor performance
                />
              </mesh>

              {/* Camera controls */}
              <OrbitControls
                makeDefault
                minDistance={2}
                maxDistance={30}
                enableDamping
                dampingFactor={0.05}
                maxPolarAngle={Math.PI / 2.1}
              />

              {/* Post-Processing Effects */}
              <PostProcessingEffects enabled={postProcessingEnabled} />
            </>
          )}
        </Suspense>
      </Canvas>

      {/* Post-Processing Toggle - only in 3D mode */}
      {!isARMode && (
        <PostProcessingToggle onChange={setPostProcessingEnabled} />
      )}

      {/* Dynamic HUD overlay - OUTSIDE Canvas, only in 3D mode */}
      {!isARMode && <DynamicOverlay />}
    </>
  )

}
