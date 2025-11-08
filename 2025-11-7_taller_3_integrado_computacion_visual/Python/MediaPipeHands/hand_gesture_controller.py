import cv2
import mediapipe as mp
import numpy as np

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.prev_gesture = "NONE"
        
    def count_fingers(self, landmarks):
        """Cuenta los dedos levantados y detecta gestos"""
        fingers = []
        
        # Pulgar - comparamos la posición x del punto 4 con el punto 3
        if landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x < landmarks[self.mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Otros dedos - comparamos la posición y del punto de la punta con el punto MCP
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:  # índice, medio, anular, meñique
            if landmarks[tip].y < landmarks[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers
    
    def get_gesture(self, fingers):
        """Convierte el conteo de dedos en gestos para el juego"""
        count = sum(fingers)
        
        if count == 0:  # Puño cerrado
            return "STOP"
        elif count == 1 and fingers[1] == 1:  # Solo índice
            return "UP"
        elif count == 2 and fingers[1] == 1 and fingers[2] == 1:  # Índice y medio
            return "RIGHT"
        elif count == 3 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:  # Índice, medio, anular
            return "DOWN"
        elif count == 4:  # Todos menos pulgar
            return "LEFT"
        elif count == 5:  # Mano abierta
            return "START"
        else:
            return "NONE"
    
    def process_frame(self, frame):
        """Procesa el frame y detecta gestos"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        gesture = "NONE"
        annotated_frame = frame.copy()
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks
                self.mp_draw.draw_landmarks(
                    annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Obtener landmarks normalizados
                landmarks = hand_landmarks.landmark
                
                # Contar dedos
                fingers = self.count_fingers(landmarks)
                gesture = self.get_gesture(fingers)
                
                # Mostrar conteo de dedos
                cv2.putText(annotated_frame, f'Dedos: {sum(fingers)}', (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Mostrar gesto detectado
        cv2.putText(annotated_frame, f'Gesto: {gesture}', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Instrucciones
        cv2.putText(annotated_frame, 'Cerrado: Salir', (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        self.prev_gesture = gesture
        return annotated_frame, gesture
    
    def release(self):
        """Libera recursos"""
        self.hands.close()