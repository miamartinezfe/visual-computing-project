/**
 * LOD (Level of Detail) Manager Utility
 * Calculates optimal detail level based on distance from camera
 */

export interface LODLevel {
  distance: number
  segments: number
  label: string
}

/**
 * Default LOD configuration
 * - High: 0-10 units from camera (most detailed)
 * - Medium: 10-20 units from camera
 * - Low: 20+ units from camera (least detailed)
 */
export const DEFAULT_LOD_LEVELS: LODLevel[] = [
  { distance: 0, segments: 64, label: 'High' },
  { distance: 10, segments: 32, label: 'Medium' },
  { distance: 20, segments: 16, label: 'Low' },
]

/**
 * Calculate the appropriate detail level based on distance
 * @param distance - Distance from camera to object
 * @param levels - Array of LOD levels (sorted by distance ascending)
 * @returns The appropriate LOD level
 */
export function getLODLevel(distance: number, levels: LODLevel[] = DEFAULT_LOD_LEVELS): LODLevel {
  // Find the appropriate level based on distance
  for (let i = levels.length - 1; i >= 0; i--) {
    if (distance >= levels[i].distance) {
      return levels[i]
    }
  }
  
  // Fallback to highest detail
  return levels[0]
}

/**
 * Get triangle count estimate for a sphere at given LOD
 * @param segments - Number of segments
 * @returns Approximate triangle count
 */
export function getSphereTriangleCount(segments: number): number {
  return segments * segments * 2
}

/**
 * Get triangle count estimate for a box at given LOD
 * @param segments - Number of segments per side
 * @returns Approximate triangle count
 */
export function getBoxTriangleCount(segments: number): number {
  return 12 * segments * segments // 6 faces, 2 triangles per face
}

/**
 * Calculate percentage of polygons saved by using LOD
 * @param highPolyCount - Triangle count at highest detail
 * @param currentPolyCount - Triangle count at current detail
 * @returns Percentage saved (0-100)
 */
export function calculatePolygonSavings(highPolyCount: number, currentPolyCount: number): number {
  if (highPolyCount === 0) return 0
  return ((highPolyCount - currentPolyCount) / highPolyCount) * 100
}
