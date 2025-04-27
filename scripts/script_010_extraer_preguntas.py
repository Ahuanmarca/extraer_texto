import pytesseract
from PIL import Image
import os
import shutil
from pillow_heif import register_heif_opener

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
IMAGENES_CRUDAS = os.path.join(BASE_DIR, "imagenes_crudas")
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")


def main(nombre_carpeta=None, nombre_archivo_log=None):
    register_heif_opener()

    carpeta_imagenes = os.path.join(IMAGENES_CRUDAS, nombre_carpeta)
    if not os.path.isdir(carpeta_imagenes):
        print(
            f"❌ La carpeta '{nombre_carpeta}' no existe dentro de 'imagenes_crudas/'."
        )
        exit(1)

    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")
    carpeta_memo = os.path.join(CARPETA_TRABAJO, "memo_ocr")
    os.makedirs(carpeta_memo, exist_ok=True)
    archivo_memo = os.path.join(carpeta_memo, f"{nombre_carpeta}_ocr.txt")

    # 🔵 Intentar cargar archivo memoizado
    if os.path.isfile(archivo_memo):
        print(f"⚡ Memo encontrado para {nombre_carpeta}, cargando texto...")
        with open(archivo_memo, "r", encoding="utf-8") as f:
            return f.read()

    # Si no hay memo, hacemos OCR normalmente
    carpeta_temporal = os.path.join(os.getcwd(), f"__tmp_{nombre_carpeta}")
    os.makedirs(carpeta_temporal, exist_ok=True)

    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write("Errores en extracción de imágenes:\n")

    procesadas = 0
    errores = 0
    texto_final = ""

    for nombre_archivo in sorted(os.listdir(carpeta_imagenes)):
        ruta_original = os.path.join(carpeta_imagenes, nombre_archivo)
        if not os.path.isfile(ruta_original):
            continue

        extension = os.path.splitext(nombre_archivo)[1].lower()
        if extension not in [".jpg", ".jpeg", ".png", ".heic"]:
            continue

        try:
            if extension == ".heic":
                imagen = Image.open(ruta_original)
                nombre_convertido = os.path.splitext(nombre_archivo)[0] + ".jpg"
                ruta_convertida = os.path.join(carpeta_temporal, nombre_convertido)
                imagen.convert("RGB").save(ruta_convertida, "JPEG")
            else:
                ruta_convertida = ruta_original

            print(f"Procesando {nombre_archivo}...")
            texto = pytesseract.image_to_string(Image.open(ruta_convertida), lang="spa")
            texto_final += f"===== {nombre_archivo} =====\n{texto}\n\n"
            procesadas += 1

        except Exception as e:
            errores += 1
            with open(archivo_log, "a", encoding="utf-8") as f:
                f.write(f"{nombre_archivo}: {str(e)}\n")
            print(f"⚠️ Error procesando {nombre_archivo}, registrado en el log.")

    if errores == 0:
        with open(archivo_log, "a", encoding="utf-8") as f:
            f.write("No se encontraron errores en la lectura de las imágenes.\n")

    shutil.rmtree(carpeta_temporal, ignore_errors=True)

    print("\n✅ Proceso terminado.")
    print(f"🖼️ Imágenes procesadas con éxito: {procesadas}")
    print(f"❌ Imágenes con error: {errores}")

    if errores > 0:
        print(f"📁 Revisa el log de errores en: {archivo_log}")

    # 🔵 Guardar texto extraído para futuras ejecuciones
    with open(archivo_memo, "w", encoding="utf-8") as f:
        f.write(texto_final)

    return texto_final


if __name__ == "__main__":
    texto_extraido = main()
    # Si quieres ver el texto extraído:
    # print(texto_extraido)
