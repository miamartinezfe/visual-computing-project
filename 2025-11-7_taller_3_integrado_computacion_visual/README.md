# Taller 3 — Taller Integral de Computación Visual
**Fecha:** 2025-11-07  
**Integrantes:** Javier Giraldo, Miguel Martinez

---

## Descripción general

Este taller integral busca **diseñar y curar experiencias visuales interactivas** que integren diferentes componentes del pipeline gráfico y sensorial.  
Los ejercicios combinan modelado 3D, materiales PBR, shaders personalizados, texturas dinámicas, interacción multimodal (voz, gestos, EEG) y control de cámara o entorno.

El objetivo es conectar percepción visual, física de la luz, geometría procedural y comunicación humano–máquina, consolidando las habilidades de integración entre arte, código y percepción.

---

## Actividades desarrolladas

### 1. Materiales, luz y color (PBR y modelos cromáticos)
- Implementación de texturas PBR (albedo, roughness, metalness, normal map).
- Iluminación múltiple (key, fill, rim, HDRI).
- Cámaras: alternancia entre perspectiva y ortográfica.
- Paletas RGB/HSV y contraste en CIELAB.
- Animaciones demostrando variaciones de luz y material.

### 2. Modelado procedural desde código
- Generación algorítmica de geometría (rejillas, espirales, fractales simples).
- Uso de bucles y recursión para patrones espaciales.
- Transformaciones dinámicas de vértices.
- Comparativa entre modelado por código y manual.

### 3. Shaders personalizados y efectos
- Implementación de shaders básicos (GLSL, HLSL, Shader Graph).
- Color dinámico por posición, tiempo o interacción.
- Efectos de toon shading, wireframe, distorsión UV y gradientes.
- Texturizado procedural y mezcla de mapas dinámicos.

### 4. Texturizado dinámico y partículas
- Materiales reactivos a tiempo o entradas del usuario.
- Mapas animados: emissive, normal, offset UV, ruido procedural.
- Integración de sistemas de partículas sincronizados con shaders.
- Evento visual coordinado shader + partículas.

### 5. Visualización de imágenes y video 360°
- Implementación de skybox o esfera invertida para escenas 360°.
- Uso de video equirectangular como textura dinámica.
- Conmutación entre panoramas o escenas.
- Control de cámara (orbit, giroscopio, entrada de usuario).

### 6. Entrada e interacción (UI, input y colisiones)
- Captura de teclado, mouse y touch.
- Uso de UI Canvas o HTML para interacción visual.
- Colisiones físicas o triggers que disparan efectos.
- Sincronización de eventos visuales con acciones del usuario.

### 7. Gestos con cámara web (MediaPipe Hands)
- Detección de manos en tiempo real con MediaPipe + OpenCV.
- Conteo de dedos, detección de gestos y distancias.
- Mapeo de gestos a acciones visuales.
- Implementación de minijuego o interfaz gestual.

### 8. Reconocimiento de voz y control por comandos
- Captura de audio con SpeechRecognition/PyAudio.
- Reconocimiento local o online.
- Diccionario de comandos y acciones visuales.
- Integración con Unity o Processing mediante OSC.
- Retroalimentación auditiva con pyttsx3.

### 9. Interfaces multimodales (voz + gestos)
- Integración simultánea de voz y gestos.
- Sincronización de hilos y eventos.
- Lógica condicional para acciones combinadas.
- Interfaz visual reactiva con retroalimentación.

### 10. Simulación BCI (EEG sintético y control)
- Generación de señales EEG sintéticas (bandas Alpha/Beta).
- Filtros pasa banda y umbrales de activación.
- Control visual a partir de variaciones EEG.
- Interfaz interactiva con PyGame o Tkinter.

### 11. Espacios proyectivos y matrices de proyección
- Uso de coordenadas homogéneas y proyecciones.
- Implementación de matrices ortográficas y perspectiva.
- Visualización de profundidad y alternancia de cámaras.

---

## Herramientas utilizadas
- **Unity (versión LTS)**
- **Three.js / React Three Fiber**
- **Python (Colab o local)**
- **Processing (2D/3D)**
- **Librerías y complementos:** MediaPipe, SpeechRecognition, OSC, OpenCV, PyGame, Tkinter.

---

## Resultados esperados
- 6 capturas de escenas distintas.
- 6 GIFs mostrando interacción y shaders dinámicos.
- 1 video (30–60 s) de la experiencia completa.
- Código ejecutable y documentado.

---

## Criterios de evaluación

| Criterio                                | Descripción                                   | Peso |
| --------------------------------------- | --------------------------------------------- | ---- |
| Organización                            | Estructura de carpetas y README claros        | 10%  |
| Modelado y geometría procedural         | Generación y coherencia de formas             | 10%  |
| Materiales e iluminación PBR            | Realismo, coherencia y respuesta a la luz     | 15%  |
| Shaders y texturizado dinámico          | Efectos visuales y complejidad técnica        | 15%  |
| Interacción multimodal (voz/gestos/EEG) | Integración funcional y creativa              | 15%  |
| Cámaras y proyección                    | Uso correcto de perspectiva/orto y movimiento | 10%  |
| Animaciones y partículas                | Movimiento expresivo, sincronización visual   | 10%  |
| Evidencias visuales                     | GIFs, videos y capturas claras                | 10%  |
| Código y documentación                  | Claridad, comentarios y commits en inglés     | 5%   |
| **Total**                               |                                               | **100%** |

---

## Contribuciones Grupales

- **Miguel Martinez** — Organizacion repositorio inicial - Materiales e iluminación PBR - Shaders y texturizado dinámico

---

## Reflexión final

Este taller integra todos los componentes explorados durante el curso, conectando **percepción, interacción y visualización avanzada**.  
El trabajo consolida una comprensión práctica del pipeline gráfico moderno, resaltando la importancia del diseño sensorial, la respuesta visual coherente y la documentación técnica reproducible.

---

## Estructura del repositorio

```plaintext
2025-10-17_taller_3_integrado_computacion_visual/
├── unity/           # Escenas y materiales PBR
├── threejs/         # Experimentos WebGL / R3F
├── python/          # Scripts de procesamiento o EEG
├── processing/      # Sketches visuales 2D/3D
├── renders/         # Capturas y GIFs
├── media/           # Videos o audios usados
└── README.md