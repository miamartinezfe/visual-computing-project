import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useControls } from 'leva'
import * as THREE from 'three'

export function WaveShaderPlane() {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const { frequency, amplitude } = useControls('Wave Shader', {
    frequency: { value: 2.0, min: 0.5, max: 5, step: 0.1 },
    amplitude: { value: 0.5, min: 0.1, max: 2, step: 0.1 }
  })

  const shaderMaterial = useRef(
    new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uFrequency: { value: frequency },
        uAmplitude: { value: amplitude },
        uColorStart: { value: new THREE.Color('#ff6030') },
        uColorEnd: { value: new THREE.Color('#1b3984') }
      },
      vertexShader: `
        uniform float uTime;
        uniform float uFrequency;
        uniform float uAmplitude;
        
        varying vec2 vUv;
        varying float vElevation;
        
        void main() {
          vUv = uv;
          
          float elevation = sin(position.x * uFrequency + uTime) * uAmplitude;
          elevation += sin(position.y * uFrequency * 1.5 + uTime * 0.7) * uAmplitude * 0.5;
          
          vElevation = elevation;
          
          vec3 newPosition = position;
          newPosition.z += elevation;
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 uColorStart;
        uniform vec3 uColorEnd;
        
        varying vec2 vUv;
        varying float vElevation;
        
        void main() {
          float mixStrength = (vElevation + 1.0) * 0.5;
          vec3 color = mix(uColorStart, uColorEnd, mixStrength);
          
          gl_FragColor = vec4(color, 1.0);
        }
      `,
      side: THREE.DoubleSide
    })
  )

  useFrame((state) => {
    if (shaderMaterial.current) {
      shaderMaterial.current.uniforms.uTime.value = state.clock.elapsedTime
      shaderMaterial.current.uniforms.uFrequency.value = frequency
      shaderMaterial.current.uniforms.uAmplitude.value = amplitude
    }
  })

  return (
    <mesh 
      ref={meshRef} 
      position={[0, 0, 0]} 
      rotation={[-Math.PI / 3, 0, 0]}
      material={shaderMaterial.current}
    >
      <planeGeometry args={[6, 6, 128, 128]} />
    </mesh>
  )
}
