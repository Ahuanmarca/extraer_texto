import re
import os
from collections import Counter

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
IMAGENES_CRUDAS = os.path.join(BASE_DIR, "imagenes_crudas")
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")

def main(nombre_archivo=None, nombre_salida=None, nombre_archivo_log=None):
    # === ENTRADA ===
    if not nombre_archivo:
        nombre_archivo = input("Archivo .txt a normalizar (sin extensión): ").strip()
    if not nombre_salida:
        nombre_salida = nombre_archivo + "_norm"
    archivo_entrada = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo}.txt")
    archivo_salida = os.path.join(CARPETA_TRABAJO, f"{nombre_salida}.txt")
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")

    # === LECTURA ===
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # === PATRONES ===
    pregunta_pat = re.compile(r'^(\d+)\.\s*(.*)')

    def normalizar_opcion(linea):
        match = re.match(r'^[\-\s]*([a-dA-D])[a-dA-D]?\)+\s*(.*)', linea)
        if match:
            letra = match.group(1).lower()
            texto = match.group(2).strip()
            return f"{letra}) {texto}", letra
        return None, None

    # === FUNCIONES ===
    nueva_lineas = []
    log_advertencias = []
    pregunta_actual = ""
    opciones_actuales = []
    letras_actuales = []

    with open(archivo_log, 'a', encoding='utf-8') as f:
        f.write('\nAdvertencias en proceso de normalización:\n')

    def guardar_pregunta_y_opciones():
        if not pregunta_actual:
            return

        errores = []

        if len(opciones_actuales) != 4:
            errores.append(f"⚠️ Pregunta con {len(opciones_actuales)} respuestas: {pregunta_actual[:100]}")

        # Verificar letras duplicadas
        letra_counts = Counter(letras_actuales)
        duplicadas = [letra for letra, count in letra_counts.items() if count > 1]
        if duplicadas:
            errores.append(f"⚠️ Letras duplicadas ({', '.join(duplicadas)}): {pregunta_actual[:100]}")

        if errores:
            log_advertencias.extend(errores)

        nueva_lineas.append(pregunta_actual.strip())
        nueva_lineas.extend([op.strip() for op in opciones_actuales])
        nueva_lineas.append("")  # línea vacía entre bloques

    # === PROCESAMIENTO ===
    for linea in lineas:
        linea = linea.rstrip()

        if not linea.strip():
            continue

        if "===== IMG_" in linea and ".heic =====" in linea:
            continue

        match_pregunta = pregunta_pat.match(linea)
        opcion_normalizada, letra_detectada = normalizar_opcion(linea)

        if match_pregunta:
            guardar_pregunta_y_opciones()
            pregunta_actual = f"{match_pregunta.group(1)}. {match_pregunta.group(2).strip()}"
            opciones_actuales = []
            letras_actuales = []
            continue

        elif opcion_normalizada:
            opciones_actuales.append(opcion_normalizada)
            letras_actuales.append(letra_detectada)
            continue

        # Continuación de la línea
        if opciones_actuales:
            opciones_actuales[-1] += f" {linea.strip()}"
        elif pregunta_actual:
            pregunta_actual += f" {linea.strip()}"

    # Guardar la última pregunta
    guardar_pregunta_y_opciones()

    # === SALIDA ===
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for linea in nueva_lineas:
            f.write(linea + '\n')

    with open(archivo_log, 'a', encoding='utf-8') as f:
        for advertencia in log_advertencias:
            f.write(advertencia + '\n')

    print(f"\n✅ Archivo normalizado guardado como: {archivo_salida}")
    print(f"📝 Log de advertencias guardado como: {archivo_log}")

if __name__ == "__main__":
    main()
