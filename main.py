import os
import sys

from scripts import (
    script_01_extraer_preguntas as script_01,
    script_02_normalizar_preguntas as script_02,
    script_03_limpiar_guiones as script_03,
    script_04_comprobar_formato as script_04,
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

    script_01.main(nombre_carpeta)
    script_02.main(nombre_archivo=nombre_carpeta)
    script_03.main(nombre_archivo=nombre_carpeta)
    script_04.main(nombre_archivo=nombre_carpeta)

if __name__ == "__main__":
    main()
