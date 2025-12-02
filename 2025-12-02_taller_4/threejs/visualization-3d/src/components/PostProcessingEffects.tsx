import { EffectComposer, Bloom, SSAO, Vignette, HueSaturation, BrightnessContrast } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'
import { useState } from 'react'

/**
 * PostProcessingEffects Component
 * Implementa efectos visuales avanzados con control de rendimiento
 * - Bloom: Resplandor en objetos brillantes
 * - SSAO: Ambient Occlusion para sombras realistas
 * - Vignette: Oscurecimiento en bordes
 * - Color Correction: Ajustes de color y contraste
 */

interface PostProcessingProps {
  enabled?: boolean
}

export default function PostProcessingEffects({ enabled = true }: PostProcessingProps) {
  if (!enabled) return null

  return (
    <EffectComposer multisampling={0}>
      {/* Bloom Effect - Resplandor para materiales emisivos */}
      <Bloom
        intensity={0.5} // Intensidad del resplandor
        luminanceThreshold={0.8} // Umbral de luminancia (solo objetos brillantes)
        luminanceSmoothing={0.9} // Suavizado de transición
        radius={0.8} // Radio del efecto
        blendFunction={BlendFunction.SCREEN} // Modo de mezcla
      />

      {/* SSAO - Screen Space Ambient Occlusion */}
      <SSAO
        intensity={20} // Intensidad de la oclusión
        radius={0.5} // Radio de búsqueda
        luminanceInfluence={0.5} // Influencia de la luminosidad
        samples={16} // Número de samples (más = mejor calidad, menos FPS)
        rings={4} // Anillos de sampling
        distanceThreshold={0.5} // Umbral de distancia
        distanceFalloff={0.5} // Caída de distancia
        rangeThreshold={0.001} // Umbral de rango
        rangeFalloff={0.001} // Caída de rango
        minRadiusScale={0.5} // Escala mínima de radio
        bias={0.5} // Sesgo para evitar acné
        blendFunction={BlendFunction.MULTIPLY}
      />

      {/* Vignette Effect - Oscurecimiento en bordes */}
      <Vignette
        offset={0.3} // Distancia desde el centro donde inicia
        darkness={0.5} // Intensidad del oscurecimiento
        eskil={false} // Usar técnica Eskil (alternativa)
        blendFunction={BlendFunction.NORMAL}
      />

      {/* Color Correction - Ajuste de tono y saturación */}
      <HueSaturation
        hue={0} // Rotación de tono (-180 a 180)
        saturation={0.1} // Ajuste de saturación (-1 a 1)
        blendFunction={BlendFunction.NORMAL}
      />

      {/* Brightness & Contrast */}
      <BrightnessContrast
        brightness={0} // Ajuste de brillo (-1 a 1)
        contrast={0.05} // Ajuste de contraste (-1 a 1)
        blendFunction={BlendFunction.NORMAL}
      />
    </EffectComposer>
  )
}

// Componente de control para activar/desactivar effects
export function PostProcessingToggle({ 
  onChange 
}: { 
  onChange: (enabled: boolean) => void 
}) {
  const [enabled, setEnabled] = useState(true)

  const toggle = () => {
    const newState = !enabled
    setEnabled(newState)
    onChange(newState)
  }

  return (
    <div style={{
      position: 'fixed',
      top: '140px',
      right: '20px',
      background: 'rgba(0, 0, 0, 0.8)',
      color: 'white',
      padding: '15px',
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '14px',
      zIndex: 1000,
      cursor: 'pointer',
      userSelect: 'none',
      border: '2px solid rgba(255, 255, 255, 0.2)',
    }} onClick={toggle}>
      <div style={{ marginBottom: '8px', fontWeight: 'bold' }}>
        ✨ POST-PROCESSING
      </div>
      <div style={{ 
        color: enabled ? '#10b981' : '#ef4444',
        fontSize: '12px'
      }}>
        {enabled ? '● ENABLED' : '○ DISABLED'}
      </div>
      <div style={{ 
        fontSize: '11px', 
        color: '#9ca3af',
        marginTop: '8px'
      }}>
        {enabled && (
          <>
            <div>+ Bloom</div>
            <div>+ SSAO</div>
            <div>+ Vignette</div>
            <div>+ Color Correction</div>
          </>
        )}
      </div>
    </div>
  )
}
