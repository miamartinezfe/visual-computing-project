import { useState } from 'react'
import './App.css'
import Scene from './components/Scene'
import ARToggle from './components/ARToggle'

function App() {
  const [isARMode, setIsARMode] = useState(false)

  const handleModeChange = (newARMode: boolean) => {
    // Clean up video before changing modes
    if (!newARMode && isARMode) {
      // Hide and remove all video elements immediately
      const videos = document.querySelectorAll('video')
      videos.forEach(v => {
        // Hide immediately
        v.style.display = 'none'
        v.style.visibility = 'hidden'
        v.style.opacity = '0'
        
        // Stop media streams
        if (v.srcObject) {
          const tracks = (v.srcObject as MediaStream).getTracks()
          tracks.forEach(track => {
            track.stop()
            console.log('🛑 Track stopped:', track.kind)
          })
          v.srcObject = null
        }
        
        // Pause video
        v.pause()
        
        // Remove from DOM
        if (v.parentElement) {
          v.parentElement.removeChild(v)
          console.log('🗑️ Video removed from DOM')
        }
      })
      
      console.log('✅ Video cleanup complete, total videos removed:', videos.length)
    }
    
    setIsARMode(newARMode)
  }

  return (
    <div className="app">
      <Scene isARMode={isARMode} />
      <ARToggle onModeChange={handleModeChange} />
    </div>
  )
}

export default App
