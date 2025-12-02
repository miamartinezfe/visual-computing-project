import { useEffect, useRef, useState } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { Html } from '@react-three/drei'
import * as THREE from 'three'

/**
 * ARScene Component - REAL AR.js Integration with Camera
 * Handles marker detection and AR camera initialization
 */

interface ARSceneProps {
  onMarkerFound?: (markerId: string) => void
  onMarkerLost?: (markerId: string) => void
}

export default function ARScene({ onMarkerFound, onMarkerLost }: ARSceneProps) {
  const { gl, scene, camera } = useThree()
  const [isARReady, setIsARReady] = useState(false)
  const [markerVisible, setMarkerVisible] = useState(false)
  const arToolkitSourceRef = useRef<any>(null)
  const arToolkitContextRef = useRef<any>(null)
  const markerRootRef = useRef<THREE.Group | null>(null)
  const videoElementRef = useRef<HTMLVideoElement | null>(null)

  useEffect(() => {
    // Check if AR.js is loaded
    if (typeof window === 'undefined' || !(window as any).THREEx) {
      console.error('❌ AR.js no está cargado. Verifica los scripts en index.html')
      return
    }

    const THREEx = (window as any).THREEx
    let markerControls: any = null

    // Initialize AR.js Source (webcam)
    arToolkitSourceRef.current = new THREEx.ArToolkitSource({
      sourceType: 'webcam',
    })

    const onSourceReady = () => {
      console.log('✅ Cámara inicializada')
      
      // AR.js creates the video automatically - just ensure it's visible
      const findAndShowVideo = () => {
        // Find ALL video elements
        const videos = document.querySelectorAll('video')
        console.log('Videos found:', videos.length)
        
        videos.forEach((video, index) => {
          console.log(`Video ${index}:`, {
            parent: video.parentElement?.tagName,
            width: video.videoWidth,
            height: video.videoHeight,
            paused: video.paused,
            srcObject: !!video.srcObject
          })
          
          // Store reference to the video element
          if (!videoElementRef.current) {
            videoElementRef.current = video
          }
          
          // Make sure the video is visible
          video.style.cssText = `
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            object-fit: cover !important;
            z-index: 1 !important;
          `
          video.play().catch(e => console.log('Play error:', e))
        })
      }
      
      setTimeout(findAndShowVideo, 100)
      setTimeout(findAndShowVideo, 500)
      
      onResize()
    }

    arToolkitSourceRef.current.init(onSourceReady, (error: any) => {
      console.error('❌ Error al inicializar cámara:', error)
      alert('No se pudo acceder a la cámara. Verifica los permisos.')
    })

    // Initialize AR.js Context
    arToolkitContextRef.current = new THREEx.ArToolkitContext({
      cameraParametersUrl: '/data/camera_para.dat',
      detectionMode: 'mono',
    })

    arToolkitContextRef.current.init(() => {
      // Copy projection matrix from AR.js to Three.js camera
      camera.projectionMatrix.copy(arToolkitContextRef.current.getProjectionMatrix())
      console.log('✅ AR Context inicializado')
      
      // Hide AR.js canvas
      if (arToolkitContextRef.current.arController?.canvas) {
        arToolkitContextRef.current.arController.canvas.style.display = 'none'
      }
      
      setIsARReady(true)
    })

    // Create marker root group
    const markerRoot = new THREE.Group()
    markerRoot.visible = false // Hide until marker is detected
    scene.add(markerRoot)
    markerRootRef.current = markerRoot

    // Setup marker controls for Hiro marker
    markerControls = new THREEx.ArMarkerControls(
      arToolkitContextRef.current,
      markerRoot,
      {
        type: 'pattern',
        patternUrl: '/markers/hiro.patt',
        changeMatrixMode: 'cameraTransformMatrix',
        smooth: true,
        smoothCount: 10,
        smoothTolerance: 0.01,
        smoothThreshold: 2,
      }
    )

    // Marker detection events with stability counter
    let markerFoundCount = 0
    let markerLostCount = 0
    const checkMarkerVisibility = setInterval(() => {
      if (markerRoot.visible) {
        markerFoundCount++
        markerLostCount = 0
        if (markerFoundCount >= 2 && !markerVisible) { // Detected for 2 consecutive frames
          console.log('✅ Marcador Hiro detectado! markerRoot.visible:', markerRoot.visible)
          console.log('markerRoot children:', markerRoot.children.length)
          setMarkerVisible(true)
          onMarkerFound?.('hiro')
        }
      } else {
        markerLostCount++
        markerFoundCount = 0
        if (markerLostCount >= 15 && markerVisible) { // Lost for 15 frames (1.5 seconds)
          console.log('❌ Marcador Hiro perdido')
          setMarkerVisible(false)
          onMarkerLost?.('hiro')
        }
      }
    }, 100)

    // Handle window resize
    function onResize() {
      if (arToolkitSourceRef.current?.ready) {
        arToolkitSourceRef.current.onResizeElement()
        arToolkitSourceRef.current.copyElementSizeTo(gl.domElement)
        
        if (arToolkitContextRef.current?.arController) {
          arToolkitSourceRef.current.copyElementSizeTo(
            arToolkitContextRef.current.arController.canvas
          )
        }
      }
    }

    window.addEventListener('resize', onResize)

    // Cleanup
    return () => {
      clearInterval(checkMarkerVisibility)
      window.removeEventListener('resize', onResize)
      
      if (markerRootRef.current) {
        scene.remove(markerRootRef.current)
      }
      
      // Hide and stop all video elements IMMEDIATELY
      const hideAllVideos = () => {
        const videos = document.querySelectorAll('video')
        videos.forEach(v => {
          // Hide immediately
          v.style.display = 'none'
          v.style.visibility = 'hidden'
          
          // Stop streams
          if (v.srcObject) {
            const tracks = (v.srcObject as MediaStream).getTracks()
            tracks.forEach(track => track.stop())
            v.srcObject = null
          }
          
          // Remove from DOM
          if (v.parentElement) {
            v.parentElement.removeChild(v)
          }
        })
      }
      
      // Execute immediately
      hideAllVideos()
      
      // Execute again after a short delay to catch any late videos
      setTimeout(hideAllVideos, 10)
      
      // Stop video stream from AR.js source
      if (arToolkitSourceRef.current?.domElement) {
        const video = arToolkitSourceRef.current.domElement
        video.style.display = 'none'
        if (video.srcObject) {
          const tracks = (video.srcObject as MediaStream).getTracks()
          tracks.forEach(track => track.stop())
        }
      }
      
      // Clear video reference
      if (videoElementRef.current) {
        videoElementRef.current.style.display = 'none';
        videoElementRef.current = null;
      }
    }
  }, [gl, scene, camera, onMarkerFound, onMarkerLost, markerVisible])

  // Add objects directly to markerRoot when marker becomes visible
  useEffect(() => {
    if (!markerRootRef.current || !isARReady) return
    
    console.log('markerVisible changed to:', markerVisible, 'markerRoot children:', markerRootRef.current.children.length)
    
    // Clear existing objects
    while (markerRootRef.current.children.length > 0) {
      markerRootRef.current.remove(markerRootRef.current.children[0])
    }
    
    if (markerVisible) {
      // Add objects using Three.js directly
      const cube = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.MeshBasicMaterial({ color: 0x00ffff })
      )
      cube.position.set(0, 0.75, 0)
      markerRootRef.current.add(cube)
      
      const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(0.5, 32, 32),
        new THREE.MeshBasicMaterial({ color: 0xff0000 })
      )
      sphere.position.set(1.5, 0.75, 0)
      markerRootRef.current.add(sphere)
      
      const torus = new THREE.Mesh(
        new THREE.TorusGeometry(0.5, 0.2, 16, 32),
        new THREE.MeshBasicMaterial({ color: 0x00ff00 })
      )
      torus.position.set(-1.5, 0.75, 0)
      torus.rotation.x = Math.PI / 2
      markerRootRef.current.add(torus)
      
      const cone = new THREE.Mesh(
        new THREE.ConeGeometry(0.4, 1, 32),
        new THREE.MeshBasicMaterial({ color: 0xffff00 })
      )
      cone.position.set(0, 1.5, -1)
      markerRootRef.current.add(cone)
      
      const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(3, 3),
        new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5 })
      )
      plane.rotation.x = -Math.PI / 2
      markerRootRef.current.add(plane)
      
      console.log('✅ Objects added! Total children:', markerRootRef.current.children.length)
    }
  }, [markerVisible, isARReady])

  // Update AR tracking every frame
  useFrame(() => {
    if (
      arToolkitSourceRef.current?.ready &&
      arToolkitContextRef.current &&
      isARReady
    ) {
      arToolkitContextRef.current.update(arToolkitSourceRef.current.domElement)
    }
  })

  return (
    <>
      {/* AR Status Indicator */}
      <Html position={[0, 0, -3]} center>
        <div style={{
          background: markerVisible ? 'rgba(16, 185, 129, 0.9)' : 'rgba(245, 158, 11, 0.9)',
          color: 'white',
          padding: '12px 24px',
          borderRadius: '12px',
          fontSize: '18px',
          fontWeight: 'bold',
          whiteSpace: 'nowrap',
          pointerEvents: 'none',
          boxShadow: '0 4px 6px rgba(0,0,0,0.3)',
          border: '2px solid white',
        }}>
          {isARReady ? (
            markerVisible ? '✅ Marcador Detectado!' : '🔍 Apunta al marcador Hiro'
          ) : (
            '⏳ Inicializando cámara...'
          )}
        </div>
      </Html>
      
      {/* Simple light for any objects */}
      <ambientLight intensity={2} />
    </>
  )
}
