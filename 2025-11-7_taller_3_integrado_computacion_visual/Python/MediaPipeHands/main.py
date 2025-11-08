import cv2
import mediapipe as mp
import math

# --- Inicialización de MediaPipe Hands ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Configura la detección de manos
hands = mp_hands.Hands(
    static_image_mode=False,      # False para video (flujo)
    max_num_hands=2,              # Máximo de manos a detectar
    min_detection_confidence=0.5, # Confianza mínima de detección
    min_tracking_confidence=0.5)  # Confianza mínima de seguimiento

# --- Inicialización de OpenCV ---
cap = cv2.VideoCapture(0) # '0' es la cámara web por defecto

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignorando frame vacío de la cámara.")
        continue

    # Voltear la imagen horizontalmente (efecto espejo)
    image = cv2.flip(image, 1)

    # --- Procesamiento de MediaPipe ---
    # Convertir la imagen de BGR (OpenCV) a RGB (MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen y encontrar manos
    results = hands.process(image_rgb)

    # --- Dibujar los resultados ---
    # Volver a convertir a BGR para dibujar con OpenCV
    # image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR) # No necesario si usamos 'image' original

    if results.multi_hand_landmarks:
        # IDs de las puntas de los dedos
        tip_ids = [4, 8, 12, 16, 20]
        # Iterar sobre cada mano detectada
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar los landmarks (lo movemos aquí para que el texto quede encima)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style())

            # --- Lógica de conteo de dedos ---
            lm_list = [] # Lista para almacenar coordenadas

            # Obtener dimensiones de la imagen
            h, w, _ = image.shape

            # Extraer coordenadas de landmarks y guardarlas en lm_list
            for id, lm in enumerate(hand_landmarks.landmark):
                # Convertir coordenadas normalizadas (0-1) a píxeles
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            dedos_levantados = []

            if len(lm_list) != 0:
                # --- Lógica de Gesto de Pinza (Distancia) ---
                # Coordenadas de la punta del pulgar (4) e índice (8)
                x1, y1 = lm_list[4][1], lm_list[4][2] # Pulgar
                x2, y2 = lm_list[8][1], lm_list[8][2] # Índice

                # Calcular la distancia euclidiana
                distancia = math.hypot(x2 - x1, y2 - y1)

                # Visualizar la línea y los puntos
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3) # Línea azul
                cv2.circle(image, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(image, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                # Lógica para el Pulgar (es diferente, comparamos en X)
                # Asumiendo que la mano se muestra vertical
                if lm_list[tip_ids[0]][1] < lm_list[tip_ids[0] - 1][1]: # Compara X de la punta (4) vs X de (3)
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)

                # Lógica para los otros 4 dedos (comparar en Y)
                for id in range(1, 5):
                    # Si la punta (tip) está más arriba (menor Y) que la articulación (pip)
                    if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                        dedos_levantados.append(1)
                    else:
                        dedos_levantados.append(0)

                # Contar el total de dedos
                total_dedos = sum(dedos_levantados)

                # Mostrar el conteo en la pantalla
                cv2.putText(image, f'Dedos: {total_dedos}', (50, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    # --- Mostrar la imagen ---
    cv2.imshow('Detección de Manos - MediaPipe', image)

    # Salir con la tecla 'ESC'
    if cv2.waitKey(5) & 0xFF == 27:
        break

# --- Limpieza ---
hands.close()
cap.release()
cv2.destroyAllWindows()