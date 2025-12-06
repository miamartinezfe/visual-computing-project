# scene2d.py
import cv2
import numpy as np

def colores_por_modo(modo: str):
    """
    Devuelve los colores (cielo, suelo, sol) en formato BGR según el modo.
    """
    if modo == "dia":
        cielo = (255, 200, 100)     # azul clarito (BGR)
        suelo = (60, 180, 60)       # verde
        sol_color = (0, 255, 255)   # amarillo
    elif modo == "atardecer":
        cielo = (80, 120, 255)      # naranja/rosado
        suelo = (40, 100, 40)
        sol_color = (0, 200, 255)
    elif modo == "noche":
        cielo = (40, 40, 80)        # azul oscuro
        suelo = (20, 60, 20)
        sol_color = (200, 200, 220) # luna
    else:  # por defecto día
        cielo = (255, 200, 100)
        suelo = (60, 180, 60)
        sol_color = (0, 255, 255)
    return cielo, suelo, sol_color


def dibujar_escena(width, height, modo, sol_x_norm, sol_y_norm, eeg=0.0):
    """
    Crea una imagen con:
    - cielo
    - suelo
    - sol/luna en la posición indicada (normalizada 0-1)
    - opcionalmente, estrellas e intensidad según 'eeg' (0-1)
    """
    # Crear imagen vacía
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Obtener colores según el modo
    cielo, suelo, sol_color = colores_por_modo(modo)

    # Pintar cielo
    img[:] = cielo

    # Pintar suelo (parte inferior de la imagen)
    suelo_y = int(height * 0.6)
    img[suelo_y:, :] = suelo

    # Calcular posición del sol/luna en píxeles a partir de [0,1]
    sol_x = int(sol_x_norm * width)
    sol_y = int(sol_y_norm * suelo_y)  # sólo aparece en el cielo

    # El EEG controla ligeramente el tamaño del sol
    radio_base = 40
    radio_sol = int(radio_base + 20 * eeg)  # crece con "activación"

    cv2.circle(img, (sol_x, sol_y), radio_sol, sol_color, -1)

    # Estrellas/partículas (sobre todo útiles en modo noche)
    # El EEG controla cuántas y qué tan brillantes
    num_estrellas = int(10 + 50 * eeg)
    if modo == "noche":
        for _ in range(num_estrellas):
            ex = np.random.randint(0, width)
            ey = np.random.randint(0, suelo_y)
            brillo = int(150 + 100 * eeg)
            cv2.circle(img, (ex, ey), 1, (brillo, brillo, brillo), -1)

    # Texto con el modo y el valor EEG
    cv2.putText(img, f"Modo: {modo}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    cv2.putText(img, f"EEG: {eeg:.2f}", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return img
