# voice_commands.py
import threading
import speech_recognition as sr

r = sr.Recognizer()

def _normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    reemplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in reemplazos:
        texto = texto.replace(a, b)
    return texto

def _escuchar_modo_blocking():
    """
    Escucha por el micrófono y devuelve:
    'dia', 'atardecer', 'noche' o None si no entiende.
    (Esta función es BLOQUEANTE. Por eso la usamos dentro de un thread.)
    """
    with sr.Microphone() as source:
        print("🎙️ Habla: 'día', 'atardecer' o 'noche'...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("🔎 Reconocido bruto:", texto)
        texto_norm = _normalizar_texto(texto)
        print("🔎 Normalizado:", texto_norm)

        if "dia" in texto_norm:
            return "dia"
        elif "atardecer" in texto_norm or "tarde" in texto_norm:
            return "atardecer"
        elif "noche" in texto_norm or "oscuro" in texto_norm:
            return "noche"
        else:
            print("⛔ No se reconoció un modo válido.")
            return None

    except sr.UnknownValueError:
        print("⛔ No se entendió el audio.")
        return None
    except sr.RequestError as e:
        print("⛔ Error con el servicio de reconocimiento:", e)
        return None

def escuchar_modo_en_segundo_plano(callback, on_finish=None):
    """
    Lanza un hilo que escucha y reconoce el modo, y luego llama a:
      callback(modo)   -> con 'dia' / 'atardecer' / 'noche' o None
    on_finish() se llama al final (opcional), para actualizar flags.
    """

    def worker():
        modo = _escuchar_modo_blocking()
        if callback is not None:
            callback(modo)
        if on_finish is not None:
            on_finish()

    hilo = threading.Thread(target=worker, daemon=True)
    hilo.start()
