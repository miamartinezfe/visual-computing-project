import { useState, useEffect } from 'react'

/**
 * Dynamic HUD overlay with performance metrics and controls
 * Displays real-time information about the 3D scene
 */
export default function DynamicOverlay() {
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      pointerEvents: 'none',
      zIndex: 100,
    }}>
      {/* Top Left - Title and Info */}
      <div style={{
        position: 'absolute',
        top: '70px', // Below Stats.js panel
        left: '20px',
      }}>
        {/* Title */}
        <div style={{
          fontFamily: 'monospace',
          color: '#fff',
          fontSize: '24px',
          fontWeight: 'bold',
          textShadow: '0 2px 4px rgba(0,0,0,0.5)',
          marginBottom: '10px',
        }}>
          Optimized 3D Visualization
        </div>

        {/* Info panel */}
        <div style={{
          fontFamily: 'monospace',
          color: '#60a5fa',
          fontSize: '14px',
          background: 'rgba(0,0,0,0.7)',
          padding: '10px 15px',
          borderRadius: '8px',
          backdropFilter: 'blur(10px)',
        }}>
          <div>🎯 Scene: LOD System Active</div>
          <div>⚡ Mode: Performance Optimized</div>
          <div>🕐 Time: {time.toLocaleTimeString()}</div>
          <div style={{ marginTop: '8px', color: '#10b981' }}>
            ▸ Use mouse to orbit • Scroll to zoom
          </div>
          <div style={{ marginTop: '4px', color: '#f59e0b', fontSize: '12px' }}>
            ⚠️ Zoom out to see LOD levels change
          </div>
        </div>
      </div>

      {/* Top Right - LOD Info Box */}
      <div style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        fontFamily: 'monospace',
        color: '#fff',
        fontSize: '13px',
        background: 'rgba(59, 130, 246, 0.15)',
        border: '2px solid #3b82f6',
        padding: '12px 16px',
        borderRadius: '10px',
        backdropFilter: 'blur(10px)',
        minWidth: '220px',
      }}>
        <div style={{ color: '#3b82f6', fontWeight: 'bold', marginBottom: '8px' }}>
          📊 LOD LEVELS
        </div>
        <div style={{ fontSize: '11px', lineHeight: '1.6' }}>
          <div style={{ color: '#10b981' }}>● High: 0-10m (64×64 segments)</div>
          <div style={{ color: '#f59e0b' }}>● Medium: 10-20m (32×32 segments)</div>
          <div style={{ color: '#ef4444' }}>● Low: 20m+ (16×16 segments)</div>
        </div>
        <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid rgba(59, 130, 246, 0.3)', fontSize: '11px', color: '#9ca3af' }}>
          Triangles reduced by ~75% at low LOD
        </div>
      </div>

      {/* Bottom Left - Project Info */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        fontFamily: 'monospace',
        color: '#9ca3af',
        fontSize: '12px',
        background: 'rgba(0,0,0,0.6)',
        padding: '8px 12px',
        borderRadius: '6px',
      }}>
        Taller 4 - Visualización 3D | Three.js + React Three Fiber
      </div>

      {/* Bottom Right - LOD Metrics Overlay (populated by LODMetrics component) */}
      <div
        id="lod-metrics-overlay"
        style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          fontFamily: 'monospace',
          background: 'rgba(0,0,0,0.8)',
          padding: '12px 16px',
          borderRadius: '8px',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(59, 130, 246, 0.3)',
        }}
      >
        Loading metrics...
      </div>
    </div>
  )
}
