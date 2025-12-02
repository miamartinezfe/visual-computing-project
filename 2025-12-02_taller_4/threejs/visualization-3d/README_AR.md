# AR.js Integration - Taller 4 Visualización 3D

## 🎯 Integración Completada

Se ha integrado AR.js con React Three Fiber para permitir la visualización de modelos 3D sobre marcadores AR en tiempo real.

## 📁 Archivos Creados

### 1. **ARScene.tsx** (`src/ar/ARScene.tsx`)
- Componente principal de AR que inicializa la cámara y el contexto AR.js
- Detecta marcadores Hiro automáticamente
- Emite eventos cuando se encuentra/pierde un marcador
- Renderiza objetos 3D sobre el marcador detectado

### 2. **ARToggle.tsx** (`src/components/ARToggle.tsx`)
- Botón flotante para alternar entre modo AR y visualización 3D
- Indicador visual del estado actual
- Instrucciones al usuario cuando AR está activo

### 3. **arUtils.ts** (`src/utils/arUtils.ts`)
- Utilidades para manejo de marcadores AR
- Funciones de permisos de cámara
- Generador de patrones de marcadores
- Configuración default de AR.js

### 4. **hiro.patt** (`public/markers/hiro.patt`)
- Patrón de marcador Hiro (predeterminado de AR.js)
- Listo para imprimir y usar

## 🔧 Modificaciones Realizadas

### **index.html**
```html
<!-- AR.js Dependencies agregadas -->
<script src="https://cdn.jsdelivr.net/gh/aframevr/aframe@1c2407b26c61958baa93967b5412487cd94b290b/dist/aframe-master.min.js"></script>
<script src="https://raw.githack.com/AR-js-org/AR.js/master/aframe/build/aframe-ar-nft.js"></script>
<script src="https://raw.githack.com/AR-js-org/AR.js/master/three.js/build/ar-threex.js"></script>
```

### **Scene.tsx**
- Añadido soporte para modo AR con prop `isARMode`
- Cámara se posiciona en [0,0,0] para AR
- Background transparente en modo AR
- Renderizado condicional: AR vs 3D normal

### **App.tsx**
- Estado global para controlar modo AR
- Integración de ARToggle component
- Pasa `isARMode` a Scene

## 🚀 Cómo Usar

### **Modo 3D Normal**
1. Abre la aplicación en el navegador
2. Interactúa con la escena usando OrbitControls
3. Visualiza métricas LOD en tiempo real

### **Modo AR**
1. Haz clic en el botón **"Activar AR"**
2. Permite acceso a la cámara cuando el navegador lo solicite
3. Imprime el marcador Hiro (disponible en `public/markers/hiro.patt`)
4. Apunta la cámara al marcador
5. Los objetos 3D aparecerán sobre el marcador

## 📱 Requisitos para AR

### **Desktop**
- Navegador con soporte WebRTC (Chrome, Firefox, Edge)
- Cámara web conectada
- HTTPS o localhost

### **Mobile**
- Android: Chrome, Firefox
- iOS: Safari (iOS 11+)
- Cámara trasera del dispositivo
- HTTPS obligatorio (excepto localhost)

## 🎨 Marcadores Disponibles

| Marcador | Archivo | Complejidad | Estado |
|----------|---------|-------------|--------|
| Hiro | `hiro.patt` | Simple | ✅ Disponible |
| Kanji | `kanji.patt` | Media | ⏳ Pendiente |
| Custom | `custom.patt` | Alta | ⏳ Pendiente |

## 🔄 Flujo de Trabajo

```
Usuario → Clic "Activar AR" 
       → Permisos cámara 
       → ARScene inicializa 
       → Detecta marcador 
       → Renderiza modelo 3D
```

## ⚙️ Configuración AR.js

```typescript
// En arUtils.ts
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
```

## 🐛 Debugging

### **Si no detecta marcador:**
1. Verifica que el marcador esté bien iluminado
2. Mantén el marcador plano (sin arrugas)
3. Distancia recomendada: 20-50cm
4. Asegúrate de que todo el marcador sea visible

### **Si la cámara no funciona:**
1. Verifica permisos del navegador
2. Asegúrate de estar en HTTPS o localhost
3. Revisa la consola del navegador por errores
4. Prueba con otro navegador/dispositivo

## 📊 Métricas AR

El sistema AR.js está optimizado para:
- **Detección**: 60 FPS máximo
- **Smoothing**: 5 frames para estabilidad
- **Confidence**: >0.5 para detección válida

## 🎓 Próximos Pasos

1. ✅ Integración AR.js completada
2. ⏳ Generar marcadores adicionales (Kanji, Custom)
3. ⏳ Documentación final con screenshots
4. ⏳ GIFs demostrativos de uso

---

**Autor**: Subsistema 3 - Visualización 3D con AR.js  
**Fecha**: Diciembre 2025  
**Taller**: Taller 4 - Computación Visual
