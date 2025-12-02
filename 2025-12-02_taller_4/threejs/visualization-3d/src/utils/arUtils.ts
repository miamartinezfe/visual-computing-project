/**
 * AR.js Utilities - Helper functions for AR marker generation and management
 */

export interface MarkerPattern {
  name: string
  path: string
  description: string
  complexity: 'simple' | 'medium' | 'complex'
}

/**
 * Available AR markers in the project
 */
export const AVAILABLE_MARKERS: MarkerPattern[] = [
  {
    name: 'Hiro',
    path: '/markers/hiro.patt',
    description: 'Classic Hiro marker - recommended for testing',
    complexity: 'simple',
  },
  {
    name: 'Kanji',
    path: '/markers/kanji.patt',
    description: 'Kanji character marker',
    complexity: 'medium',
  },
  {
    name: 'Custom',
    path: '/markers/custom.patt',
    description: 'Custom pattern marker',
    complexity: 'complex',
  },
]

/**
 * Get marker by name
 */
export function getMarkerByName(name: string): MarkerPattern | undefined {
  return AVAILABLE_MARKERS.find(
    (marker) => marker.name.toLowerCase() === name.toLowerCase()
  )
}

/**
 * Check if AR.js is loaded
 */
export function isARjsLoaded(): boolean {
  return typeof window !== 'undefined' && !!(window as any).THREEx
}

/**
 * Request camera permissions (for mobile)
 */
export async function requestCameraPermission(): Promise<boolean> {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' },
      audio: false,
    })
    
    // Stop stream immediately, we just needed to check permission
    stream.getTracks().forEach((track) => track.stop())
    
    return true
  } catch (error) {
    console.error('Camera permission denied:', error)
    return false
  }
}

/**
 * Generate marker pattern data (simplified version)
 * For production, use AR.js marker training tools
 */
export function generateMarkerData(size: number = 16): string {
  const data: number[][] = []
  
  for (let i = 0; i < size; i++) {
    const row: number[] = []
    for (let j = 0; j < size; j++) {
      // Create a simple pattern (border + center square)
      const isBorder = i < 2 || i >= size - 2 || j < 2 || j >= size - 2
      const isCenter = i >= size / 2 - 2 && i < size / 2 + 2 && 
                       j >= size / 2 - 2 && j < size / 2 + 2
      
      row.push(isBorder || isCenter ? 0 : 255)
    }
    data.push(row)
  }
  
  // Convert to AR.js pattern format (3 channels RGB)
  let pattern = ''
  
  for (let channel = 0; channel < 3; channel++) {
    for (let i = 0; i < size; i++) {
      pattern += data[i].join(' ') + '\n'
    }
    pattern += '\n'
  }
  
  return pattern
}

/**
 * Download marker pattern as .patt file
 */
export function downloadMarkerPattern(
  patternData: string,
  filename: string = 'custom-marker.patt'
) {
  const blob = new Blob([patternData], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  
  URL.revokeObjectURL(url)
}

/**
 * AR.js configuration defaults
 */
export const AR_CONFIG = {
  source: {
    sourceType: 'webcam',
    sourceWidth: window.innerWidth,
    sourceHeight: window.innerHeight,
  },
  context: {
    cameraParametersUrl: '/data/camera_para.dat',
    detectionMode: 'mono',
    maxDetectionRate: 60,
  },
  marker: {
    type: 'pattern',
    minConfidence: 0.5,
    smooth: true,
    smoothCount: 5,
    smoothTolerance: 0.01,
  },
}
