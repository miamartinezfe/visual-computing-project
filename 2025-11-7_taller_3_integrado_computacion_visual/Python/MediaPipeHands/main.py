import cv2
import numpy as np
from hand_gesture_controller import HandGestureController
from snake_game import SnakeGame

def main():
    # Inicializar componentes
    cap = cv2.VideoCapture(0)
    gesture_controller = HandGestureController()
    snake_game = SnakeGame(width=800, height=600)
    
    # Configurar ventana
    cv2.namedWindow('Snake con Gestos', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Snake con Gestos', 1200, 600)
    
    print("Controles del juego:")
    print("Mano ABIERTA (5 dedos) - Iniciar/Reiniciar juego")
    print("Solo INDICE - Arriba")
    print("INDICE y MEDIO - Derecha")
    print("INDICE, MEDIO y ANULAR - Abajo")
    print("4 dedos (sin pulgar) - Izquierda")
    print("PUÑO - Pausa/Stop")
    print("PUÑO por 3 segundos - Salir del juego")
    
    closed_hand_start_time = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Voltear frame horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)
            
            # Redimensionar frame de cámara para que ocupe 1/3 del ancho
            cam_height, cam_width = frame.shape[:2]
            target_cam_width = 400  # 1/3 de 1200
            target_cam_height = int(cam_height * target_cam_width / cam_width)
            frame_resized = cv2.resize(frame, (target_cam_width, target_cam_height))
            
            # Procesar gestos
            annotated_frame, gesture = gesture_controller.process_frame(frame_resized)
            
            # Detectar gesto de salida (puño cerrado por 3 segundos)
            if gesture == "STOP":
                if closed_hand_start_time is None:
                    closed_hand_start_time = cv2.getTickCount() / cv2.getTickFrequency()
                else:
                    elapsed_time = cv2.getTickCount() / cv2.getTickFrequency() - closed_hand_start_time
                    if elapsed_time > 3:  # 3 segundos
                        cv2.putText(annotated_frame, 'SALIENDO...', 
                                   (target_cam_width//2-80, target_cam_height//2), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow('Snake con Gestos', annotated_frame)
                        cv2.waitKey(1000)
                        break
                    # Mostrar cuenta regresiva
                    countdown = 3 - int(elapsed_time)
                    cv2.putText(annotated_frame, f'Saliendo en: {countdown}', 
                               (target_cam_width//2-70, target_cam_height-20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                closed_hand_start_time = None
            
            # Actualizar juego
            snake_game.update(gesture)
            
            # Crear canvas combinado (1200x600)
            combined_width = 1200
            combined_height = 600
            
            combined_canvas = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)
            
            # Colocar cámara a la izquierda (1/3)
            cam_y_offset = (combined_height - target_cam_height) // 2
            combined_canvas[cam_y_offset:cam_y_offset + target_cam_height, 0:target_cam_width] = annotated_frame
            
            # Colocar juego a la derecha (2/3)
            game_x_offset = target_cam_width
            game_y_offset = (combined_height - snake_game.height) // 2
            snake_game.draw(combined_canvas, x_offset=game_x_offset, y_offset=game_y_offset)
            
            # Dibujar línea divisoria
            cv2.line(combined_canvas, (target_cam_width, 0), (target_cam_width, combined_height), (100, 100, 100), 2)
            
            # Mostrar frame combinado
            cv2.imshow('Snake con Gestos', combined_canvas)
            
            # Salir con 'q' o ESC
            key = cv2.waitKey(1) & 0xFF
            if key in [ord('q'), 27]:  # 'q' o ESC
                break
                
    finally:
        # Liberar recursos
        cap.release()
        gesture_controller.release()
        cv2.destroyAllWindows()
        print("Juego terminado. ¡Hasta pronto!")

if __name__ == "__main__":
    main()