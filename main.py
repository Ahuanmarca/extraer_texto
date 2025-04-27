import os
import sys

from scripts import (
    script_010_extraer_preguntas as script_010,
    script_020_normalizar_preguntas as script_020,
    script_040_comprobar_formato as script_040,
    script_010_extraer_preguntas as script_110,
    script_120_normalizar_respuestas as script_120,
)


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
    script_010.main(nombre_carpeta, salida_01, nombre_archivo_log)

    # Normalizar estructura del texto
    script_020.main(
        nombre_archivo=salida_01,
        nombre_salida=salida_02,
        nombre_archivo_log=nombre_archivo_log,
    )

    # Buscar errores y marcarlos con "=== TO FIX ==="
    script_040.main(nombre_archivo=salida_02, nombre_archivo_log=nombre_archivo_log)

    # Extraer texto de imágenes crudas (de respuestas)
    script_110.main(
        nombre_carpeta[:-1] + "B", salida_11, nombre_archivo_log=nombre_archivo_log
    )

    # Normalizar texto de respuestas
    script_120.main(
        nombre_archivo=salida_11,
        nombre_salida=salida_12,
        nombre_archivo_log=nombre_archivo_log,
    )


if __name__ == "__main__":
    main()
