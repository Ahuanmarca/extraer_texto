import os
import sys

from scripts import (
    script_010_extraer_preguntas as script_01,
    script_020_normalizar_preguntas as script_02,
    script_030_limpiar_guiones as script_03,
    script_040_comprobar_formato as script_04,
)

def limpiar_archivos_con_prefijo(prefijo="imagenes_prueba"):
    carpeta = "carpeta_trabajo"
    if not os.path.exists(carpeta):
        print("⚠️ La carpeta 'carpeta_trabajo/' no existe.")
        return

    archivos_eliminados = 0
    for archivo in os.listdir(carpeta):
        if archivo.startswith(prefijo):
            ruta = os.path.join(carpeta, archivo)
            os.remove(ruta)
            archivos_eliminados += 1

    print(f"🧹 Limpieza completada: {archivos_eliminados} archivo(s) eliminados que comienzan con '{prefijo}'.")

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

    if len(sys.argv) > 1 and sys.argv[1].strip().lower() == "clean":
        prefijo = sys.argv[2].strip() if len(sys.argv) > 2 else "imagenes_prueba"
        limpiar_archivos_con_prefijo(prefijo)
        return

    nombre_carpeta = obtener_nombre_carpeta()
    os.makedirs("carpeta_trabajo", exist_ok=True)

    # Nombres de archivos para cada script
    nombre_archivo_log = nombre_carpeta[:-1]
    nombre_salida_01 = nombre_carpeta + "_extr"             # filename_extr
    nombre_salida_02 = nombre_carpeta + "_extr_norm"        # filename_extr_norm
    nombre_salida_03 = nombre_carpeta + "_extr_norm_limp"   # filename_extr_norm_limp

    script_01.main(nombre_carpeta, nombre_salida_01, nombre_archivo_log)
    script_02.main(nombre_archivo=nombre_salida_01, nombre_salida=nombre_salida_02, nombre_archivo_log=nombre_archivo_log)
    script_03.main(nombre_archivo=nombre_salida_02, nombre_salida=nombre_salida_03, nombre_archivo_log=nombre_archivo_log)
    script_04.main(nombre_archivo=nombre_salida_03, nombre_archivo_log=nombre_archivo_log)

if __name__ == "__main__":
    main()
