/**
 * Optimized lighting system with controlled shadow quality
 * Reduces performance impact while maintaining visual quality
 */
export default function LightingOptimized() {
  return (
    <>
      {/* Ambient light for base illumination */}
      <ambientLight intensity={0.3} />

      {/* Main directional light with optimized shadows */}
      <directionalLight
        castShadow
        position={[5, 8, 5]}
        intensity={1}
        shadow-mapSize={[1024, 1024]} // Reduced from 2048 for performance
        shadow-camera-far={20} // Limited shadow distance
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
        shadow-bias={-0.0001}
      />

      {/* Fill light to soften shadows */}
      <directionalLight
        position={[-5, 5, -5]}
        intensity={0.3}
        color="#60a5fa"
      />

      {/* Accent light from below */}
      <pointLight
        position={[0, 2, 0]}
        intensity={0.5}
        color="#fbbf24"
        distance={10}
      />
    </>
  )
}
