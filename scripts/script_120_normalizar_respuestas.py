import re
import os
from collections import Counter
from funciones.debug import guardar_texto_con_timestamp
from funciones.normalizadores import corregir_numeracion_y_letras
from funciones.normalizadores import corregir_letras_duplicadas
from funciones.normalizadores import insertar_linea_vacia_antes_numeracion
from funciones.normalizadores import unir_oraciones_partidas
from funciones.normalizadores import unir_palabras_partidas_por_guiones
from funciones.normalizadores import reemplazar_texto_por_linea_vacia
from funciones.normalizadores import insertar_espacio_entre_punto_y_letra
from funciones.normalizadores import unir_numeracion_con_letra
from funciones.normalizadores import corregir_numeracion_preguntas_reserva
from funciones.normalizadores import insertar_espacio_tras_letra_y_parentesis

DEBUG = False

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")


def main(texto, nombre_archivo_log=None):
    # def main(nombre_archivo=None, nombre_salida=None, nombre_archivo_log=None):
    # archivo_entrada = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo}.txt")
    # archivo_salida = os.path.join(CARPETA_TRABAJO, f"{nombre_salida}.txt")
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")

    # === LECTURA DE LÍNEAS === <-- Se omiten líneas vacías
    # with open(archivo_entrada, "r", encoding="utf-8") as f:
    # lineas = [line.rstrip() for line in f if line.strip()]

    # === 0. LIMPIAR LÍNEAS VACÍAS Y ESPACIOS AL FINAL DE LÍNEAS ===
    lineas = [line.rstrip() for line in texto.splitlines() if line.strip()]

    # === 1. ELIMINAR LÍNEAS CON REFERENCIAS A IMÁGENES ===
    lineas = [l for l in lineas if not ("===== IMG_" in l and ".heic =====" in l)]

    nuevas_lineas = "\n".join(lineas)
    log_advertencias = ["TODO"]

    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "referencia_imagenes")

    # === 1b. INSERTAR ESPACIO ENTRE PUNTO Y LETRAS ===
    nuevas_lineas = insertar_espacio_entre_punto_y_letra(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "espacio_entre_punto_y_letra")

    # === 1c. UNIR NUMERACIÓN CON LETRA PARTIDOS POR SALTO DE LINEA ===
    nuevas_lineas = unir_numeracion_con_letra(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "unir_numeracion_con_letra")

    # === 1d. INSERTAR ESPACIO ENTRE LETRA Y TEXTO ===
    nuevas_lineas = insertar_espacio_tras_letra_y_parentesis(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "espacio_tras_letra_parentesis")

    # === 2. AGREGAR NUMERACIÓN FALTANTE ===
    nuevas_lineas = corregir_numeracion_y_letras(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "numeracion")

    # === 3. CORREGIR LETRAS RARAS / DUPLICADAS ===
    nuevas_lineas = corregir_letras_duplicadas(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "letras")

    # === 3b. CORREGIR NUMERACIÓN PREGUNTAS RESERVA ===
    nuevas_lineas = corregir_numeracion_preguntas_reserva(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "preguntas_reserva")

    # === 4. INSERTAR LÍNEA VACÍA ENTRE CADA ITEM ===
    nuevas_lineas = insertar_linea_vacia_antes_numeracion(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "insertar_lineas")

    # === 4b. INSERTAR LÍNEA VACÍA EN "Preguntas de reserva" ===
    nuevas_lineas = reemplazar_texto_por_linea_vacia(
        nuevas_lineas, "Preguntas de reserva"
    )
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "limpiar_str_preguntas_reserva")

    # === 5. UNIR ORACIONES PARTIDAS ===
    nuevas_lineas = unir_oraciones_partidas(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "unir_oraciones")

    # === 6. CORREGIR PALABRAS PARTIDAS CON GUIONES ===
    nuevas_lineas = unir_palabras_partidas_por_guiones(nuevas_lineas)
    if DEBUG:
        guardar_texto_con_timestamp(nuevas_lineas, "unir_palabras")

    # === 7. GUARDAR RESULTADOS ===
    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in log_advertencias:
            f.write(advertencia + "\n")

    # === 8. MENSAJE FINAL EN CONSOLA ===
    print(f"📝 Log de advertencias guardado como: {archivo_log}")

    return nuevas_lineas


if __name__ == "__main__":
    main()
