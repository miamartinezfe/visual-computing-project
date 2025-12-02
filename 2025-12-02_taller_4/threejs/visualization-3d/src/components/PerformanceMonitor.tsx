import { useEffect, useRef } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import Stats from 'stats.js'

/**
 * Performance monitoring component using Stats.js
 * Displays FPS, MS, and memory usage in real-time
 * MUST be rendered inside <Canvas> component
 */
export default function PerformanceMonitor() {
  const statsRef = useRef<Stats | null>(null)
  const { gl } = useThree()

  useEffect(() => {
    // Initialize Stats.js
    const stats = new Stats()
    stats.showPanel(0) // 0: fps, 1: ms, 2: mb
    
    // Style the stats panel
    stats.dom.style.position = 'absolute'
    stats.dom.style.left = '0px'
    stats.dom.style.top = '0px'
    stats.dom.style.zIndex = '1000'
    
    document.body.appendChild(stats.dom)
    statsRef.current = stats

    // Cleanup
    return () => {
      if (statsRef.current && document.body.contains(statsRef.current.dom)) {
        document.body.removeChild(statsRef.current.dom)
      }
    }
  }, [])

  // Update stats every frame
  useFrame(() => {
    if (statsRef.current) {
      statsRef.current.update()
    }
  })

  // Log renderer info periodically
  useEffect(() => {
    const interval = setInterval(() => {
      const info = gl.info
      console.log('📊 Renderer Info:', {
        geometries: info.memory.geometries,
        textures: info.memory.textures,
        calls: info.render.calls,
        triangles: info.render.triangles,
        points: info.render.points,
        lines: info.render.lines,
      })
    }, 5000) // Log every 5 seconds

    return () => clearInterval(interval)
  }, [gl])

  return null // This component doesn't render anything in the 3D scene
}
