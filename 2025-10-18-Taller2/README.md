# Ejercicio 2 — Ojos Digitales (Filtros y Bordes con OpenCV)

## Meta
Entender el flujo básico de percepción en imágenes digitales: procesamiento en escala de grises, aplicación de filtros convolucionales y detección de bordes.

## Entorno
- **Lenguaje:** Python  
- **Plataforma:** Jupyter Notebook  
- **Librerías:**  
  - `opencv-python (cv2)`
  - `matplotlib`
  - `numpy`

## Objetivos del Ejercicio
1. Convertir imágenes a escala de grises
2. Aplicar filtros de suavizado (Blur) y enfoque (Sharpen)
3. Detectar bordes usando operadores Sobel (X e Y)
4. Detectar bordes usando el operador Laplaciano
5. Comparar visualmente los diferentes métodos
6. **Bonus:** Implementar controles interactivos con sliders y cámara web en tiempo real

---

## Bibliotecas Utilizadas

```python
import cv2                    # OpenCV - procesamiento de imágenes
import numpy as np            # Manejo eficiente de matrices
import matplotlib.pyplot as plt  # Visualización de resultados
```

---

## Desarrollo del Ejercicio

### 1. Carga y Visualización de la Imagen

```python
img = cv2.imread('lena.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Conversión BGR→RGB para Matplotlib
```

**Nota:** OpenCV carga imágenes en formato BGR, mientras que Matplotlib espera RGB. La conversión es necesaria para visualización correcta.

### 2. Conversión a Escala de Grises

```python
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

La escala de grises simplifica el procesamiento al reducir la imagen de 3 canales (RGB) a 1 canal de intensidad, facilitando la detección de bordes y patrones.

### 3. Aplicación de Filtros

#### Filtro Blur (Gaussiano)

```python
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
```

- **Propósito:** Suavizar la imagen y reducir ruido
- **Kernel:** 7x7 píxeles
- **Efecto:** Elimina detalles finos y reduce artefactos

#### Filtro Sharpen (Enfoque)

```python
kernel_sharp = np.array([[0, -1, 0], 
                         [-1, 5, -1], 
                         [0, -1, 0]])
img_sharp = cv2.filter2D(img_gray, -1, kernel_sharp)
```

- **Propósito:** Resaltar bordes y detalles
- **Kernel personalizado:** Realza diferencias entre píxeles vecinos
- **Efecto:** Aumenta la nitidez y contraste de bordes

### 4. Detección de Bordes

#### Operador Sobel

```python
sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=5)  # Bordes verticales
sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=5)  # Bordes horizontales
```

- **Sobel X:** Detecta cambios de intensidad en dirección horizontal (bordes verticales)
- **Sobel Y:** Detecta cambios de intensidad en dirección vertical (bordes horizontales)
- **Kernel size:** 5x5 píxeles
- **Ventaja:** Permite analizar orientación de bordes

#### Operador Laplaciano

```python
laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
```

- **Propósito:** Detectar bordes en todas direcciones simultáneamente
- **Característica:** Segunda derivada, más sensible a cambios abruptos
- **Ventaja:** No requiere análisis direccional separado

### 5. Visualización Comparativa

```python
titles = ['Original', 'Gray', 'Blur', 'Sharpen', 'Sobel X', 'Sobel Y', 'Laplacian']
images = [img_rgb, img_gray, img_blur, img_sharp, sobelx, sobely, laplacian]

plt.figure(figsize=(15,8))
for i in range(7):
    plt.subplot(2,4,i+1)
    plt.imshow(images[i], cmap='gray' if i>0 else None)
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.show()
```

---

## Resultados

A continuación se muestra el collage que compara cada etapa del procesamiento:

![Collage de resultados](output_5_0.png)

### Análisis Comparativo de Métodos

| Método | Características | Mejor Uso |
|--------|----------------|-----------|
| **Original** | Imagen RGB original | Referencia visual |
| **Gray** | Imagen base en escala de grises | Preprocesamiento estándar |
| **Blur** | Suaviza detalles, reduce ruido | Eliminar artefactos antes de detección de bordes |
| **Sharpen** | Resalta bordes y detalles finos | Mejorar definición de contornos |
| **Sobel X** | Detecta bordes verticales (cambios horizontales) | Identificar líneas verticales y estructuras |
| **Sobel Y** | Detecta bordes horizontales (cambios verticales) | Identificar líneas horizontales |
| **Laplacian** | Detecta todos los bordes simultáneamente | Detección general de contornos, alta sensibilidad |

### Observaciones Clave

1. **Blur vs Sharpen:** Son operaciones opuestas. Blur elimina detalles mientras que Sharpen los realza.

2. **Sobel X e Y:** Proporcionan información direccional. Combinados pueden calcular la magnitud total del gradiente: `√(Sobel_X² + Sobel_Y²)`

3. **Laplaciano:** Más sensible al ruido que Sobel, detecta cambios abruptos de intensidad. Combina información de ambas direcciones en un solo operador.

4. **Preprocesamiento:** Aplicar Blur antes de detectar bordes puede mejorar resultados al reducir falsos positivos causados por ruido.

---

## Bonus: Sistema Interactivo con Webcam y Sliders

### Descripción

Se implementó un sistema en tiempo real que permite ajustar parámetros de filtros mediante sliders y visualizar los resultados instantáneamente desde la cámara web.

### Características del Sistema

1. **Grid 2x2 de visualización:**
   - **Superior izquierda:** Imagen original en escala de grises
   - **Superior derecha:** Blur + Sharpen aplicados
   - **Inferior izquierda:** Detección Sobel combinada (X + Y)
   - **Inferior derecha:** Detección Laplaciano

2. **Controles interactivos:**
   - **Blur slider:** Ajusta el nivel de suavizado (kernel size 1-15)
   - **Sharpen slider:** Controla la intensidad del enfoque (0-5)
   - **Sobel k:** Modifica el tamaño del kernel Sobel (1-7)
   - **Lap k:** Modifica el tamaño del kernel Laplaciano (1-7)

3. **Pipeline de procesamiento:**
   ```
   Webcam → Gris → Blur → Sharpen → [Sobel / Laplacian] → Grid Display
   ```

### Implementación

```python
import cv2
import numpy as np

def nothing(x):
    pass

def resize_img(img, size=(150, 150)):
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)  # Inicializar webcam

cv2.namedWindow('Filtros Demo')
cv2.resizeWindow('Filtros Demo', 200, 200)

# Crear sliders
cv2.createTrackbar('Blur', 'Filtros Demo', 1, 15, nothing)
cv2.createTrackbar('Sharpen', 'Filtros Demo', 0, 5, nothing)
cv2.createTrackbar('Sobel k', 'Filtros Demo', 1, 7, nothing)
cv2.createTrackbar('Lap k', 'Filtros Demo', 1, 7, nothing)

size = (150, 150)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Leer valores de sliders
    blur_k = cv2.getTrackbarPos('Blur', 'Filtros Demo') | 1
    sharp_i = cv2.getTrackbarPos('Sharpen', 'Filtros Demo')
    sobel_k = cv2.getTrackbarPos('Sobel k', 'Filtros Demo') | 1
    lap_k = cv2.getTrackbarPos('Lap k', 'Filtros Demo') | 1

    # Procesar Blur+Sharpen
    img_blur = cv2.GaussianBlur(img_gray, (blur_k, blur_k), 0)
    kernel_sharp = np.array([[0, -1, 0], [-1, 5 + sharp_i, -1], [0, -1, 0]])
    blur_sharpen = cv2.filter2D(img_blur, -1, kernel_sharp)
    blur_sharpen_resized = resize_img(blur_sharpen, size)

    # Sobel y Laplaciano
    sobelx = cv2.Sobel(blur_sharpen, cv2.CV_64F, 1, 0, ksize=sobel_k)
    sobely = cv2.Sobel(blur_sharpen, cv2.CV_64F, 0, 1, ksize=sobel_k)
    sobel_combined = cv2.convertScaleAbs(np.sqrt(sobelx**2 + sobely**2))
    sobel_combined = resize_img(sobel_combined, size)

    laplacian = cv2.convertScaleAbs(cv2.Laplacian(blur_sharpen, cv2.CV_64F, ksize=lap_k))
    laplacian = resize_img(laplacian, size)
    
    original = resize_img(img_gray, size)

    # Crear grid 2x2
    top_row = np.hstack([original, blur_sharpen_resized])
    bottom_row = np.hstack([sobel_combined, laplacian])
    grid = np.vstack([top_row, bottom_row])

    cv2.imshow('Filtros Demo', grid)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Instrucciones de uso:**
- Ejecutar el código para iniciar la cámara web
- Ajustar los sliders para experimentar con diferentes parámetros
- Presionar `q` para salir del programa

### Ventajas del Sistema Interactivo

- **Experimentación en tiempo real:** Permite ver inmediatamente el efecto de cada parámetro
- **Comprensión intuitiva:** Facilita entender cómo cada filtro afecta la imagen
- **Optimización de parámetros:** Ayuda a encontrar valores óptimos para diferentes escenarios
- **Visualización simultánea:** Compara múltiples técnicas al mismo tiempo

### Observaciones del Sistema en Tiempo Real

- **Blur bajo (1-3):** Preserva detalles pero puede mostrar ruido
- **Blur alto (11-15):** Suaviza excesivamente, puede perder bordes importantes
- **Sharpen óptimo:** Valores 2-3 suelen dar mejor balance
- **Sobel k pequeño (1-3):** Mayor sensibilidad pero más ruido
- **Laplacian k mayor:** Reduce sensibilidad al ruido pero puede perder detalles finos

---

## Conclusiones

Este ejercicio demuestra el flujo básico de percepción visual computacional:

1. **Preprocesamiento:** Conversión a escala de grises simplifica el análisis
2. **Filtrado:** Permite controlar el balance ruido-detalle según necesidades
3. **Detección de bordes:** Fundamental para reconocimiento de patrones y segmentación
4. **Interactividad:** Los controles en tiempo real facilitan la comprensión y optimización

Los diferentes métodos de detección de bordes tienen aplicaciones específicas:
- **Sobel:** Ideal cuando la orientación del borde es relevante
- **Laplaciano:** Mejor para detección rápida omnidireccional
- **Pipeline Blur→Sharpen→Edge:** Produce resultados más robustos al ruido

### Aplicaciones Prácticas

- **Visión artificial:** Reconocimiento de objetos, lectura de códigos QR
- **Segmentación de imágenes:** Separar regiones de interés
- **Análisis médico:** Detección de contornos en radiografías o tomografías
- **Robótica:** Navegación autónoma y detección de obstáculos
- **Procesamiento de video:** Seguimiento de objetos en movimiento

---

## Referencias

- OpenCV Documentation: https://docs.opencv.org/
- Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
- Laplacian Operator: https://en.wikipedia.org/wiki/Laplace_operator
- Gaussian Blur: https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html

---