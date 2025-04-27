import os
import sys

from scripts import (
    script_010_extraer_preguntas as script_010,
    script_020_normalizar_preguntas as script_020,
    script_040_comprobar_formato as script_040,
    script_010_extraer_preguntas as script_110,
    script_120_normalizar_respuestas as script_120,
    script_210_combinar_preguntas_respuestas as script_210,
)

from funciones.debug import guardar_texto_con_timestamp

DEBUG = True


def obtener_nombre_carpeta():
    # 1. Comprobar si se pasó como argumento
    if len(sys.argv) > 1:
        nombre = sys.argv[1].strip()
    else:
        nombre = input("Introduce el nombre de la carpeta de imágenes: ").strip()

    # 2. Verificar si existe dentro de 'imagenes_crudas/'
    ruta = os.path.join("imagenes_crudas", nombre)
    if not os.path.isdir(ruta):
        print(f"❌ La carpeta '{nombre}' no existe dentro de 'imagenes_crudas/'.")
        sys.exit(1)

    return nombre


def main():
    nombre_carpeta = obtener_nombre_carpeta()
    os.makedirs("carpeta_trabajo", exist_ok=True)

    # Nombre de archivo log
    nombre_archivo_log = nombre_carpeta[:-1]

    # Nombres de archivos de trabajo
    salida_01 = nombre_carpeta + "_010"  # filename_010
    salida_02 = nombre_carpeta + "_020"  # filename_020

    salida_11 = nombre_carpeta + "_110"  # filename_110
    salida_12 = nombre_carpeta + "_120"  # filename_120

    # Extraer texto de imágenes crudas
    texto_preguntas = script_010.main(nombre_carpeta, nombre_archivo_log)
    if DEBUG:
        guardar_texto_con_timestamp(texto_preguntas, "01_extraer_preguntas")

    # Normalizar estructura del texto
    texto_preguntas = script_020.main(
        texto_preguntas,
        nombre_archivo_log=nombre_archivo_log,
    )
    if DEBUG:
        guardar_texto_con_timestamp(texto_preguntas, "02_normalizar_preguntas")

    # Extraer texto de imágenes crudas (de respuestas)
    texto_respuestas = script_110.main(
        nombre_carpeta[:-1] + "B", nombre_archivo_log=nombre_archivo_log
    )
    if DEBUG:
        guardar_texto_con_timestamp(texto_respuestas, "04_extraer_respuestas")

    # Normalizar texto de respuestas
    texto_respuestas = script_120.main(
        texto_respuestas,
        nombre_archivo_log=nombre_archivo_log,
    )
    if DEBUG:
        guardar_texto_con_timestamp(texto_respuestas, "05_normalizar_respuestas")

    # Combinar preguntas y respuesta en un único archivo
    preguntas_respuestas = script_210.main(texto_preguntas, texto_respuestas)
    if DEBUG:
        guardar_texto_con_timestamp(preguntas_respuestas, "06_preguntas_respuestas")

    # Buscar errores y marcarlos con "=== TO FIX ==="
    preguntas_respuestas = script_040.main(
        preguntas_respuestas, nombre_archivo_log=nombre_archivo_log
    )
    if DEBUG:
        guardar_texto_con_timestamp(preguntas_respuestas, "07_marcar_errores")

    # === GUARDAR ARCHIVO FINAL ===
    output_dir = os.path.join("carpeta_trabajo", "output")
    os.makedirs(output_dir, exist_ok=True)

    ruta_salida_final = os.path.join(output_dir, f"{nombre_carpeta}.txt")

    with open(ruta_salida_final, "w", encoding="utf-8") as f:
        f.write(preguntas_respuestas)

    print(f"\n✅ Archivo final guardado en: {ruta_salida_final}")


if __name__ == "__main__":
    main()
