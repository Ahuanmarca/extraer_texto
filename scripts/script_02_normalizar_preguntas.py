import re
import os
from collections import Counter

def main(nombre_archivo=None):
    # === ENTRADA ===
    if not nombre_archivo:
        nombre_archivo = input("Archivo .txt a normalizar (sin extensión): ").strip()
    archivo_entrada = f"carpeta_trabajo/{nombre_archivo}_extr.txt"
    archivo_salida = f"carpeta_trabajo/{nombre_archivo}_extr_norm.txt"
    archivo_log = f"carpeta_trabajo/{nombre_archivo[:15]}.log"

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
            nueva_lineas.append("-------- TO FIX --------")
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
