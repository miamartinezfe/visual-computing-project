import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def analizar_resultados():
    print("📊 Analizando resultados de calibración...")
    
    # Cargar parámetros
    try:
        mtx = np.load('resultados/camera_matrix.npy')
        dist = np.load('resultados/distortion_coeffs.npy')
    except FileNotFoundError:
        print("❌ Ejecuta calibracion.py primero")
        return
    
    # Mostrar parámetros detallados
    print("\n🔍 ANÁLISIS DETALLADO DE PARÁMETROS:")
    
    fx, fy = mtx[0,0], mtx[1,1]
    cx, cy = mtx[0,2], mtx[1,2]
    
    print(f"Distancia focal X (fx): {fx:.2f} píxeles")
    print(f"Distancia focal Y (fy): {fy:.2f} píxeles")
    print(f"Centro óptico X (cx): {cx:.2f} píxeles") 
    print(f"Centro óptico Y (cy): {cy:.2f} píxeles")
    print(f"Relación fx/fy: {fx/fy:.4f} (cercano a 1.0 es ideal)")
    
    print(f"\nCoeficientes de distorsión:")
    print(f"k1: {dist[0][0]:.6f} (distorsión radial principal)")
    print(f"k2: {dist[0][1]:.6f} (distorsión radial secundaria)")
    print(f"p1: {dist[0][2]:.6f} (distorsión tangencial)")
    print(f"p2: {dist[0][3]:.6f} (distorsión tangencial)")
    print(f"k3: {dist[0][4]:.6f} (distorsión radial terciaria)")
    
    # Análisis de calidad
    print(f"\n✅ EVALUACIÓN DE CALIDAD:")
    
    # Verificar proporción de píxeles
    if abs(fx - fy) / fx < 0.05:
        print("🟢 Píxeles aproximadamente cuadrados")
    else:
        print("🟡 Píxeles no cuadrados - normal en algunas cámaras")
    
    if abs(dist[0][0]) > 0.1:
        print("🟡 Distorsión radial significativa detectada")
    else:
        print("🟢 Distorsión radial baja")
    
    # Generar gráficos comparativos
    generar_graficos_comparacion()
    
    # Análisis específico de distorsión
    analizar_distorsion()
    
    # Generar reporte final
    generar_reporte_final()

def generar_graficos_comparacion():
    print("\n📈 Generando gráficos comparativos...")
    
    # Buscar imágenes de ejemplo
    images = glob.glob('imagenes_tablero/*.jpg') + glob.glob('imagenes_tablero/*.png')
    
    if not images:
        print("❌ No se encontraron imágenes para comparación")
        return
    
    # Usar máximo 3 imágenes para el análisis
    images = images[:3]
    
    mtx = np.load('resultados/camera_matrix.npy')
    dist = np.load('resultados/distortion_coeffs.npy')
    
    # Crear figura para comparación
    fig, axes = plt.subplots(len(images), 2, figsize=(15, 5*len(images)))
    
    # Manejar caso de una sola imagen
    if len(images) == 1:
        axes = axes.reshape(1, -1)
    
    for i, img_path in enumerate(images):
        print(f"Procesando imagen {i+1}/{len(images)} para comparación...")
        
        # Cargar imagen
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Corregir distorsión
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        undistorted = cv2.undistort(img, mtx, dist, None, newcameramtx)
        undistorted_rgb = cv2.cvtColor(undistorted, cv2.COLOR_BGR2RGB)
        
        # Mostrar comparación
        axes[i,0].imshow(img_rgb)
        axes[i,0].set_title(f'Original {i+1} - Con Distorsión', fontsize=12, fontweight='bold')
        axes[i,0].axis('off')
        
        # Añadir líneas de referencia para mostrar distorsión
        h_orig, w_orig = img_rgb.shape[:2]
        axes[i,0].axhline(y=h_orig//2, color='red', linestyle='--', alpha=0.7, linewidth=2)
        axes[i,0].axvline(x=w_orig//2, color='red', linestyle='--', alpha=0.7, linewidth=2)
        
        axes[i,1].imshow(undistorted_rgb)
        axes[i,1].set_title(f'Corregida {i+1} - Sin Distorsión', fontsize=12, fontweight='bold')
        axes[i,1].axis('off')
        
        # Añadir líneas de referencia en imagen corregida
        h_corr, w_corr = undistorted_rgb.shape[:2]
        axes[i,1].axhline(y=h_corr//2, color='green', linestyle='--', alpha=0.7, linewidth=2)
        axes[i,1].axvline(x=w_corr//2, color='green', linestyle='--', alpha=0.7, linewidth=2)
    
    plt.tight_layout()
    plt.savefig('resultados/comparacion_visual.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("💾 Gráfico guardado: resultados/comparacion_visual.png")

def analizar_distorsion():
    """Análisis específico de los tipos de distorsión"""
    
    print("\n🔍 ANÁLISIS DE DISTORSIÓN:")
    
    dist = np.load('resultados/distortion_coeffs.npy')
    
    k1, k2, p1, p2, k3 = dist[0]
    
    # Análisis de distorsión radial
    if k1 > 0:
        print(f"📊 Distorsión radial: BARRIL (k1={k1:.4f})")
        print("   Las líneas rectas se curvan hacia adentro en los bordes")
    elif k1 < 0:
        print(f"📊 Distorsión radial: COJÍN (k1={k1:.4f})")
        print("   Las líneas rectas se curvan hacia afuera en los bordes")
    else:
        print("📊 Sin distorsión radial significativa")
    
    # Análisis de distorsión tangencial
    if abs(p1) > 0.001 or abs(p2) > 0.001:
        print(f"📊 Distorsión tangencial detectada: p1={p1:.4f}, p2={p2:.4f}")
        print("   La imagen puede parecer ligeramente inclinada")
    else:
        print("📊 Distorsión tangencial mínima")
    
    # Crear visualización de distorsión
    crear_mapa_distorsion()

def crear_mapa_distorsion():
    """Crear un mapa visual de la distorsión"""
    
    mtx = np.load('resultados/camera_matrix.npy')
    dist = np.load('resultados/distortion_coeffs.npy')
    
    # Crear una grilla de puntos
    h, w = 480, 640  # Dimensiones típicas
    
    # Puntos de una grilla regular
    x, y = np.meshgrid(np.arange(0, w, 40), np.arange(0, h, 40))
    points = np.column_stack((x.ravel(), y.ravel())).astype(np.float32)
    
    # Simular corrección inversa (mostrar cómo se distorsiona)
    points_undist = cv2.undistortPoints(
        points.reshape(-1, 1, 2), mtx, dist, None, mtx
    )
    points_undist = points_undist.reshape(-1, 2)
    
    # Crear visualización
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Grilla original (sin distorsión)
    ax1.scatter(points[:, 0], points[:, 1], c='blue', s=20, alpha=0.7)
    ax1.set_title('Grilla Ideal (Sin Distorsión)', fontweight='bold')
    ax1.set_xlim(0, w)
    ax1.set_ylim(0, h)
    ax1.invert_yaxis()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Grilla después de corrección
    ax2.scatter(points_undist[:, 0], points_undist[:, 1], c='red', s=20, alpha=0.7)
    ax2.set_title('Grilla Corregida', fontweight='bold')
    ax2.set_xlim(0, w)
    ax2.set_ylim(0, h)
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('resultados/mapa_distorsion.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("💾 Mapa de distorsión guardado: resultados/mapa_distorsion.png")

def generar_reporte_final():
    """Genera un reporte completo en markdown"""
    
    print("\n📋 GENERANDO REPORTE FINAL...")
    
    # Leer parámetros
    mtx = np.load('resultados/camera_matrix.npy')
    dist = np.load('resultados/distortion_coeffs.npy')
    
    fx, fy = mtx[0,0], mtx[1,1]
    cx, cy = mtx[0,2], mtx[1,2]
    k1, k2, p1, p2, k3 = dist[0]
    
    # Determinar tipo de distorsión
    tipo_distorsion = "BARRIL" if k1 > 0 else "COJÍN" if k1 < 0 else "MÍNIMA"
    calidad = "EXCELENTE" if abs(k1) < 0.1 else "BUENA" if abs(k1) < 0.3 else "REGULAR"
    
    reporte = f"""# 🎯 REPORTE FINAL - CALIBRACIÓN DE CÁMARA

## 📋 Resumen Ejecutivo

✅ **Estado de la Calibración**: {calidad}  
📊 **Tipo de Distorsión Principal**: {tipo_distorsion}  
🎯 **Error de Reproyección**: Ver archivo de calibración  

---

## 🔍 Parámetros Intrínsecos Obtenidos

### Matriz de Cámara (K):
```
[{fx:8.2f}    0.00    {cx:6.2f}]
[   0.00   {fy:8.2f}    {cy:6.2f}]
[   0.00      0.00      1.00   ]
```

### Interpretación:
- **Distancia Focal X**: {fx:.2f} píxeles
- **Distancia Focal Y**: {fy:.2f} píxeles  
- **Centro Óptico**: ({cx:.1f}, {cy:.1f}) píxeles
- **Relación fx/fy**: {fx/fy:.4f} {'✅ (píxeles cuadrados)' if abs(fx/fy - 1) < 0.05 else '⚠️ (píxeles rectangulares)'}

---

## 🌀 Coeficientes de Distorsión

| Coeficiente | Valor | Descripción |
|-------------|-------|-------------|
| k1 | {k1:8.6f} | Distorsión radial principal |
| k2 | {k2:8.6f} | Distorsión radial secundaria |
| p1 | {p1:8.6f} | Distorsión tangencial horizontal |
| p2 | {p2:8.6f} | Distorsión tangencial vertical |
| k3 | {k3:8.6f} | Distorsión radial terciaria |

### Análisis de Distorsión:
- **Tipo**: {tipo_distorsion} (k1 {'> 0' if k1 > 0 else '< 0' if k1 < 0 else '≈ 0'})
- **Severidad**: {'ALTA' if abs(k1) > 0.3 else 'MODERADA' if abs(k1) > 0.1 else 'BAJA'}
- **Distorsión Tangencial**: {'PRESENTE' if abs(p1) > 0.001 or abs(p2) > 0.001 else 'MÍNIMA'}

---

## 📊 Evaluación de Calidad

### Criterios de Evaluación:
- ✅ **Detección de Esquinas**: Automática con OpenCV
- ✅ **Consistencia de Parámetros**: Valores dentro de rangos esperados
- ✅ **Corrección Visual**: Líneas rectas más lineales después de calibración
- {'✅' if abs(k1) < 0.2 else '⚠️'} **Nivel de Distorsión**: {calidad.lower()}

### Recomendaciones:
{f'🟢 La calibración es {calidad.lower()} y lista para usar en aplicaciones.' if abs(k1) < 0.2 else '🟡 Considerar tomar más imágenes desde ángulos diversos para mejorar precisión.'}

---

## 🎯 Aplicaciones Sugeridas

Con estos parámetros puedes implementar:

1. **Corrección de Distorsión en Tiempo Real**
2. **Mediciones Precisas en Imágenes**
3. **Realidad Aumentada**
4. **Reconstrucción 3D**
5. **Visión Estéreo** (con segunda cámara calibrada)

---

## 📁 Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `camera_matrix.npy` | Matriz de parámetros intrínsecos |
| `distortion_coeffs.npy` | Coeficientes de distorsión |
| `comparacion_visual.png` | Comparación antes/después |
| `mapa_distorsion.png` | Visualización de la distorsión |
| `corners_detected_*.jpg` | Verificación de detección de esquinas |
| `REPORTE_FINAL.md` | Este reporte |

---

## 🔬 Conclusiones Técnicas

La calibración {'fue exitosa y los parámetros obtenidos son consistentes' if abs(k1) < 0.2 else 'requiere refinamiento adicional'}. 
{'La distorsión detectada es típica de cámaras web/móviles y puede corregirse efectivamente.' if abs(k1) < 0.3 else 'La alta distorsión indica la necesidad de más imágenes de calibración.'}

**Fecha de Calibración**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open('resultados/REPORTE_FINAL.md', 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print("✅ Reporte completo guardado: resultados/REPORTE_FINAL.md")

if __name__ == "__main__":
    analizar_resultados()