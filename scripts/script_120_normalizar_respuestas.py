import re
import os
from collections import Counter
from funciones.normalizadores import corregir_numeracion_y_letras
from funciones.normalizadores import corregir_letras_duplicadas
from funciones.normalizadores import insertar_linea_vacia_antes_numeracion
from funciones.normalizadores import unir_oraciones_partidas
from funciones.normalizadores import unir_palabras_partidas_por_guiones

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")


def main(nombre_archivo=None, nombre_salida=None, nombre_archivo_log=None):
    archivo_entrada = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo}.txt")
    archivo_salida = os.path.join(CARPETA_TRABAJO, f"{nombre_salida}.txt")
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")

    # === LECTURA DE LÍNEAS === <-- Se omiten líneas vacías
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        lineas = [line.rstrip() for line in f if line.strip()]

    # === 1. ELIMINAR LÍNEAS CON REFERENCIAS A IMÁGENES ===
    lineas = [l for l in lineas if not ("===== IMG_" in l and ".heic =====" in l)]

    nuevas_lineas = "\n".join(lineas)
    log_advertencias = ["TODO"]

    # === 2. AGREGAR NUMERACIÓN FALTANTE ===
    nuevas_lineas = corregir_numeracion_y_letras(nuevas_lineas)

    # === 3. CORREGIR LETRAS RARAS / DUPLICADAS ===
    nuevas_lineas = corregir_letras_duplicadas(nuevas_lineas)

    # === 4. INSERTAR LÍNEA VACÍA ENTRE CADA ITEM ===
    nuevas_lineas = insertar_linea_vacia_antes_numeracion(nuevas_lineas)

    # === 5. UNIR ORACIONES PARTIDAS ===
    nuevas_lineas = unir_oraciones_partidas(nuevas_lineas)

    # === 6. CORREGIR PALABRAS PARTIDAS CON GUIONES ===
    nuevas_lineas = unir_palabras_partidas_por_guiones(nuevas_lineas)

    # === 7. GUARDAR RESULTADOS ===
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for linea in nuevas_lineas.splitlines():
            f.write(linea + "\n")

    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in log_advertencias:
            f.write(advertencia + "\n")

    # === 8. MENSAJE FINAL EN CONSOLA ===
    print(f"\n✅ Archivo normalizado guardado como: {archivo_salida}")
    print(f"📝 Log de advertencias guardado como: {archivo_log}")


if __name__ == "__main__":
    main()
