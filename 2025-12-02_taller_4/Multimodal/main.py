# main.py
import cv2
import time
import mediapipe as mp

from scene2d import dibujar_escena
from eeg_simulator import eeg_valor
from gestures import obtener_posicion_mano
from voice_commands import escuchar_modo_en_segundo_plano

WIDTH = 800
HEIGHT = 600

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def main():
    cap = cv2.VideoCapture(0)

    modo = "dia"         # 'dia', 'atardecer', 'noche'
    sol_x_norm = 0.5
    sol_y_norm = 0.3

    t0 = time.time()

    # Control de voz en segundo plano
    ultimo_tiempo_voz = time.time()
    intervalo_voz = 3.0       # cada 3 segundos intenta escuchar
    escuchando_voz = False    # flag para no lanzar varios hilos a la vez

    nombre_ventana_escena = "Escena 2D multimodal (gestos + EEG + voz)"
    nombre_ventana_camara = "Camara (gestos)"

    cv2.namedWindow(nombre_ventana_escena)
    cv2.namedWindow(nombre_ventana_camara)

    def callback_modo(nuevo_modo):
        nonlocal modo
        if nuevo_modo is not None:
            modo = nuevo_modo
            print(f"✅ Modo cambiado por voz a: {modo}")
        else:
            print("❕ No se cambió el modo (no se reconoció bien).")

    def callback_fin_voz():
        nonlocal escuchando_voz, ultimo_tiempo_voz
        escuchando_voz = False
        ultimo_tiempo_voz = time.time()

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Procesar gestos (mano)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

            pos_mano = obtener_posicion_mano(results)
            if pos_mano is not None:
                x_norm, y_norm = pos_mano
                sol_x_norm = x_norm
                sol_y_norm = y_norm * 0.6  # solo parte de arriba

            # EEG simulado
            t = time.time() - t0
            eeg = eeg_valor(t)

            # Dibujar escena
            escena = dibujar_escena(
                WIDTH,
                HEIGHT,
                modo,
                sol_x_norm,
                sol_y_norm,
                eeg=eeg
            )

            cv2.imshow(nombre_ventana_camara, frame)
            cv2.imshow(nombre_ventana_escena, escena)

            # Solo usamos waitKey para refrescar ventanas y poder cerrarlas con la X
            key = cv2.waitKey(1) & 0xFF
            if cv2.getWindowProperty(nombre_ventana_escena, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.getWindowProperty(nombre_ventana_camara, cv2.WND_PROP_VISIBLE) < 1:
                break

            # Lanzar escucha de voz en segundo plano cada cierto tiempo
            ahora = time.time()
            if (ahora - ultimo_tiempo_voz > intervalo_voz) and not escuchando_voz:
                print("\n🕒 Lanzando escucha de voz en segundo plano...")
                escuchando_voz = True
                escuchar_modo_en_segundo_plano(callback_modo, on_finish=callback_fin_voz)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
