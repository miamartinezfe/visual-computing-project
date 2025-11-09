# Practica: **Percepción Visual con YOLO, MediaPipe, MiDaS y SAM** (Colab-Ready)

> **Meta:** Construir un mini-pipeline de visión por computador que combine **detección (YOLO)**, **landmarks/gestos (MediaPipe)**, **profundidad monocular (MiDaS)** y **segmentación interactiva (SAM)** para resolver tareas integradas sobre imágenes y video.

---

## 1) Referencias (Colab / Docs)

* **YOLO (Ultralytics)**

  * Notebook oficial: *Ultralytics Examples Tutorial* (Colab). ([https://colab.research.google.com/github/ultralytics/ultralytics/blob/main/examples/tutorial.ipynb?utm_source=chatgpt.com][1])
  * Guía Colab e integración/training: *Ultralytics + Google Colab*. ([https://docs.ultralytics.com/es/integrations/google-colab/?utm_source=chatgpt.com][2])
  * Modo `train/val/predict` (doc). ([https://docs.ultralytics.com/es/modes/train/?utm_source=chatgpt.com][3])

* **MediaPipe**

  * Guía oficial “Solutions” (Python/Web/Android/iOS). ([https://ai.google.dev/edge/mediapipe/solutions/guide?utm_source=chatgpt.com&hl=es-419][4])
  * Setup Python (instalación). ([https://ai.google.dev/edge/mediapipe/solutions/setup_python?utm_source=chatgpt.com&hl=es-419][5])
  * Repo oficial (para ejemplos y tasks). ([https://github.com/google-ai-edge/mediapipe?utm_source=chatgpt.com][6])

* **MiDaS (Depth)**

  * Notebook Colab (PyTorch Hub). ([https://colab.research.google.com/github/pytorch/pytorch.github.io/blob/master/assets/hub/intelisl_midas_v2.ipynb?utm_source=chatgpt.com][7])
  * Repo oficial MiDaS (códigos y modelos). ([https://github.com/isl-org/MiDaS?utm_source=chatgpt.com][8])
  * Tutorial OpenVINO (opcional, aceleración). ([https://docs.openvino.ai/2024/notebooks/vision-monodepth-with-output.html?utm_source=chatgpt.com][9])

* **SAM / SAM-2 (Segment Anything)**

  * Repo oficial SAM (Meta). ([https://github.com/facebookresearch/segment-anything?utm_source=chatgpt.com][10])
  * Notebook SAM (Roboflow) en Colab (uso práctico). ([https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/how-to-segment-anything-with-sam.ipynb?utm_source=chatgpt.com][11])
  * SAM-2 (segmentación en video, referencia). ([https://github.com/facebookresearch/sam2?utm_source=chatgpt.com][12])
  * Doc de SAM en Ultralytics (API práctica). ([https://docs.ultralytics.com/es/models/sam/?utm_source=chatgpt.com][13])

---

## 2) Instrucciones principales (paso a paso)

1. **YOLO – Detección base**

   * Abre el notebook de Ultralytics en Colab y corre `predict` sobre 5 imágenes tuyas o un clip corto (10–20 s).
   * Exporta resultados (bounding boxes + confianza). Describe dos “failure cases”.

2. **MediaPipe – Landmarks/gestos**

   * Instala y prueba **MediaPipe Tasks** en Python (mano o pose). Captura landmarks en tiempo real o sobre video.
   * Define al menos **2 reglas de interacción**: p. ej., gesto de “pinch” = pausar video, gesto “mano abierta” = tomar captura. Documenta FPS y estabilidad.

3. **MiDaS – Profundidad monocular**

   * Usa el notebook de MiDaS para generar mapas de profundidad **de las mismas imágenes** usadas en YOLO.
   * Normaliza el depth map y calcula una **métrica de distancia relativa** del objeto detectado (promedio del depth dentro de su bbox). Explica sus límites.
   * (Opcional) Prueba el flujo con OpenVINO para comparar latencia.

4. **SAM – Segmentación por prompts**

   * En Colab, aplica SAM para **refinar** la región de un objeto detectado por YOLO (prompt = caja de YOLO). Exporta la **máscara binaria**.
   * Evalúa 2 prompts distintos (puntos vs caja) y compara IoU entre máscaras.

5. **Mini-pipeline integrado**

   * **Input:** imagen o frame de video.
   * **Flujo:** YOLO (bbox) → SAM (máscara del objeto) → MiDaS (profundidad relativa del objeto) → MediaPipe (si hay gesto, guarda/descarta resultado).
   * **Output:** overlay con bbox, máscara, y etiqueta “cerca/medio/lejos” según percentiles de profundidad.
   * Mide latencia (ms) por etapa y reporta un diagrama simple del pipeline.

---

## 3) Reto creativo

Crea una **demo temática** (elige un tema: movilidad urbana, laboratorio, cocina, makerspace, etc.) donde:

* YOLO detecte **≥3 categorías** relevantes al tema.
* SAM genere máscaras útiles para **recortes o conteo de pixeles** (p. ej., área ocupada).
* MiDaS estime si los objetos están **más cerca que la mediana** de la escena (clasifícalos en 3 bins).
* MediaPipe permita **control hands-free** (p. ej., gesto=“siguiente escena” / “captura”).
* Muestra **al menos 2 clips** con condiciones de luz distintas.

---

## 4) Entrega esperada

* **Notebook(s) Colab** con todo el flujo (enlaces compartibles).
* **Dataset mínimo** (5–10 imágenes o 2 videos cortos).
* **Capturas** (3–5 imágenes) mostrando:

  1. sólo YOLO, 2) YOLO+SAM (máscara), 3) YOLO+MiDaS (mapa de profundidad + bin), 4) pipeline completo, 5) gesto MediaPipe actuando.
* **Video corto** (30–60 s) con la demo integrada (antes/después).
* **Ficha técnica** (PDF o README): decisiones, métricas, hardware, tiempos por etapa.
* **Tabla de latencia** por módulo (promedio de 50 frames).

---

## 5) Estructura de repositorio

```
yyyy-mm-dd_practica_percepcion_multimodelo/
├── colab_links/                  # .txt con URLs a tus notebooks
├── data/                         # imágenes y/o videos de prueba
├── results/
│   ├── yolo/                     # predicciones .jpg/.mp4 con bboxes
│   ├── sam/                      # máscaras .png
│   ├── midas/                    # depth maps .png / .npy
│   └── demo/                     # video final, gifs
├── metrics/
│   ├── latency.csv               # tiempos por etapa
│   └── iou_masks.csv             # IoU entre prompts
├── diagrams/
│   └── pipeline.drawio.png       # diagrama del flujo
└── README.md
```

---

## 6) Contenido del `README.md`

* **Resumen del proyecto** (tema elegido y caso de uso).
* **Referencias usadas** (pega tus 4–6 enlaces clave de Colab/Docs).
* **Pipeline** (diagrama + explicación breve de cada etapa).
* **Parámetros clave**

  * YOLO: modelo, umbral conf/NMS, resolución.
  * MediaPipe: task, FPS, landmarks usados.
  * MiDaS: versión del modelo y normalización del mapa.
  * SAM: tipo de prompt (punto/caja), versión del checkpoint.
* **Métricas** (latencia por etapa, IoU de máscaras, % de aciertos “cerca/medio/lejos”).
* **Limitaciones** (ruido en profundidad, oclusiones, sensibilidad a luz).
* **Futuro** (SAM-2 para video, cuantización, seguimiento multi-objeto).

---

## 7) Criterios de evaluación

* ✅ **Ejecución individual** de cada modelo con evidencia (capturas/resultados).
* ✅ **Integración**: flujo YOLO→SAM→MiDaS (+ control con MediaPipe) funcionando.
* ✅ **Métricas**: latencia por etapa e IoU de máscaras reportadas.
* ✅ **Calidad de documentación** (README) y **orden** del repo.
* ✅ **Reto creativo**: coherencia temática y comparación en **2 condiciones de luz**.
* ✅ **Buenas prácticas**: enlazar notebooks, describir fallos y limitaciones.

---

## 8) Pistas técnicas rápidas

* **Sin GPU local:** usa Colab y reduce resolución de entrada para medir latencia realista.
* **Profundidad relativa:** promedia el depth **dentro de la máscara de SAM** (mejor que en bbox) para robustez.
* **Control gestual:** filtra landmarks con media móvil (3–5 frames) para suavizar jitter.

---
