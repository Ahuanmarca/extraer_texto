import pytesseract
from PIL import Image
import os
import shutil
from pillow_heif import register_heif_opener

def main():
    register_heif_opener()

    # Preguntar al usuario el nombre de la carpeta
    nombre_carpeta = input("Introduce el nombre de la carpeta con las imágenes: ").strip()

    # Ruta a la carpeta (se asume que está en el mismo nivel que el script)
    carpeta_imagenes = os.path.join(os.getcwd(), "imagenes_crudas", nombre_carpeta)

    # Verificar que la carpeta exista
    if not os.path.isdir(carpeta_imagenes):
        print(f"❌ La carpeta '{nombre_carpeta}' no existe en el mismo nivel que el script.")
        exit(1)

    # Archivos de salida
    archivo_salida = os.path.join(os.getcwd(), f"carpeta_trabajo/{nombre_carpeta}_extr.txt")
    archivo_log = os.path.join(os.getcwd(), f"carpeta_trabajo/{nombre_carpeta}.log")

    # Crear carpeta temporal para conversiones
    carpeta_temporal = os.path.join(os.getcwd(), f"__tmp_{nombre_carpeta}")
    os.makedirs(carpeta_temporal, exist_ok=True)

    # Limpiar archivos anteriores
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('')
    with open(archivo_log, 'w', encoding='utf-8') as f:
        f.write('Errores en extracción de imágenes:\n')

    # Contadores
    procesadas = 0
    errores = 0

    # Recorre todas las imágenes de la carpeta
    for nombre_archivo in sorted(os.listdir(carpeta_imagenes)):
        ruta_original = os.path.join(carpeta_imagenes, nombre_archivo)

        if not os.path.isfile(ruta_original):
            continue

        extension = os.path.splitext(nombre_archivo)[1].lower()

        if extension not in ['.jpg', '.jpeg', '.png', '.heic']:
            continue

        try:
            # Si es .heic, convertir a .jpg en la carpeta temporal
            if extension == '.heic':
                imagen = Image.open(ruta_original)
                nombre_convertido = os.path.splitext(nombre_archivo)[0] + '.jpg'
                ruta_convertida = os.path.join(carpeta_temporal, nombre_convertido)
                imagen.convert("RGB").save(ruta_convertida, "JPEG")
            else:
                ruta_convertida = ruta_original

            print(f'Procesando {nombre_archivo}...')
            texto = pytesseract.image_to_string(Image.open(ruta_convertida), lang='spa')

            with open(archivo_salida, 'a', encoding='utf-8') as f:
                f.write(f"===== {nombre_archivo} =====\n")
                f.write(texto)
                f.write("\n\n")

            procesadas += 1

        except Exception as e:
            errores += 1
            with open(archivo_log, 'a', encoding='utf-8') as f:
                f.write(f"{nombre_archivo}: {str(e)}\n")
            print(f'⚠️ Error procesando {nombre_archivo}, registrado en el log.')

    if errores == 0:
        with open(archivo_log, 'a', encoding='utf-8') as f:
            f.write("No se encontraron errores en la lectura de las imágenes.\n")

    # Eliminar carpeta temporal
    shutil.rmtree(carpeta_temporal, ignore_errors=True)

    # Resumen final
    print("\n✅ Proceso terminado.")
    print(f"📄 Texto extraído guardado en: {archivo_salida}")
    print(f"🖼️ Imágenes procesadas con éxito: {procesadas}")
    print(f"❌ Imágenes con error: {errores}")

    if errores > 0:
        print(f"📁 Revisa el log de errores en: {archivo_log}")
    
if __name__ == "__main__":
    main()
