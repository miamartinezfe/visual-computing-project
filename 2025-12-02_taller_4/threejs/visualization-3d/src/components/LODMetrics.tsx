import { useEffect, useState } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { Mesh, Object3D } from 'three'

interface LODMetrics {
  totalTriangles: number
  highDetailCount: number
  mediumDetailCount: number
  lowDetailCount: number
  averageDistance: number
  polygonSavings: number
}

/**
 * LOD Metrics component - tracks and displays LOD system performance
 * Must be rendered inside Canvas
 */
export default function LODMetrics() {
  const { scene, camera } = useThree()
  const [metrics, setMetrics] = useState<LODMetrics>({
    totalTriangles: 0,
    highDetailCount: 0,
    mediumDetailCount: 0,
    lowDetailCount: 0,
    averageDistance: 0,
    polygonSavings: 0,
  })

  useFrame(() => {
    let totalTris = 0
    let high = 0
    let medium = 0
    let low = 0
    let totalDistance = 0
    let objectCount = 0

    scene.traverse((object: Object3D) => {
      if (object.type === 'Mesh') {
        const mesh = object as Mesh
        const geometry = mesh.geometry
        
        if (geometry) {
          // Count triangles
          const positions = geometry.attributes.position
          if (positions) {
            const triangles = positions.count / 3
            totalTris += triangles

            // Calculate distance from camera
            const distance = camera.position.distanceTo(mesh.position)
            totalDistance += distance
            objectCount++

            // Categorize by LOD level based on segment count
            if (triangles > 6000) high++ // ~64x64 segments
            else if (triangles > 1500) medium++ // ~32x32 segments
            else low++ // ~16x16 segments
          }
        }
      }
    })

    const avgDistance = objectCount > 0 ? totalDistance / objectCount : 0
    
    // Calculate theoretical max triangles if all were high detail
    const maxTriangles = (high + medium + low) * 8192 // Max for 64x64 sphere
    const savings = maxTriangles > 0 ? ((maxTriangles - totalTris) / maxTriangles) * 100 : 0

    setMetrics({
      totalTriangles: Math.floor(totalTris),
      highDetailCount: high,
      mediumDetailCount: medium,
      lowDetailCount: low,
      averageDistance: avgDistance,
      polygonSavings: savings,
    })
  })

  // Update DOM overlay every second
  useEffect(() => {
    const updateOverlay = () => {
      const overlay = document.getElementById('lod-metrics-overlay')
      if (overlay) {
        overlay.innerHTML = `
          <div style="font-family: monospace; color: #10b981; font-size: 12px; line-height: 1.6;">
            <strong style="color: #3b82f6;">🔧 LOD METRICS</strong><br/>
            Total Triangles: <strong>${metrics.totalTriangles.toLocaleString()}</strong><br/>
            High Detail: <strong style="color: #10b981;">${metrics.highDetailCount}</strong> objects<br/>
            Medium Detail: <strong style="color: #f59e0b;">${metrics.mediumDetailCount}</strong> objects<br/>
            Low Detail: <strong style="color: #ef4444;">${metrics.lowDetailCount}</strong> objects<br/>
            Avg Distance: <strong>${metrics.averageDistance.toFixed(1)}m</strong><br/>
            Polygon Savings: <strong style="color: #10b981;">${metrics.polygonSavings.toFixed(1)}%</strong>
          </div>
        `
      }
    }

    const interval = setInterval(updateOverlay, 100)
    return () => clearInterval(interval)
  }, [metrics])

  return null
}
