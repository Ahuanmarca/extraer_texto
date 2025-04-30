import re
from datetime import datetime


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


def insertar_espacio_tras_letra_y_parentesis_v2(texto: str) -> tuple[str, str]:
    """
    Inserta un espacio después de 'a)', 'b)', etc., solo si:
    - la línea comienza con 'a)', 'b)', etc., sin número, o
    - comienza con '1. a)', '12. c)', etc.
    Y si no hay espacio tras el paréntesis.
    Devuelve una tupla: (texto_modificado, log_cambios)
    """
    patron_sin_numero = re.compile(r"^([a-dA-D]\))(?=\S)")
    patron_con_numero = re.compile(r"^(\d{1,2}\. [a-dA-D]\))(?=\S)")

    lineas = texto.splitlines()
    nuevas_lineas = []
    log = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"=== Registro de inserciones de espacio generado el {timestamp} ===\n")

    for idx, linea in enumerate(lineas):
        nueva_linea = linea
        if patron_con_numero.match(linea):
            nueva_linea = patron_con_numero.sub(r"\1 ", linea)
        elif patron_sin_numero.match(linea):
            nueva_linea = patron_sin_numero.sub(r"\1 ", linea)

        if nueva_linea != linea:
            log.append(f"Línea {idx + 1}:")
            log.append(f"  Antes: {linea}")
            log.append(f"  Después: {nueva_linea}")
            log.append("")

        nuevas_lineas.append(nueva_linea)

    log.append("==========\n")
    log_texto = "\n".join(log)

    return "\n".join(nuevas_lineas), log_texto


# TODO: Hacer esta función más RESTRICTIVA.
def eliminar_basuritas_inicio(texto: str, basuritas: set[str]) -> str:
    """
    Elimina del inicio de cada línea las basuritas especificadas (solo si están al inicio exacto).
    Sólo elimina la primera ocurrencia de cada basurita en el inicio de la línea.
    """
    lineas = texto.splitlines()
    nuevas_lineas = []

    for linea in lineas:
        nueva_linea = linea
        for basurita in sorted(basuritas, key=len, reverse=True):  # Más largas primero
            if nueva_linea.startswith(basurita):
                nueva_linea = nueva_linea[len(basurita) :]
                break  # Solo eliminar una basurita por línea
        nuevas_lineas.append(nueva_linea)

    return "\n".join(nuevas_lineas)


# def reemplazar_inicio_linea(texto: str, reemplazos: list[tuple[str, str]]) -> str:
#     """
#     Reemplaza múltiples patrones en los primeros 8 caracteres de cada línea.

#     Args:
#         texto (str): Texto multilinea.
#         reemplazos (list[tuple[str, str]]): Lista de tuplas (buscar, reemplazar).

#     Returns:
#         str: Texto modificado.
#     """
#     lineas = texto.splitlines()
#     nuevas_lineas = []

#     for linea in lineas:
#         rango_busqueda = linea[:8]  # máximo 8 caracteres (o menos si la línea es corta)
#         nueva_linea = linea

#         for buscar, reemplazar in reemplazos:
#             idx = rango_busqueda.find(buscar)
#             if idx != -1:
#                 nueva_linea = (
#                     nueva_linea[:idx] + reemplazar + nueva_linea[idx + len(buscar) :]
#                 )
#                 break  # Solo aplicar el primer reemplazo que se encuentre

#         nuevas_lineas.append(nueva_linea)

#     return "\n".join(nuevas_lineas)


def reemplazar_inicio_linea(texto: str, reemplazos: list[tuple[str, str]]) -> str:
    """
    Reemplaza múltiples patrones en el inicio de cada línea, ampliando el rango de búsqueda
    según la longitud del patrón más largo.

    Args:
        texto (str): Texto multilinea.
        reemplazos (list[tuple[str, str]]): Lista de tuplas (buscar, reemplazar).

    Returns:
        str: Texto modificado.
    """
    # Calcular el largo máximo de los patrones a buscar
    max_len = max((len(buscar) for buscar, _ in reemplazos), default=8)

    lineas = texto.splitlines()
    nuevas_lineas = []

    for linea in lineas:
        rango_busqueda = linea[:max_len]
        nueva_linea = linea

        for buscar, reemplazar in reemplazos:
            idx = rango_busqueda.find(buscar)
            if idx != -1:
                nueva_linea = (
                    nueva_linea[:idx] + reemplazar + nueva_linea[idx + len(buscar) :]
                )
                break  # Solo aplicar el primer reemplazo que se encuentre

        nuevas_lineas.append(nueva_linea)

    return "\n".join(nuevas_lineas)


def reemplazar_linea(texto_multilinea, texto_a_buscar, texto_reemplazo):
    lineas = texto_multilinea.splitlines()
    nuevas_lineas = [
        texto_reemplazo if texto_a_buscar in linea else linea for linea in lineas
    ]
    return "\n".join(nuevas_lineas)


def agregar_numeracion_respuestas_v2(texto: str):
    """
    Agrega numeración a respuestas huérfanas (tipo a), b), c), d)) siguiendo reglas explicadas.
    Retorna (texto_modificado, log_cambios).
    """
    # Patrones
    patron_numeracion = re.compile(r"^(\d{1,2})\.\s+[a-d]\)\s+")
    patron_letra_sola = re.compile(r"^[a-d]\)\s+")

    lineas = texto.splitlines()

    # Estados
    cambios = {}
    huérfanas = []
    ultimo_numero = 0
    log = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"=== Registro de numeración generado el {timestamp} ===\n")

    for idx, linea in enumerate(lineas):
        linea_strip = linea.lstrip()

        # ¿Es numeración?
        m_num = patron_numeracion.match(linea_strip)
        if m_num:
            num_actual = int(m_num.group(1))

            if huérfanas:
                esperado = ultimo_numero + len(huérfanas) + 1
                if num_actual == esperado:
                    for i, idx_huerfana in enumerate(huérfanas):
                        nuevo_num = ultimo_numero + i + 1
                        cambios[idx_huerfana] = nuevo_num
                    log.append(
                        f"Se numeraron {len(huérfanas)} respuestas huérfanas antes de la línea {idx+1}."
                    )
                else:
                    log.append(
                        f"Se descartaron {len(huérfanas)} respuestas huérfanas antes de la línea {idx+1} (falsa alarma)."
                    )
                huérfanas.clear()

            if num_actual > ultimo_numero:
                ultimo_numero = num_actual
            else:
                log.append(
                    f"Número descendente ignorado en línea {idx+1}: {num_actual}"
                )

            continue

        # ¿Es letra sola huérfana?
        m_let = patron_letra_sola.match(linea_strip)
        if m_let:
            huérfanas.append(idx)

    # Si al final quedan huérfanas sin numerar, numerarlas igual
    if huérfanas:
        for i, idx_huerfana in enumerate(huérfanas):
            nuevo_num = ultimo_numero + i + 1
            cambios[idx_huerfana] = nuevo_num
        log.append(
            f"Se numeraron {len(huérfanas)} respuestas huérfanas al final del documento."
        )

    # Segunda pasada: aplicar cambios
    nuevas_lineas = []
    for idx, linea in enumerate(lineas):
        if idx in cambios:
            numero = cambios[idx]
            nueva_linea = f"{numero}. {linea.lstrip()}"
            nuevas_lineas.append(nueva_linea)
        else:
            nuevas_lineas.append(linea)

    texto_modificado = "\n".join(nuevas_lineas)
    log.append("==========\n")

    return texto_modificado, "\n".join(log)


import re


def unir_oraciones_partidas_v3(texto):
    lineas = texto.splitlines()
    resultado = []

    # Patrones de líneas que indican que NO deben unirse con la anterior
    patrones_exclusion = [
        r"^\d+\. [a-z]\) ",  # 1. c) ...
        r"^P\d+ - ",  # P1 - ...
        r"^-{1,2} ",  # - o -- seguido de espacio
        r"^-> [a-z]\)",  # -> b)
        r"^\d+\.\d+\.\d+\. ",  # 3.1.2.
    ]
    patrones_exclusion = [re.compile(p) for p in patrones_exclusion]

    # Puntuación fuerte que indica final de oración
    patron_fin_oracion = re.compile(r"[.:!?]$")

    buffer = ""

    for linea in lineas:
        linea_strip = linea.strip()

        if not linea_strip:
            # Línea vacía
            if buffer:
                buffer += " "
            continue

        es_exclusion = any(p.match(linea_strip) for p in patrones_exclusion)
        termina_oracion = patron_fin_oracion.search(buffer.strip()) if buffer else False

        if buffer and (termina_oracion or es_exclusion):
            # Si la oración anterior terminó o la actual empieza con patrón prohibido
            resultado.append(buffer.strip())
            buffer = linea_strip
        elif buffer:
            # Se puede unir con la línea anterior
            buffer += " " + linea_strip
        else:
            buffer = linea_strip

    if buffer:
        resultado.append(buffer.strip())

    return "\n".join(resultado)


import re


def insertar_espacios_en_titulos_v1(texto):
    lineas = texto.splitlines()
    resultado = []
    patron = re.compile(r"^\d+\. [a-z]\) ")

    primera_ocurrencia = True

    for linea in lineas:
        if patron.match(linea):
            if not primera_ocurrencia:
                resultado.append("")  # línea vacía antes
            resultado.append(linea)
            resultado.append("")  # línea vacía después
            primera_ocurrencia = False
        else:
            resultado.append(linea)

    return "\n".join(resultado)
