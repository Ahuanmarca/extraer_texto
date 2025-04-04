import os
import sys

from scripts import (
    script_01_extraer_preguntas as script_01,
    script_02_normalizar_preguntas as script_02,
    script_03_limpiar_guiones as script_03,
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

    script_01.main(nombre_carpeta)
    script_02.main(nombre_archivo=nombre_carpeta)
    script_03.main(nombre_archivo=nombre_carpeta)

if __name__ == "__main__":
    main()
