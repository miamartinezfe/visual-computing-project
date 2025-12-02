import { WebGLRenderer } from 'three'

/**
 * Performance metrics tracking utilities
 */

export interface PerformanceMetrics {
  fps: number
  frameTime: number
  triangles: number
  drawCalls: number
  geometries: number
  textures: number
  timestamp: number
}

export interface PerformanceSnapshot {
  before: PerformanceMetrics
  after: PerformanceMetrics
  improvement: {
    fpsGain: number
    trianglesReduced: number
    drawCallsReduced: number
  }
}

/**
 * Create a performance metrics snapshot
 */
export function createMetricsSnapshot(
  gl: WebGLRenderer,
  fps: number,
  frameTime: number
): PerformanceMetrics {
  const info = gl.info
  
  return {
    fps,
    frameTime,
    triangles: info.render.triangles,
    drawCalls: info.render.calls,
    geometries: info.memory.geometries,
    textures: info.memory.textures,
    timestamp: Date.now(),
  }
}

/**
 * Calculate improvement between two performance snapshots
 */
export function calculateImprovement(
  before: PerformanceMetrics,
  after: PerformanceMetrics
): PerformanceSnapshot['improvement'] {
  return {
    fpsGain: after.fps - before.fps,
    trianglesReduced: before.triangles - after.triangles,
    drawCallsReduced: before.drawCalls - after.drawCalls,
  }
}

/**
 * Format metrics for display
 */
export function formatMetrics(metrics: PerformanceMetrics): string {
  return `FPS: ${metrics.fps.toFixed(0)} | Triangles: ${metrics.triangles.toLocaleString()} | Draw Calls: ${metrics.drawCalls}`
}
