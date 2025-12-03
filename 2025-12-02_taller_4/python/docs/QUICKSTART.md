# Quick Start Guide

Esta guía te llevará desde la instalación hasta la ejecución del sistema de detección y segmentación en menos de 10 minutos.

---

## Requisitos Previos

- **Python** 3.10 o superior
- **Conda** (Anaconda o Miniconda)
- **GPU NVIDIA** con CUDA (recomendado, pero no obligatorio)
- **8GB RAM** mínimo (16GB recomendado)
- **10GB espacio en disco** para modelos

---

## Paso 1: Configuración del Entorno

### 1.1 Crear entorno conda

```bash
# Crear entorno con Python 3.10
conda create -n cv_subsystem python=3.10 -y

# Activar entorno
conda activate cv_subsystem
```

### 1.2 Instalar dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```


**Paquetes principales que se instalarán:**
- PyTorch (con soporte CUDA)
- Ultralytics (YOLOv8)
- Segment Anything
- OpenCV
- Flask
    # Jupyter (eliminado: notebooks ya no forman parte del repositorio)

---

## Limpieza automática de imágenes

Al cerrar el servidor web, **todas las imágenes** generadas en `data/output/web_results` y subidas a través de la interfaz en `data/input/web_uploads` se eliminan automáticamente para mantener el sistema limpio.

---

## Paso 2: Descargar Modelos

### 2.1 Descargar modelos pre-entrenados

```bash
# Descargar YOLO y SAM (esto puede tardar unos minutos)
python scripts/download_models.py
```

**Modelos descargados:**
- `yolov8n.pt` (6.2 MB) - YOLO Nano
- `yolov8s.pt` (21.5 MB) - YOLO Small  
- `yolov8m.pt` (49.7 MB) - YOLO Medium
- `sam_vit_b_01ec64.pth` (375 MB) - SAM ViT-B

### 2.2 Descargar imágenes de prueba

```bash
# Descargar imágenes de ejemplo
python scripts/download_samples.py
```

---


## Paso 3: Ejecutar el Sistema

### Opción A: API REST (Recomendado)

**Iniciar el servidor:**

```bash
cd python
conda activate cv_subsystem
python api/server.py
```

**Salida esperada:**
```
============================================================
DETECTION & SEGMENTATION API SERVER
============================================================
Starting server on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

**Probar la API:**

```bash
# En otra terminal
python tests/test_api.py
```

**Resultado esperado:**
```
Servidor activo
Usando imagen: people.jpg
Procesamiento exitoso!
    • Objetos detectados: 2
Prueba completada exitosamente!
```

---

### Opción B: Pipeline de Python

**Procesamiento de imagen individual:**

```bash
conda activate cv_subsystem
python detection/pipeline.py
```

**Con parámetros personalizados:**

```bash
python detection/pipeline.py \
    --image data/input/test.jpg \
    --model yolov8n \
    --output results/images/my_result.jpg
```

---

### Opción C: Detección con YOLO únicamente

**Solo detección de objetos:**

```bash
python detection/yolo_detector.py \
    --image data/input/test.jpg \
    --model yolov8n \
    --conf 0.25
```

**Parámetros:**
- `--image`: Ruta de la imagen
- `--model`: Modelo YOLO (n/s/m)
- `--conf`: Umbral de confianza (0.0-1.0)

---

### Opción D: Segmentación con SAM

**Segmentación precisa:**

```bash
python detection/sam_segmenter.py \
    --image data/input/test.jpg \
    --bbox "100,200,300,400"
```

---

### Opción E: Procesamiento de Video

**Video o webcam:**

```bash
# Procesar video
python detection/video_processor.py \
    --input video.mp4 \
    --output results/videos/output.mp4

# Webcam en tiempo real
python detection/video_processor.py \
    --webcam \
    --max-duration 30
```

---


## Paso 5: Usar la API REST

### 5.1 Endpoints Disponibles

#### Health Check
```bash
curl http://127.0.0.1:5000/health
```

#### Detección con YOLO
```bash
curl -X POST http://127.0.0.1:5000/detect \
  -F "image=@data/input/test.jpg" \
  -F "model=yolov8n"
```

#### Pipeline Completo (YOLO + SAM)
```bash
curl -X POST http://127.0.0.1:5000/pipeline \
  -F "image=@data/input/test.jpg" \
  -F "model=yolov8n"
```

### 5.2 Desde Python

```python
import requests

# Enviar imagen
with open('data/input/test.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:5000/pipeline',
        files={'image': f},
        data={'model': 'yolov8n'}
    )

result = response.json()
print(f"Detectados: {result['num_detections']} objetos")

# Descargar resultado
img_url = result['output_image']
img = requests.get(f'http://127.0.0.1:5000{img_url}')
with open('resultado.jpg', 'wb') as f:
    f.write(img.content)
```

### 5.3 Desde JavaScript

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('model', 'yolov8n');

fetch('http://127.0.0.1:5000/pipeline', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => {
    console.log(`Detectados: ${data.num_detections} objetos`);
    // Mostrar imagen resultado
    document.getElementById('result').src = 
        `http://127.0.0.1:5000${data.output_image}`;
});
```

---

## Paso 6: Generar Evidencias

### Crear videos y GIFs demostrativos

```bash
python utils/generate_evidence.py --mode all
```

**Genera:**
- Videos de demostración
- GIFs animados
- Capturas secuenciales
- Comparaciones visuales

---

## Paso 7: Métricas de Rendimiento

### Ejecutar benchmark

```python
from utils.metrics import BenchmarkRunner

benchmark = BenchmarkRunner()
results = benchmark.run_benchmark(
    images=['data/input/test.jpg'],
    models=['yolov8n', 'yolov8s', 'yolov8m']
)

# Ver resultados
print(benchmark.get_summary())

# Guardar métricas
benchmark.save_results('results/metrics/benchmark.csv')
```

---

## Configuración

### Archivo config.yaml

```yaml
yolo:
  model_dir: data/models
  default_model: yolov8n
  confidence_threshold: 0.25
  iou_threshold: 0.45
  
sam:
  model_path: data/models/sam_vit_b_01ec64.pth
  model_type: vit_b
  device: cuda  # cuda o cpu

api:
  host: 0.0.0.0
  port: 5000
  debug: false
  upload_folder: data/input/api_uploads
  output_folder: data/output/api_results
```

---

## Solución de Problemas

### Problema: Error al importar torch/CUDA

**Solución:**
```bash
# Reinstalar PyTorch con CUDA
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Problema: ModuleNotFoundError

**Solución:**
```bash
# Asegurarse de estar en el entorno correcto
conda activate cv_subsystem

# Verificar instalación
pip list | grep -E "ultralytics|segment-anything|torch"
```

### Problema: Memoria insuficiente

**Solución:**
```python
# Usar modelo más pequeño
python detection/pipeline.py --model yolov8n

# O procesar en CPU
python detection/pipeline.py --device cpu
```

### Problema: API no responde

**Solución:**
```bash
# Verificar que el puerto 5000 esté libre
netstat -ano | findstr :5000

# Usar puerto alternativo
python api/server.py --port 5001
```

---

## Comandos Útiles

### Verificar instalación
```bash
# Verificar Python
python --version

# Verificar paquetes
pip list | grep -E "torch|ultralytics|opencv"

# Verificar CUDA
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}')"
```

### Limpiar resultados
```bash
# Limpiar carpetas de resultados
rm -rf results/images/*
rm -rf results/videos/*
rm -rf data/output/*
```

### Ver logs del servidor
```bash
# Ejecutar con logs detallados
python api/server.py --debug
```

---

## Flujo de Trabajo Típico

### 1. Desarrollo/Pruebas
```bash
# Activar entorno
conda activate cv_subsystem

# Probar con notebook
jupyter notebook notebooks/01_yolo_detection_demo.ipynb

# Probar pipeline
python detection/pipeline.py --image test.jpg
```

### 2. Producción/API
```bash
# Iniciar servidor
cd python
conda activate cv_subsystem
python api/server.py

# En otra terminal: ejecutar tests
python tests/test_api.py

# Hacer peticiones desde tu aplicación
curl -X POST http://localhost:5000/pipeline -F "image=@img.jpg"
```

### 3. Análisis de Resultados
```bash
# Generar evidencias
python utils/generate_evidence.py

# Ver métricas
python utils/metrics.py

# Revisar resultados en results/
```

---

## Documentación Adicional

- **[INSTALLATION.md](docs/INSTALLATION.md)** - Guía detallada de instalación
- **[USAGE.md](docs/USAGE.md)** - Ejemplos de uso avanzado
- **[API.md](docs/API.md)** - Referencia completa de la API
- **[EVIDENCIAS.md](docs/EVIDENCIAS.md)** - Resultados y benchmarks
- **[STRUCTURE.md](STRUCTURE.md)** - Estructura del proyecto

---


## Listo!

Ahora tienes el sistema completamente funcional. Puedes:

- Detectar objetos con YOLO  
- Segmentar con SAM  
- Procesar videos en tiempo real  
- Usar la API REST  
- Experimentar con notebooks  
- Generar evidencias visuales  

**Nota:** Al cerrar el servidor web (`api/web_interface.py`) se eliminarán automáticamente todas las imágenes generadas en `data/output/web_results/` para mantener limpio el sistema.

**¿Necesitas ayuda?** Consulta la documentación en `docs/` o revisa los ejemplos en `notebooks/`.

---

**Última actualización**: Diciembre 2, 2025  
**Versión**: 1.0.0  
**Autor**: Taller 4 - Visual Computing
