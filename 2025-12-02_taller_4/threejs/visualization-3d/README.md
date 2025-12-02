# Visualization 3D - Optimized Three.js Scene

## 🎯 Objective

This module implements an **optimized 3D visualization system** using React Three Fiber, with performance monitoring, dynamic overlays, and AR.js integration. It's part of the Taller 4 specialized subsystem approach.

## 🛠️ Tech Stack

- **React 18.3** - UI framework
- **Three.js r168** - 3D graphics engine
- **React Three Fiber 8.15** - React renderer for Three.js
- **Drei 9.114** - Helper components for R3F
- **Stats.js 0.17** - Performance monitoring
- **TypeScript 5.6** - Type safety
- **Vite 5.4** - Build tool

## 📦 Installation

```bash
npm install
```

## 🚀 Development

Start the development server:

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🏗️ Project Structure

```
src/
├── components/
│   ├── Scene.tsx                 # Main 3D scene
│   ├── LightingOptimized.tsx     # Optimized lighting system
│   ├── PerformanceMonitor.tsx    # FPS & metrics monitoring
│   ├── DynamicOverlay.tsx        # HUD overlay
│   └── OptimizedModels.tsx       # LOD system (coming soon)
├── ar/
│   └── ARScene.tsx               # AR.js integration (coming soon)
├── utils/
│   ├── lodManager.ts             # Level of Detail manager
│   └── performanceMetrics.ts    # Performance tracking utilities
├── App.tsx                       # Root component
└── main.tsx                      # Entry point
```

## ⚡ Optimizations Implemented

### ✅ Completed

1. **Optimized Lighting**
   - Shadow map size reduced to 1024x1024
   - Limited shadow distance (far: 20)
   - Reduced number of shadow-casting lights

2. **Performance Monitoring**
   - Real-time FPS tracking with Stats.js
   - Renderer info logging (geometries, textures, draw calls)
   - Memory usage monitoring

3. **Adaptive Rendering**
   - Dynamic pixel ratio [1, 2]
   - High-performance GPU preference
   - Efficient camera controls with damping

4. **Dynamic HUD**
   - Real-time scene information
   - Performance metrics display
   - Interactive overlay system

### 🚧 In Progress

5. **LOD System** (Level of Detail)
   - 3 detail levels based on distance
   - Automatic switching for performance

6. **Texture Compression**
   - Basis Universal format
   - KTX2 GPU compression
   - Mipmaps optimization

7. **AR.js Integration**
   - Custom marker tracking
   - 3D model placement
   - Mobile-optimized rendering

## 📊 Performance Metrics

Current performance targets:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| FPS | 60 | ~60 | ✅ |
| Draw Calls | <100 | ~8 | ✅ |
| Triangles | <100k | ~2k | ✅ |
| Shadow Map | 1024² | 1024² | ✅ |

## 🎮 Controls

- **Left Mouse**: Orbit camera
- **Right Mouse**: Pan camera
- **Scroll**: Zoom in/out
- **Stats Panel**: Top-left corner shows FPS

## 📝 Next Steps

- [ ] Implement LOD system with multiple detail levels
- [ ] Add texture compression pipeline
- [ ] Integrate AR.js with custom markers
- [ ] Create complex 3D models for demonstration
- [ ] Implement post-processing effects
- [ ] Add performance comparison charts
- [ ] Generate screenshots and GIFs for documentation

## 🧪 Testing

To test the scene:

1. Start the dev server: `npm run dev`
2. Open browser console to see renderer info logs
3. Check FPS counter in top-left corner
4. Interact with the scene (orbit, zoom, pan)

## 📚 Documentation

- [Three.js Docs](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Drei Components](https://github.com/pmndrs/drei)
- [AR.js Documentation](https://ar-js-org.github.io/AR.js-Docs/)

## 👥 Team

**Subsystem 3: 3D Visualization**
- Responsible for optimized rendering, AR integration, and visual performance

---

**Status**: 🟡 In Development (Base scene completed, LOD & AR pending)
