import re


def eliminar_referencias_imagen(texto: str) -> str:
    """
    Elimina las líneas que contienen referencias a imágenes tipo '===== IMG_xxxx.heic ====='.
    No elimina líneas vacías ni modifica el resto del texto.
    """
    lineas = texto.splitlines()
    lineas_filtradas = [
        linea
        for linea in lineas
        if not ("===== IMG_" in linea and ".heic =====" in linea)
    ]
    return "\n".join(lineas_filtradas)


def eliminar_basurita_suelta(texto: str, basuritas: set = None) -> str:
    """
    Elimina líneas que:
    - Son solo una letra con paréntesis (como a), Cc)).
    - Son solo una numeración suelta (como 1, 4., 50).
    - Coinciden exactamente (tras strip) con algún string en un set de basuritas.

    No elimina:
    - Líneas solo porque tengan 1 o 2 palabras.
    - Líneas que tengan más contenido junto a la numeración o letra.
    """
    if basuritas is None:
        basuritas = set()

    nuevas_lineas = []
    lineas = texto.splitlines()

    patron_letra_parentesis = re.compile(r"^\s*[a-zA-Z]{1,2}\)\s*$")
    patron_numeracion = re.compile(r"^\s*\d+\.?\s*$")

    for linea in lineas:
        contenido = linea.strip()

        if not contenido:
            nuevas_lineas.append(linea)
            continue

        # Eliminar si coincide con letra+paréntesis
        if patron_letra_parentesis.match(contenido):
            print(f"⏩ Eliminada letra con paréntesis: '{contenido}'")
            continue

        # Eliminar si coincide con numeración suelta
        if patron_numeracion.match(contenido):
            print(f"⏩ Eliminada numeración suelta: '{contenido}'")
            continue

        # Eliminar si coincide exactamente con alguna basurita
        if contenido in basuritas:
            print(f"⏩ Eliminada basurita específica: '{contenido}'")
            continue

        # Si no se eliminó, conservar la línea
        nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas)


# TODO: Que sólo busque y transforme en inicios de línea.
def insertar_espacio_tras_letra_y_parentesis_v2(texto: str) -> str:
    """
    Inserta un espacio después de un paréntesis de opciones tipo 'a)', 'b)', 'c)', 'd)', pero sólo si aparecen al INICIO de la línea.
    """
    patron = re.compile(r"^([a-dA-D]{1,2}\))(?=\S)")

    lineas = texto.splitlines()
    nuevas_lineas = []

    for linea in lineas:
        nueva_linea = patron.sub(r"\1 ", linea)
        nuevas_lineas.append(nueva_linea)

    return "\n".join(nuevas_lineas)
