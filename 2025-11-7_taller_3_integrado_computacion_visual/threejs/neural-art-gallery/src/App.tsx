import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'
import { NeuralArtGallery } from './components/NeuralArtGallery'
import { VoiceStatus } from './components/VoiceStatus'
import './App.css'

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <VoiceStatus />
      <Canvas shadows camera={{ position: [0, 5, 10], fov: 50 }}>
        <Suspense fallback={null}>
          <NeuralArtGallery />
        </Suspense>
      </Canvas>
    </div>
  )
}

export default App
