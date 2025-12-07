import cv2
import numpy as np

def demo_tiempo_real():
    print("🎥 Iniciando demo en tiempo real...")
    
    # Cargar parámetros de calibración
    try:
        mtx = np.load('resultados/camera_matrix.npy')
        dist = np.load('resultados/distortion_coeffs.npy')
        print("✅ Parámetros de calibración cargados")
    except FileNotFoundError:
        print("❌ No se encontraron parámetros de calibración. Ejecuta calibracion.py primero")
        return
    
    # Inicializar cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return
    
    print("📷 Cámara iniciada. Presiona 'q' para salir, 's' para guardar frame")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ No se pudo capturar frame")
            break
        
        # Obtener dimensiones
        h, w = frame.shape[:2]
        
        # Calcular nueva matriz de cámara
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        
        # Aplicar corrección de distorsión
        undistorted = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        
        # Crear vista combinada (original | corregido)
        combined = np.hstack((frame, undistorted))
        
        # Añadir texto informativo
        cv2.putText(combined, 'ORIGINAL', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.putText(combined, 'CORREGIDO', (w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(combined, 'Presiona Q para salir, S para guardar', (10, h-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        # Mostrar resultado
        cv2.imshow('Calibracion en Tiempo Real - Original vs Corregido', combined)
        
        # Controles de teclado
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f'resultados/captura_tiempo_real_{frame_count:03d}.jpg'
            cv2.imwrite(filename, combined)
            print(f"💾 Guardado: {filename}")
            frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    print("🔚 Demo terminada")

if __name__ == "__main__":
    demo_tiempo_real()