# Taller 3 — Taller Integral de Computación Visual
**Fecha:** 2025-11-07  
**Integrantes:** Javier Giraldo, Miguel Martinez, Brayan Rubiano

---

# Subproyecto: Geometría Procedural, Shaders y Espacios Proyectivos

## Estructura

```
2025-11-07_taller_3_integrado_computacion_visual/
├── renders/                 #Generated GIFs & Images.
├── unity/
    ├── T3_Int_Sec_2_3_11/   #Folder with Unity Scene objects and structure
        ├── Assets/
           ├── Materials/    #Procedural Material.
           ├── Scripts/      #Game Object procedural behaviour gen & Camera Projection Switch. 
           ├── Shaders/      #HLSL Custom Procedural Shader.
├── README.md                #You are here man.            
```

#### Implementación: Brayan Rubiano
## IMPORTANTE: [Enlace implementación subproyecto completa](https://github.com/brubianop/VisualComputingUN2025II/tree/main/2025-11-07_Taller_3_Integrado)     
Este documento describe la implementación de técnicas de gráficos por computadora en Unity (Universal Render Pipeline, URP), enfocándose en la generación de geometría dinámica y shaders procedurales.

![Procedural Wave](./renders/T3_Procedural_Shaders_Projections.gif)

![Procedural Wave](./renders/T3_ProceduralWave_Perspective.png)

![Procedural Wave](./renders/T3_ProceduralWave_Orthographic.png)

---

## 1. Introducción

El objetivo de este proyecto es demostrar las capacidades de la **Generación Procedural en CPU** (C#) y el **Renderizado Procedural en GPU** (HLSL) para crear un efecto de onda dinámica y coloreada.

---

## 2. Secciones Implementadas

El proyecto aborda y completa las siguientes secciones del taller:

| Sección | Tema | Implementación |
| :--- | :--- | :--- |
| **Sección 2** | **Geometría Procedural (CPU)** | Generación de una malla de plano dinámica. Deformación en tiempo real de los vértices (altura **Y**) usando una función **senoidal 1D** (`ProceduralWaveGen.cs`). |
| **Sección 3 & 4** | **Shaders Procedurales (GPU)** | Implementación de un *shader* URP en **HLSL** (`ProceduralURPHLSL.shader`). El color se calcula en el *Fragment Shader* basándose en la **posición mundial** (`positionWS`) y el **tiempo** (`_Time.y`). |
| **Sección 11** | **Proyección de Cámara** | Control de la vista de la cámara, permitiendo el *toggle* entre proyecciones `Perspectiva` y `Ortografica` (Barra Espaciadora commo *Trigger*). |


## 3. Componentes Clave del Código

| Archivo | Objeto Asignado | Función Principal |
| :--- | :--- | :--- |
| **`ProceduralWaveGen.cs`** | `ProceduralWave` | Genera la malla (`Mesh`), almacena las posiciones base (`baseVertices`), y calcula la deformación de la onda en `Update()`. |
| **`ProceduralURPHLSL.shader`** | `ProceduralMat` | Contiene el código HLSL para calcular el color dinámico y el mapeo. |
| **`CameraSwitch.cs`** | `Main Camera` | Fija la posición de cámara inicial y gestiona el *toggle* de proyección al presionar la **Barra Espaciadora**. |

## 4. Código Relevante
#### `ProceduralWaveGen.cs`
```csharp
void CreateProceduralMesh()
{
    // Vertex and UV gen
    List<Vector3> vertices = new List<Vector3>();
    List<Vector2> uvs = new List<Vector2>();

    for (int i = 0; i <= resolution; i++)
    {
        for (int j = 0; j <= resolution; j++)
        {
            // Vertex pos. Center at (0, 0, 0)
            float x = (float)i / resolution * size - size / 2f;
            float z = (float)j / resolution * size - size / 2f;
            vertices.Add(new Vector3(x, 0, z));
            uvs.Add(new Vector2((float)i / resolution, (float)j / resolution));
        }
    }
    mesh.vertices = vertices.ToArray();
    mesh.uv = uvs.ToArray();

    // Triangle gen -> Quad gen.
    List<int> triangles = new List<int>();
    for (int i = 0; i < resolution; i++)
    {
        for (int j = 0; j < resolution; j++)
        {
            int a = i * (resolution + 1) + j;
            int b = a + 1;
            int c = (i + 1) * (resolution + 1) + j;
            int d = c + 1;

            // Quad triangulation
            triangles.Add(a); triangles.Add(c); triangles.Add(b);
            triangles.Add(b); triangles.Add(c); triangles.Add(d);
        }
    }
    mesh.triangles = triangles.ToArray();
    mesh.RecalculateNormals();
}

void Update()
{
    if (baseVertices == null || baseVertices.Length == 0) return;

    currentVertices = mesh.vertices;

    for (int i = 0; i < currentVertices.Length; i++)
    {
        Vector3 basePos = baseVertices[i];

        // Wave behaviour. (Sine function used)
        float waveY = amplitude * Mathf.Sin(
            (basePos.x * frequency) + (Time.time * speed)
        );

        // New Height recalc.
        currentVertices[i] = new Vector3(basePos.x, waveY, basePos.z);
    }

    mesh.vertices = currentVertices;
    mesh.RecalculateNormals();
    mesh.RecalculateBounds();

}
```

#### `ProceduralURPHLSL.shader`
``` csharp 
HLSLPROGRAM

#pragma vertex vert
#pragma fragment frag

#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

struct Attributes {
    float4 positionOS : POSITION; 
};

struct Varyings {
    float4 positionCS : SV_POSITION; 
    float3 positionWS : TEXCOORD0; // Vertex pos in World Space
};

CBUFFER_START(UnityPerMaterial)
    float4 _Color;
    float _Frequency;
    float _Speed;
CBUFFER_END

// Vertex Shader
Varyings vert (Attributes input) {
    Varyings output;
    output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
    output.positionWS = TransformObjectToWorld(input.positionOS.xyz);

    return output;
}

// Fragment Shader (Procedural Color Calc.)
float4 frag (Varyings input) : SV_Target {
    
    float time = _Time.y; 

    // Color given time and pos.
    float r_comp = sin(input.positionWS.x * _Frequency + time * _Speed);
    float g_comp = sin(input.positionWS.z * _Frequency * 1.5 + time * _Speed * 1.5);
    
    // Mapping. Normalization from [-1, 1] -> [0, 1] coords..
    float intensityR = r_comp * 0.5 + 0.5;
    float intensityG = g_comp * 0.5 + 0.5;
    float intensityB = input.positionWS.y * 0.1 + 0.5; // BLUE -. Height
    
    float4 proceduralColor = float4(intensityR, intensityG, intensityB, 1.0);
    
    // Mix Procedural Color and Base Color
    return proceduralColor * _Color;
}
ENDHLSL
```

#### `CameraSwitch.cs`
``` csharp 
private Camera mainCamera;
void Start()
{
    mainCamera = GetComponent<Camera>();
    mainCamera.orthographic = false; // DEFAULT = PERSPECTIVE

    // Initial Camera pos.
    transform.position = new Vector3(25, 20, -30);
    transform.rotation = Quaternion.Euler(30, -45, 0);

    mainCamera.fieldOfView = 80;
}


void Update()
{
    // Camera Switch trigger = SpaceBar.
    if (Input.GetKeyDown(KeyCode.Space))
    {
        // Switch Projection
        mainCamera.orthographic = !mainCamera.orthographic;

        if (mainCamera.orthographic)
        {
            // Ortho adjustment. Size.
            mainCamera.orthographicSize = 18;
            Debug.Log("ORTHOGRAPHIC: (Sec. 11).");
        }
        else
        {
            Debug.Log("PERSPECTIVE:(Sec. 11).");
        }
    }
}
```

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