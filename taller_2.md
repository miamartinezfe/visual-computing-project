# Taller — Computación Visual & 3D: Jerarquías, Proyección, Raster, Visión por Computador y Generación Paramétrica


## Objetivo general


Integrar en **un solo taller** (multi-módulo) los temas de gráficos 3D y visión por computador: **jerarquías y transformaciones**, **proyecciones de cámara**, **rasterización clásica**, **visión artificial (filtros, bordes, segmentación, análisis geométrico)**, **modelos de color**, **conversión e inspección de formatos 3D**, **escenas paramétricas desde datos**, **filtros por convolución personalizada**, y **control por gestos con webcam**.
Cada tema se aborda como un **ejercicio** independiente dentro del mismo taller, con entregables homogéneos y una rúbrica común.


---


## Estructura del taller (ejercicios)


> Realiza **al menos 4 ejercicios** (libre elección) y documenta todo en un único `README.md`. Si haces más, mejor.
> Puedes trabajar en **Python (OpenCV/NumPy/etc.)**, **Three.js con React Three Fiber**, y/o **Unity (LTS)**.


---


### Ejercicio 1 — Árbol del Movimiento (Jerarquías y Transformaciones)


**Meta:** Comprender relaciones padre-hijo en escenas 3D y efectos de transformaciones acumuladas.


**Opciones por entorno**


* **Three.js + R3F:** Construye `<group>` con `<mesh>` hijos; controla rotación/traslación del padre (GUI: `leva` o `dat.GUI`); añade un **tercer nivel** para visualizar transformaciones encadenadas.
* **Unity (LTS):** Crea jerarquía **padre → hijo → nieto**; controla desde UI (sliders) la transformación del padre; muestra posición/rotación/escala actuales; **bonus:** animación con pausa/reinicio.


**Evidencia sugerida:** GIF de la escena con sliders y transformación heredada por los hijos.


---


### Ejercicio 2 — Ojos Digitales (Filtros y Bordes con OpenCV)


**Meta:** Entender el flujo básico de percepción: escala de grises, filtros y bordes.


**Entorno:** Python (Colab/Jupyter).
**Tareas:** convertir a gris, **blur/sharpen**, **Sobel X/Y**, **Laplaciano**, comparación visual; **bonus:** sliders (`cv2.createTrackbar`) y webcam en vivo.


**Evidencia:** Collage con resultados y breve análisis de diferencias entre métodos.


---


### Ejercicio 3 — Segmentando el Mundo (Binarización y Contornos)


**Meta:** Umbralización (fija y adaptativa) y detección de formas.


**Entorno:** Python (OpenCV).
**Tareas:** `threshold`, `adaptiveThreshold`, `findContours`, dibujar contornos; calcular **centroides** (momentos), **área**, **perímetro**; **bonus:** clasificar por vértices (`approxPolyDP`).


**Evidencia:** GIF mostrando imagen original → segmentada → contornos/centroides/cajas.


---


### Ejercicio 4 — Imagen = Matriz (Canales, Slicing, Histogramas)


**Meta:** Manipular pixeles y regiones directamente.


**Entorno:** Python (OpenCV + NumPy).
**Tareas:** separar **RGB/HSV**, editar regiones por slicing (cambiar color, copiar/pegar regiones), **histograma** de intensidades, **brillo/contraste** (manual u OpenCV); **bonus:** sliders interactivos.


**Evidencia:** Antes/después por regiones + histogramas.


---


### Ejercicio 5 — Rasterización desde Cero (Línea, Círculo, Triángulo)


**Meta:** Implementar algoritmos clásicos de raster (sin librerías de alto nivel).


**Entorno:** Python (Pillow/NumPy/Matplotlib).
**Tareas:** **Bresenham** (línea), **punto medio** (círculo) y **scanline** (relleno de triángulo).
**Evidencia:** Imágenes generadas y reflexión comparando precisión/eficiencia.


---


### Ejercicio 6 — Análisis Geométrico (Centroide, Área, Perímetro)


**Meta:** Extraer métricas de contornos en imágenes binarizadas.


**Entorno:** Python (OpenCV).
**Tareas:** `findContours`, `contourArea`, `arcLength`, centroides (momentos), etiquetar métricas sobre la imagen; **bonus:** clasificación automática (triángulo/cuadrado/círculo aproximado).


**Evidencia:** GIF de resultados con etiquetas numéricas.


---


### Ejercicio 7 — Importando el Mundo (OBJ/STL/GLTF)


**Meta:** Comparar y convertir formatos 3D y visualizar diferencias.


**Entornos:**


* **Python:** `trimesh`/`open3d`/`assimp` para cargar/inspeccionar **vértices, caras, normales, duplicados**; convertir entre formatos.
* **Three.js (R3F):** Cargar los tres formatos, alternar vista, comparar **materiales/texturas/suavidad**; **OrbitControls**; **bonus:** HUD con conteo de vértices.


**Evidencia:** Tabla comparativa + GIF con el selector de formato.


---


### Ejercicio 8 — Escenas Paramétricas (Objetos desde Datos)


**Meta:** Generar geometría a partir de listas/CSV/JSON.


**Opciones por entorno**


* **Python:** `vedo`/`open3d`/`trimesh` para instanciar primitivos desde coordenadas y reglas; **exportar** `.OBJ/.STL/.GLTF`.
* **Three.js (R3F):** Mapear arrays a `<mesh>` parametrizando posición/escala/color; GUI con `leva`.
* **Unity:** `GameObject.CreatePrimitive()` en runtime con listas/JSON; **bonus:** UI para regenerar/variar.


**Evidencia:** GIF de la escena y (si aplica) archivos exportados.


---


### Ejercicio 9 — Filtro Visual (Convoluciones Personalizadas)


**Meta:** Implementar **convolución 2D manual** y comparar con `cv2.filter2D`.


**Entorno:** Python (OpenCV + NumPy).
**Tareas:** diseñar al menos **3 kernels** (sharpen, blur, bordes/esquinas), comparar lado a lado; **bonus:** sliders para editar pesos del kernel.


**Evidencia:** Panel comparativo de filtros y comentarios de comportamiento.


---


### Ejercicio 10 — Explorando el Color (RGB, HSV, CIE Lab + Simulaciones)


**Meta:** Entender efectos de distintos modelos y condiciones de visión.


**Entornos:**


* **Python:** conversiones **RGB↔HSV/Lab**, visualización de canales, **simulación de daltonismo** (protanopía/deuteranopía mediante matrices), **baja iluminación** (brillo/contraste), filtros de temperatura/inversión/monocromo; **bonus:** función para alternar modelos.
* **Unity/Three.js (opcional):** materiales y cambios de color/shaders simples.


**Evidencia:** Comparativas de canales y simulaciones con breve reflexión.


---


### Ejercicio 11 — Proyecciones 3D (Perspectiva vs Ortográfica)


**Meta:** Comparar cámaras y matrices de proyección.


**Opciones por entorno**


* **Unity:** escena con objetos a distintas profundidades; alternar **perspectiva/ortográfica** (UI), ajustar `FOV/Size`, mostrar (opcional) `projectionMatrix`.
* **Three.js (R3F):** alternar `<PerspectiveCamera>`/`<OrthographicCamera>`, `OrbitControls`; mostrar **HUD** con parámetros; **bonus:** `Vector3.project(camera)` para ver proyección de un punto.


**Evidencia:** GIF alternando modo de cámara y variando parámetros.


---


### Ejercicio 12 — Gestos con Webcam (MediaPipe Hands)


**Meta:** Control visual por gestos en tiempo real.


**Entorno:** Python (MediaPipe + OpenCV).
**Tareas:** detectar manos, contar dedos, medir distancias, **mapear gestos a acciones** (cambiar color/mover objeto/cambiar escena); **bonus:** minijuego o UI controlada por gestos.


**Evidencia:** GIF de la interacción y breve nota sobre robustez/latencia.


---


## Entrega (estructura única del repositorio)


Crea la carpeta principal **`yyyy-mm-dd_taller_cv_3d`** con la siguiente estructura sugerida (puedes agregar más subcarpetas si lo requieres):


```
yyyy-mm-dd_taller_cv_3d/
├── ejercicios/
│   ├── 01_jerarquias_transformaciones/
│   ├── 02_ojos_digitales_opencv/
│   ├── 03_segmentacion_umbral_contornos/
│   ├── 04_imagen_matriz_pixeles/
│   ├── 05_rasterizacion_clasica/
│   ├── 06_analisis_figuras_geometricas/
│   ├── 07_conversion_formatos_3d/
│   ├── 08_escenas_parametricas/
│   ├── 09_convoluciones_personalizadas/
│   ├── 10_modelos_color_percepcion/
│   ├── 11_proyecciones_camara/
│   └── 12_gestos_webcam_mediapipe/
├── assets/                # imágenes de entrada, modelos 3D, CSV/JSON de datos
├── gifs/                  # evidencias animadas por ejercicio (nombradas coherentemente)
├── README.md              # documento maestro con toda la narrativa y enlaces
└── docs/                  # anexos, notas, PDFs opcionales
```


**En cada subcarpeta de ejercicio** coloca el código/notebook/escena correspondiente.
Puedes fusionar ambientes (Unity/Three.js/Python) dentro de la misma carpeta del ejercicio usando subcarpetas internas (`unity/`, `threejs/`, `python/`), si aplica.


---


## Contenido requerido del `README.md` (documento maestro)


Incluye secciones en este orden:


1. **Resumen del Taller** (1–2 párrafos): objetivos globales y alcance.
2. **Ejercicios Realizados**: por cada ejercicio que elijas, agrega:


  * Breve explicación (qué hiciste y por qué).
  * **GIF(s) animado(s)** (obligatorio) mostrando el resultado clave.
  * Enlace al código/escena/notebook dentro del repo.
  * **Prompts utilizados** (si aplican, p. ej. para generar assets).
  * Comentarios personales: aprendizaje, retos, mejoras futuras.
3. **Dependencias y Cómo Ejecutar**: por ambiente (Python/Unity/Three.js) y por ejercicio si cambian.
4. **Estructura del Repo** (pegar el árbol real).
5. **Créditos/Referencias** (si usaste datasets o modelos de terceros).


---





