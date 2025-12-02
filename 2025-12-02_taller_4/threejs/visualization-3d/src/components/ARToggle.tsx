import { useState } from 'react'

/**
 * ARToggle Component - Switch between AR and 3D Visualization modes
 */

interface ARToggleProps {
  onModeChange: (isAR: boolean) => void
}

export default function ARToggle({ onModeChange }: ARToggleProps) {
  const [isARMode, setIsARMode] = useState(false)

  const handleToggle = () => {
    const newMode = !isARMode
    setIsARMode(newMode)
    onModeChange(newMode)
  }

  return (
    <div
      style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 1000,
      }}
    >
      <button
        onClick={handleToggle}
        style={{
          padding: '12px 24px',
          fontSize: '16px',
          fontWeight: 'bold',
          color: 'white',
          backgroundColor: isARMode ? '#ef4444' : '#3b82f6',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
          transition: 'all 0.3s ease',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.05)'
          e.currentTarget.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.4)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)'
          e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.3)'
        }}
      >
        {isARMode ? (
          <>
            <span>📱</span>
            <span>Modo AR Activo</span>
          </>
        ) : (
          <>
            <span>🎮</span>
            <span>Activar AR</span>
          </>
        )}
      </button>

      {isARMode && (
        <div
          style={{
            marginTop: '12px',
            padding: '12px',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            borderRadius: '8px',
            color: '#10b981',
            fontSize: '14px',
            textAlign: 'center',
            fontFamily: 'monospace',
          }}
        >
          📸 Apunta la cámara al marcador Hiro
          <div style={{ fontSize: '12px', color: '#fbbf24', marginTop: '5px' }}>
            ⚠️ Mantén el marcador visible y bien iluminado
          </div>
        </div>
      )}
    </div>
  )
}
