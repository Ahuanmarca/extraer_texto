import os
from datetime import datetime

# Base de tu proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
CARPETA_STEPS = os.path.join(CARPETA_TRABAJO, "output/010-steps")

def guardar_texto_con_timestamp(texto: str, sufijo: str = None) -> str:
    """
    Guarda el texto en un archivo .txt con nombre basado en timestamp preciso.
    Puede incluir un sufijo personalizado.
    Devuelve la ruta completa del archivo guardado.
    """
    # Crear carpeta 'steps' si no existe
    os.makedirs(CARPETA_STEPS, exist_ok=True)

    # Timestamp preciso (hasta microsegundos)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    if sufijo:
        # Limpiamos espacios en el sufijo
        sufijo = sufijo.strip().replace(" ", "_")
        nombre_archivo = f"{timestamp}_{sufijo}.txt"
    else:
        nombre_archivo = f"{timestamp}.txt"

    ruta_archivo = os.path.join(CARPETA_STEPS, nombre_archivo)

    # Guardar archivo
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"📝 Archivo guardado: {ruta_archivo}")
    return ruta_archivo
