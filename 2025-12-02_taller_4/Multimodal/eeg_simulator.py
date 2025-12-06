# eeg_simulator.py
import math
import random

def eeg_valor(t: float) -> float:
    """
    Devuelve un valor entre 0 y 1 que simula un nivel de 'activación'.
    Combinamos una onda sinusoidal suave con un poquito de ruido.
    """
    base = 0.5 * (1 + math.sin(t))      # onda entre 0 y 1
    ruido = random.uniform(-0.1, 0.1)   # ruido pequeño
    valor = base + ruido
    return max(0.0, min(1.0, valor))
