import re

def limpiar_lineas_heic(texto):
    """
    Elimina líneas con nombres de imagen como '===== IMG_XXXX.heic ====='.
    """
    lineas = texto.splitlines()
    lineas_filtradas = [
        linea for linea in lineas
        if not re.match(r"^=+ IMG_\d+\.heic =+$", linea.strip())
    ]
    return "\n".join(lineas_filtradas)

