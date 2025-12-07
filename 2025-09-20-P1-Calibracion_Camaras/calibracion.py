import cv2
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

def calibrar_camara():
    print("🚀 Iniciando calibración de cámara...")
    
    # CONFIGURACIÓN DEL TABLERO
    # Cambia estos valores según tu tablero impreso
    chessboard_size = (9, 6)  # (ancho, alto) esquinas internas
    square_size = 1.0  # Tamaño en unidades arbitrarias
    
    # Criterio de terminación para refinamiento de esquinas
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Preparar puntos 3D del tablero (z=0, plano)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)
    objp *= square_size
    
    # Arrays para almacenar puntos
    objpoints = []  # Puntos 3D en el mundo real
    imgpoints = []  # Puntos 2D en la imagen
    
    # Cargar imágenes
    images = glob.glob('imagenes_tablero/*.jpg') + glob.glob('imagenes_tablero/*.png')
    
    if len(images) == 0:
        print("❌ No se encontraron imágenes en la carpeta 'imagenes_tablero'")
        return None
    
    print(f"📸 Encontradas {len(images)} imágenes")
    
    # Crear carpeta de resultados
    os.makedirs('resultados', exist_ok=True)
    
    # Procesar cada imagen
    successful_images = 0
    
    for i, fname in enumerate(images):
        print(f"Procesando imagen {i+1}/{len(images)}: {os.path.basename(fname)}")
        
        img = cv2.imread(fname)
        if img is None:
            print(f"⚠️  No se pudo cargar: {fname}")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Buscar esquinas del tablero
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        
        if ret:
            # Refinar posición de esquinas
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            
            # Guardar puntos
            objpoints.append(objp)
            imgpoints.append(corners2)
            
            # Dibujar esquinas para verificación
            img_with_corners = img.copy()
            cv2.drawChessboardCorners(img_with_corners, chessboard_size, corners2, ret)
            cv2.imwrite(f'resultados/corners_detected_{i:03d}.jpg', img_with_corners)
            
            successful_images += 1
            print(f"✅ Esquinas detectadas correctamente")
        else:
            print(f"❌ No se pudieron detectar esquinas")
    
    print(f"\n📊 Resumen: {successful_images}/{len(images)} imágenes procesadas exitosamente")
    
    if successful_images < 10:
        print("⚠️  Se recomienda tener al menos 10 imágenes válidas para una buena calibración")
    
    # CALIBRACIÓN
    print("\n🔄 Ejecutando calibración...")
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    
    if not ret:
        print("❌ La calibración falló")
        return None
    
    # GUARDAR RESULTADOS
    np.save('resultados/camera_matrix.npy', mtx)
    np.save('resultados/distortion_coeffs.npy', dist)
    
    print("✅ Calibración completada exitosamente!")
    print(f"\n📋 RESULTADOS:")
    print(f"Matriz de cámara (K):\n{mtx}")
    print(f"\nCoeficientes de distorsión:\n{dist}")
    
    # CALCULAR ERROR DE REPROYECCIÓN
    total_error = 0
    errors = []
    
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        errors.append(error)
        total_error += error
    
    mean_error = total_error / len(objpoints)
    
    print(f"\n📏 ERROR DE REPROYECCIÓN:")
    print(f"Error medio: {mean_error:.4f} píxeles")
    print(f"Error máximo: {max(errors):.4f} píxeles")
    print(f"Error mínimo: {min(errors):.4f} píxeles")
    
    # Interpretación del error
    if mean_error < 0.5:
        print("🟢 Excelente calibración!")
    elif mean_error < 1.0:
        print("🟡 Buena calibración")
    else:
        print("🔴 Calibración regular - considera tomar más imágenes")
    
    # GENERAR IMAGEN CORREGIDA DE EJEMPLO
    test_img = cv2.imread(images[0])
    h, w = test_img.shape[:2]
    
    # Obtener nueva matriz de cámara optimizada
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    # Corregir distorsión
    dst = cv2.undistort(test_img, mtx, dist, None, newcameramtx)
    
    # Recortar imagen según ROI
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    # Guardar comparación
    comparison = np.hstack((test_img, cv2.resize(dst, (test_img.shape[1], test_img.shape[0]))))
    cv2.imwrite('resultados/comparacion_antes_despues.jpg', comparison)
    
    print(f"\n💾 Archivos guardados en 'resultados/':")
    print("- camera_matrix.npy")
    print("- distortion_coeffs.npy") 
    print("- corners_detected_*.jpg")
    print("- comparacion_antes_despues.jpg")
    
    return mtx, dist, mean_error

if __name__ == "__main__":
    calibrar_camara()