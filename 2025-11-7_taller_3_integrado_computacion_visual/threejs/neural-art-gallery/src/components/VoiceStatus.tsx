import { useState, useEffect } from 'react'

export function VoiceStatus() {
  const [listening, setListening] = useState(false)
  const [command, setCommand] = useState<string>('')

  useEffect(() => {
    // Simular reconocimiento de voz (placeholder)
    // En producción, usar Web Speech API
    const simulateCommands = ['Change color', 'Rotate left', 'Zoom in', 'Reset camera']
    
    const interval = setInterval(() => {
      if (Math.random() > 0.7) {
        const randomCommand = simulateCommands[Math.floor(Math.random() * simulateCommands.length)]
        setCommand(randomCommand)
        setListening(true)
        
        setTimeout(() => {
          setListening(false)
        }, 2000)
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{
      position: 'absolute',
      top: 20,
      right: 20,
      zIndex: 1000,
      background: 'rgba(0, 0, 0, 0.8)',
      color: 'white',
      padding: '15px 20px',
      borderRadius: '10px',
      fontFamily: 'monospace',
      minWidth: '200px'
    }}>
      <h3 style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
        🎤 Voice Control
      </h3>
      <div style={{ fontSize: '12px' }}>
        Status: <span style={{ 
          color: listening ? '#4ecdc4' : '#ff6b6b',
          fontWeight: 'bold'
        }}>
          {listening ? 'LISTENING' : 'IDLE'}
        </span>
      </div>
      {command && (
        <div style={{ 
          marginTop: '8px', 
          fontSize: '11px',
          color: '#4ecdc4'
        }}>
          Last: "{command}"
        </div>
      )}
      <div style={{ 
        marginTop: '12px', 
        fontSize: '10px',
        color: '#888',
        borderTop: '1px solid #333',
        paddingTop: '8px'
      }}>
        <div>• "change color"</div>
        <div>• "rotate left/right"</div>
        <div>• "zoom in/out"</div>
        <div>• "reset camera"</div>
      </div>
    </div>
  )
}
