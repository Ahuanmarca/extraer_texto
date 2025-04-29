import re
import os
from collections import Counter
from funciones.debug import guardar_texto_con_timestamp
from funciones.normalizadores import corregir_numeracion_y_letras
from funciones.normalizadores import corregir_letras_duplicadas
from funciones.normalizadores import insertar_linea_vacia_antes_numeracion
from funciones.normalizadores import unir_oraciones_partidas
from funciones.normalizadores import unir_oraciones_partidas_v2
from funciones.normalizadores import unir_palabras_partidas_por_guiones
from funciones.normalizadores import reemplazar_texto_por_linea_vacia
from funciones.normalizadores import insertar_espacio_entre_punto_y_letra
from funciones.normalizadores import unir_numeracion_con_letra
from funciones.normalizadores import corregir_numeracion_preguntas_reserva
from funciones.normalizadores import insertar_espacio_tras_letra_y_parentesis
from funciones.normalizadores import agregar_numeracion_a_respuestas_huerfanas
from funciones.normalizadores import eliminar_numeraciones_huerfanas
from funciones.normalizadores import reemplazar_letras_en_bloques

# NORMALIZADORES V2
from funciones.normalizadores_v2 import eliminar_referencias_imagen
from funciones.normalizadores_v2 import eliminar_basurita_suelta
from funciones.normalizadores_v2 import insertar_espacio_tras_letra_y_parentesis_v2

DEBUG = False

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")


def main(texto, nombre_archivo_log=None):
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")
    log_advertencias = []
    nuevas_lineas = texto

    # === 1. ELIMINAR LÍNEAS CON REFERENCIAS A IMÁGENES ===
    nuevas_lineas = eliminar_referencias_imagen(texto)
    nuevas_lineas = eliminar_basurita_suelta(nuevas_lineas, {"Ue", "*", "59%", "e", "\"", "24,", "L", "9;", "19;", "32:", "SEL", "(6)"})
    # TODO: Eliminar basuritas a inicios de lineas.
    # TODO: Eliminar basuritas al final de lineas.
    nuevas_lineas = insertar_espacio_tras_letra_y_parentesis_v2(nuevas_lineas) # <-- Aún inserta en finales de líneas. TODO: Corregir.
    # TODO: Insertar espacio luego del punto de la numeración, cunado falta.
    # nuevas_lineas = corregir_letras_duplicadas(nuevas_lineas)
    
    guardar_texto_con_timestamp(nuevas_lineas, "PRE")
    guardar_texto_con_timestamp(nuevas_lineas, "POST")

    # nuevas_lineas = insertar_espacio_entre_punto_y_letra(nuevas_lineas)
    # nuevas_lineas, log_lines = eliminar_numeraciones_huerfanas(nuevas_lineas)
    # nuevas_lineas = unir_oraciones_partidas_v2(nuevas_lineas)
    # nuevas_lineas = reemplazar_letras_en_bloques(nuevas_lineas)
    # nuevas_lineas = agregar_numeracion_a_respuestas_huerfanas(nuevas_lineas)
    # nuevas_lineas = corregir_numeracion_y_letras(nuevas_lineas)
    # nuevas_lineas = corregir_numeracion_preguntas_reserva(nuevas_lineas)
    # nuevas_lineas = insertar_linea_vacia_antes_numeracion(nuevas_lineas)
    # nuevas_lineas = reemplazar_texto_por_linea_vacia(
        # nuevas_lineas, "Preguntas de reserva"
    # )
    # nuevas_lineas, log_lines = unir_palabras_partidas_por_guiones(nuevas_lineas)

    # === 7. GUARDAR RESULTADOS ===
    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in log_advertencias:
            f.write(advertencia + "\n")

    return nuevas_lineas


if __name__ == "__main__":
    main()
