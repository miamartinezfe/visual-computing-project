# gestures.py
import mediapipe as mp

mp_hands = mp.solutions.hands

def obtener_posicion_mano(results):
    """
    Devuelve (x_norm, y_norm) de la mano en coordenadas normalizadas [0,1]
    usando la posición de la muñeca (landmark 0).

    Si no se detecta mano, devuelve None.
    """
    if not results.multi_hand_landmarks:
        return None

    # Tomamos solo la primera mano detectada
    hand_landmarks = results.multi_hand_landmarks[0]

    wrist = hand_landmarks.landmark[0]
    x_norm = wrist.x   # 0 (izquierda) a 1 (derecha)
    y_norm = wrist.y   # 0 (arriba) a 1 (abajo)

    return x_norm, y_norm
