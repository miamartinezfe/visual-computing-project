"""
Script para probar la API REST de detección y segmentación
"""
import requests
import json
from pathlib import Path

# URL de la API
API_URL = "http://127.0.0.1:5000"

# Verificar que el servidor esté activo
print("🔍 Verificando conexión con la API...")
try:
    health = requests.get(f"{API_URL}/health", timeout=5)
    print(f"✅ Servidor activo: {health.json()}")
except Exception as e:
    print(f"❌ Error conectando al servidor: {e}")
    exit(1)

# Buscar una imagen de prueba
data_dir = Path("data/input")
if not data_dir.exists():
    data_dir = Path("data/samples")

image_files = list(data_dir.glob("*.jpg")) + list(data_dir.glob("*.png"))

if not image_files:
    print(f"❌ No se encontraron imágenes en {data_dir}/")
    exit(1)

image_path = image_files[0]
print(f"\n📸 Usando imagen: {image_path.name}")

# Enviar imagen al pipeline completo
print("\n🚀 Procesando con pipeline completo (YOLO + SAM)...")
try:
    with open(image_path, 'rb') as f:
        response = requests.post(
            f'{API_URL}/pipeline',
            files={'image': f},
            data={'model': 'yolov8n'}
        )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Procesamiento exitoso!")
        print(f"   • Objetos detectados: {result.get('num_detections', 0)}")
        
        if 'processing_time' in result:
            print(f"   • Tiempo de procesamiento: {result['processing_time']:.2f}s")
        if 'detection_time' in result:
            print(f"   • Tiempo de detección: {result['detection_time']:.3f}s")
        if 'segmentation_time' in result:
            print(f"   • Tiempo de segmentación: {result['segmentation_time']:.3f}s")
        
        print(f"\n📦 Detecciones:")
        detections = result.get('detections', [])
        for i, det in enumerate(detections[:5]):  # Mostrar máximo 5
            conf = det.get('confidence', 0)
            cls = det.get('class', 'unknown')
            bbox = det.get('bbox', [0, 0, 0, 0])
            print(f"   {i+1}. {cls} - Confianza: {conf:.2%}")
            print(f"      Posición: ({bbox[0]:.0f}, {bbox[1]:.0f}) - "
                  f"({bbox[2]:.0f}, {bbox[3]:.0f})")
        
        if len(detections) > 5:
            print(f"   ... y {len(detections) - 5} más")
        
        # Descargar imagen procesada si está disponible
        if 'output_image' in result:
            img_url = result['output_image']
            print(f"\n💾 Descargando imagen procesada...")
            img_response = requests.get(f'{API_URL}{img_url}')
            
            output_path = Path("results/api_test_result.jpg")
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Imagen guardada en: {output_path}")
        
        print(f"\n🎉 Prueba completada exitosamente!")
        
    else:
        print(f"❌ Error en la petición: {response.status_code}")
        print(f"   {response.text}")
        
except Exception as e:
    print(f"❌ Error durante el procesamiento: {e}")
    import traceback
    traceback.print_exc()
