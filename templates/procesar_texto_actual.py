# Template para procesar texto, basado en
# primeros scripts creados en este proyecto

import re
import os
from collections import Counter

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")

def normalizar_opcion(linea):
    """
    Detecta opciones tipo 'a)', 'b)', etc., con ruido (espacios, guiones) y devuelve formato limpio.
    """
    match = re.match(r'^[\-\s]*([a-dA-D])[a-dA-D]?\)+\s*(.*)', linea)
    if match:
        letra = match.group(1).lower()
        texto = match.group(2).strip()
        return f"{letra}) {texto}", letra
    return None, None

def main(nombre_archivo=None, nombre_salida=None, nombre_archivo_log=None):
    archivo_entrada = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo}.txt")
    archivo_salida = os.path.join(CARPETA_TRABAJO, f"{nombre_salida}.txt")
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")

    # === LECTURA DE LÍNEAS ===
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = [line.rstrip() for line in f if line.strip()]

    # === 1. ELIMINAR LÍNEAS CON REFERENCIAS A IMÁGENES ===
    lineas = [l for l in lineas if not ("===== IMG_" in l and ".heic =====" in l)]

    nuevas_lineas = [ "TODO" ]
    log_advertencias = [ "TODO" ]

    # === 4. GUARDAR RESULTADOS ===
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for linea in lineas:
            f.write(linea + '\n')

    with open(archivo_log, 'a', encoding='utf-8') as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in log_advertencias:
            f.write(advertencia + '\n')

    # === 5. MENSAJE FINAL EN CONSOLA ===
    print(f"\n✅ Archivo normalizado guardado como: {archivo_salida}")
    print(f"📝 Log de advertencias guardado como: {archivo_log}")

if __name__ == "__main__":
    main()
