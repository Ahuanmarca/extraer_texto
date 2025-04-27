import os
import re
import json

# === BASE_DIR: carpeta raíz del proyecto ===
# Rutas usadas por unir_palabras_partidas_por_guiones
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
RECHAZADAS_PATH = os.path.join(BASE_DIR, "rechazadas.json")


def limpiar_lineas_heic(texto):
    """
    Elimina líneas con nombres de imagen como '===== IMG_XXXX.heic ====='.
    """
    # lineas = texto.splitlines()
    lineas = texto
    lineas_filtradas = [
        linea
        for linea in lineas
        if not re.match(r"^=+ IMG_\d+\.heic =+$", linea.strip())
    ]
    return "\n".join(lineas_filtradas)


def insertar_espacio_entre_punto_y_letra(texto: str) -> str:
    """
    Inserta un espacio después del punto en numeraciones tipo '1.a)', '24.c)', etc.
    No modifica nada más en el texto.
    """
    lineas = texto.splitlines()
    nuevas_lineas = []

    patron = re.compile(r"^(\d+)\.([a-dA-D]\))")  # Número, punto, letra y paréntesis

    for linea in lineas:
        nueva_linea = patron.sub(r"\1. \2", linea)
        nuevas_lineas.append(nueva_linea)

    return "\n".join(nuevas_lineas)


def unir_numeracion_con_letra(texto: str) -> str:
    """
    Une numeraciones que quedaron separadas de la opción.
    Ejemplo:
    1.
    a) Lorem Ipsum
    → 1. a) Lorem Ipsum
    """
    lineas = texto.splitlines()
    resultado = []
    i = 0

    while i < len(lineas):
        linea = lineas[i].rstrip()

        if re.match(r"^\d+\.$", linea) and i + 1 < len(lineas):
            siguiente = lineas[i + 1].lstrip()

            match_opcion = re.match(r"^([A-Za-z]{1,2})\)", siguiente)
            if match_opcion:
                letra = match_opcion.group(1).lower()[
                    -1
                ]  # Solo la última letra y minúscula
                resto = siguiente[len(match_opcion.group(0)) :].lstrip()
                nueva_linea = f"{linea[:-1]}. {letra}) {resto}"
                resultado.append(nueva_linea)
                i += 2
                continue

        resultado.append(linea)
        i += 1

    return "\n".join(resultado)


def insertar_espacio_tras_letra_y_parentesis(texto: str) -> str:
    """
    Inserta un espacio después del paréntesis de opciones tipo 'a)', 'b)', 'c)', 'd)' si no existe.
    Aplica en cualquier parte de la línea.
    """

    patron = re.compile(r"([a-dA-D])[a-dA-D]?\)(?=\S)")

    lineas = texto.splitlines()
    nuevas_lineas = []

    for linea in lineas:
        nueva_linea = patron.sub(lambda m: m.group(0) + " ", linea)
        nuevas_lineas.append(nueva_linea)

    return "\n".join(nuevas_lineas)


def reemplazar_texto_por_linea_vacia(texto, texto_objetivo):
    """
    Reemplaza ocurrencias de un marcador en el texto por una línea vacía.
    Si el marcador aparece dentro de una línea, divide la línea en dos partes, inserta una línea vacía en medio.

    Args:
        texto (str): El texto completo a procesar.
        marcador (str): El string que se debe reemplazar por una línea vacía.

    Returns:
        str: El texto modificado.
    """
    lineas = texto.splitlines()
    nuevas_lineas = []

    for linea in lineas:
        if texto_objetivo in linea:
            partes = linea.split(texto_objetivo)
            for idx, parte in enumerate(partes):
                if parte.strip():
                    nuevas_lineas.append(parte.strip())
                if idx < len(partes) - 1:
                    nuevas_lineas.append("")  # insertar línea vacía
        else:
            nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas)


def eliminar_numeraciones_huerfanas(texto: str) -> str:
    """
    Elimina líneas que consisten únicamente en una numeración (número, opcionalmente seguido de un punto).
    """
    lineas = texto.splitlines()
    nuevas_lineas = []
    log_lines = []
    
    patron_huerfana = re.compile(r"^\s*\d+\.?\s*$")

    for linea in lineas:
        if patron_huerfana.match(linea):
            # print(f"⏩ Eliminada numeración huérfana: '{linea.strip()}'")
            log_lines.append(f"⏩ Eliminada numeración huérfana: '{linea.strip()}'")
            continue
        nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas), log_lines


def reemplazar_letras_en_bloques(texto: str) -> str:
    """
    Reemplaza letras a), b), c), d) por guiones solo si la línea anterior o siguiente también empieza igual.
    """
    lineas = texto.splitlines()
    nuevas_lineas = []

    patron_letra = re.compile(r"^[a-dA-D]\)")

    for i, linea in enumerate(lineas):
        linea_actual_es_letra = bool(patron_letra.match(linea.strip()))

        linea_anterior_es_letra = (
            i > 0 and bool(patron_letra.match(lineas[i - 1].strip()))
        )
        linea_siguiente_es_letra = (
            i < len(lineas) - 1 and bool(patron_letra.match(lineas[i + 1].strip()))
        )

        if linea_actual_es_letra and (linea_anterior_es_letra or linea_siguiente_es_letra):
            # Reemplazar la letra inicial por un guion
            nueva_linea = re.sub(r"^([a-dA-D]\))", "-", linea, count=1)
            nuevas_lineas.append(nueva_linea)
        else:
            nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas)


## NUEVA VERSIÓN DE AGREGAR NUMERACIÓN, QUE FUNCIONA CON MUCHAS
## RESPUESTAS HUÉRFANAS AL INICIO DEL ARCHIVO
def agregar_numeracion_a_respuestas_huerfanas(texto: str) -> str:
    """
    Agrega numeración faltante a respuestas huérfanas que empiezan con letras como 'a)', 'Cc)', etc.
    Respeta las líneas que ya tienen numeración correcta.
    """

    # === Primera pasada: detectar bloques importantes (letras huérfanas y numeradas correctas) ===
    eventos = []  # Ejemplo: [('huérfana', 'a)'), ('huérfana', 'b)'), ('numerada', 10), ...]

    patron_huerfana = re.compile(r"^\s*([a-dA-D]{1,2})\)")
    patron_numerada = re.compile(r"^\s*(\d+)\.\s*([a-dA-D]{1,2})\)")

    lineas = texto.splitlines()

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        match_num = patron_numerada.match(linea)
        if match_num:
            numero = int(match_num.group(1))
            eventos.append(('numerada', numero))
            continue

        match_huerfana = patron_huerfana.match(linea)
        if match_huerfana:
            eventos.append(('huérfana', match_huerfana.group(1).lower()))
            continue

    # === Construir la lista de numeraciones que usaremos ===
    numeraciones = []
    siguiente_num = 1

    for tipo, dato in eventos:
        if tipo == 'huérfana':
            numeraciones.append(siguiente_num)
            siguiente_num += 1
        elif tipo == 'numerada':
            numeraciones.append(dato)
            siguiente_num = dato + 1  # Nos sincronizamos al número real encontrado

    # === Segunda pasada: aplicar numeración a las huérfanas ===
    nuevas_lineas = []
    idx_numeracion = 0

    for linea in lineas:
        original = linea.rstrip()

        # Caso 1: línea numerada correcta, solo copiar
        if patron_numerada.match(original):
            nuevas_lineas.append(original)
            idx_numeracion += 1
            continue

        # Caso 2: línea con letra huérfana, agregar numeración
        match_huerfana = patron_huerfana.match(original)
        if match_huerfana:
            letra = match_huerfana.group(1).lower()
            resto = original[len(match_huerfana.group(0)):].lstrip()
            numero = numeraciones[idx_numeracion]
            nueva_linea = f"{numero}. {letra}) {resto}"
            nuevas_lineas.append(nueva_linea)
            idx_numeracion += 1
            continue

        # Caso 3: línea normal, no tocar
        nuevas_lineas.append(original)

    return "\n".join(nuevas_lineas)


# Agregar numeración faltante a RESPUESTAS extraídas de imágenes crudas
# ... no usar para normalizar las preguntas, posiblemente funcione mal
def corregir_numeracion_y_letras(texto: str) -> str:
    lineas = texto.splitlines()

    # Paso 1: recolectar numeraciones existentes
    numeracion_pat = re.compile(r"^(\d+)\.\s")
    numeros_existentes = []

    for linea in lineas:
        match = numeracion_pat.match(linea)
        if match:
            numeros_existentes.append(int(match.group(1)))

    # Paso 2: recorrer el texto e insertar numeración faltante
    resultado = []
    i = 0
    modo_corregir = False
    siguiente_idx = 0
    bloque_actual = None
    numero_en_progreso = 0

    while i < len(lineas):
        linea = lineas[i]
        match = numeracion_pat.match(linea)

        if match:
            bloque_actual = int(match.group(1))
            resultado.append(linea)
            i += 1

            # Ver si el siguiente número es consecutivo
            if siguiente_idx < len(numeros_existentes) - 1:
                numero_esperado = numeros_existentes[siguiente_idx + 1]
                if numero_esperado == bloque_actual + 1:
                    modo_corregir = False
                else:
                    modo_corregir = True
                    numero_en_progreso = bloque_actual + 1
                siguiente_idx += 1
            else:
                modo_corregir = True
                numero_en_progreso = bloque_actual + 1
            continue

        if modo_corregir:
            # Detectar letras tipo "a)", "Cc)", etc.
            match_opcion = re.match(r"^([A-Za-z]{1,2})\)", linea.strip())
            if match_opcion:
                letra = match_opcion.group(1).lower()[-1]  # tomar última letra válida
                if letra in "abcd":

                    # <<<< TODO: Hacer esta funcionalidad configurable !!!!
                    # <<<< EXCEPCIÓN PARA NUMERACIÓN DE RESPUESTAS DE PREGUNTAS DE RESERVA
                    # if numero_en_progreso <= 4 and bloque_actual == 60:
                    # numero_en_progreso += 60
                    # <<<< FIN DE EXCEPCIÓN

                    nueva_linea = f"{numero_en_progreso}. {letra}) {linea.strip()[len(match_opcion.group(0)):].strip()}"
                    resultado.append(nueva_linea)
                    numero_en_progreso += 1
                    i += 1
                    continue

        resultado.append(linea)
        i += 1

    return "\n".join(resultado)


# OJO, función diseñada para normalizar RESPUESTAS, pero podría funcionar OK
# para normalizar preguntas, usándola en el momento correcto. TODO: ¡Probar!
def corregir_letras_duplicadas(texto: str) -> str:
    """
    Corrige errores de letras duplicadas (como 'Cc)') justo después de una numeración.
    La numeración debe ser secuencial (1., 2., 3., etc.) para aplicar la corrección.
    """
    lineas = texto.splitlines()
    resultado = []
    numeracion_esperada = None  # Comienza sin numeración previa

    patron_numeracion = re.compile(r"^(\d+)\.\s*([a-zA-Z]{1,2})\)")

    for linea in lineas:
        match = patron_numeracion.match(linea.strip())

        if match:
            numero_actual = int(match.group(1))
            letras = match.group(2)

            # Si es la primera numeración encontrada, inicializar numeración esperada
            if numeracion_esperada is None:
                numeracion_esperada = numero_actual

            # Solo corregir si el número es el esperado
            if numero_actual == numeracion_esperada:
                # Corregir si hay dos letras (ej: Cc), Aa), etc.)
                if len(letras) > 1:
                    letra_corregida = letras[-1].lower()
                    linea = re.sub(
                        r"^(\d+\.\s*)[a-zA-Z]{1,2}\)",
                        r"\1" + letra_corregida + ")",
                        linea,
                    )

                numeracion_esperada += 1  # Esperar el siguiente número
            else:
                # Si no es el número esperado, no corregir nada, pero actualizar
                numeracion_esperada = numero_actual + 1

        resultado.append(linea)

    return "\n".join(resultado)


def corregir_numeracion_preguntas_reserva(texto: str) -> str:
    """
    A partir de la línea '60.', corrige las siguientes numeraciones '1.', '2.', '3.', '4.'
    convirtiéndolas en '61.', '62.', '63.', '64.' respectivamente.
    """

    lineas = texto.splitlines()
    nuevas_lineas = []

    patron_60 = re.compile(r"^60\.\s*[a-dA-D][a-dA-D]?\)\s+.*")
    patron_reserva = re.compile(r"^([1-4])\.\s*([a-dA-D])[a-dA-D]?\)\s+(.*)")

    encontrado_60 = False
    reservas_actualizadas = 0

    for linea in lineas:
        if not encontrado_60:
            if patron_60.match(linea):
                encontrado_60 = True
            nuevas_lineas.append(linea)
            continue

        if reservas_actualizadas < 4:
            match = patron_reserva.match(linea)
            if match:
                numero_actual = int(match.group(1))
                letra = match.group(2).lower()
                resto = match.group(3)
                nuevo_numero = 60 + numero_actual
                nueva_linea = f"{nuevo_numero}. {letra}) {resto}"
                nuevas_lineas.append(nueva_linea)
                reservas_actualizadas += 1
                continue

        nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas) + "\n"


def corregir_numeracion_preguntas_reserva_general(texto: str) -> str:
    """
    A partir de la línea que empieza con '60.', corrige las siguientes numeraciones '1.', '2.', '3.', '4.'
    convirtiéndolas en '61.', '62.', '63.', '64.' respectivamente, en un formato más laxo.
    """

    lineas = texto.splitlines()
    nuevas_lineas = []

    # Nuevo patrón más flexible:
    patron_60 = re.compile(r"^60\.\s+.*")
    patron_reserva = re.compile(r"^([1-4])\.\s+.*")

    encontrado_60 = False
    reservas_actualizadas = 0

    for linea in lineas:
        if not encontrado_60:
            if patron_60.match(linea):
                encontrado_60 = True
            nuevas_lineas.append(linea)
            continue

        if reservas_actualizadas < 4:
            match = patron_reserva.match(linea)
            if match:
                numero_actual = int(match.group(1))
                nuevo_numero = 60 + numero_actual
                # Solo reemplazar el número inicial
                nueva_linea = re.sub(r"^\d+\.", f"{nuevo_numero}.", linea, count=1)
                nuevas_lineas.append(nueva_linea)
                reservas_actualizadas += 1
                continue

        nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas) + "\n"


def insertar_linea_vacia_antes_numeracion(texto: str) -> str:
    lineas = texto.splitlines()
    nuevas_lineas = []
    numero_esperado = 1
    patron_numeracion = re.compile(r"^(\d+)\.\s?[a-zA-Z]?\)?")

    for linea in lineas:
        match = patron_numeracion.match(linea.strip())
        if match:
            numero_encontrado = int(match.group(1))
            if numero_encontrado == numero_esperado:
                if (
                    numero_esperado != 1
                ):  # No agregar línea vacía antes del primer número
                    nuevas_lineas.append("")
                nuevas_lineas.append(linea)
                numero_esperado += 1
                continue
            else:
                # Número fuera de orden: lo ignoramos (lo tratamos como línea normal)
                pass
        nuevas_lineas.append(linea)

    return "\n".join(nuevas_lineas)


def unir_oraciones_partidas(lineas: str) -> str:
    """
    Une líneas partidas que forman parte de la misma oración,
    respetando reglas estrictas para no unir bloques que no deben.

    Protecciones:
    - No une si hay una línea vacía entre medio.
    - No une si la siguiente línea empieza con comillas (" o “).
    - No une si la línea actual termina en ciertos caracteres que indican fin de frase (. ? ! :).
    """

    caracteres_finales = {".", "?", "!", ":", ";"}  # Se pueden agregar más si quieres
    resultado = []
    buffer = ""
    lineas = lineas.splitlines()

    for idx, linea in enumerate(lineas):
        linea_actual = linea.rstrip()

        if not linea_actual:
            # Si encontramos línea vacía, guardamos lo que tengamos en el buffer
            if buffer:
                resultado.append(buffer)
                buffer = ""
            resultado.append("")  # Conservamos la línea vacía
            continue

        if buffer:
            # Si hay algo en el buffer, decidir si unir o no
            if (not buffer[-1] in caracteres_finales) and (
                not linea_actual.startswith(('"', "“"))
            ):
                # Unir la línea al buffer con espacio
                buffer += " " + linea_actual
            else:
                # No unir, guardar lo que había
                resultado.append(buffer)
                buffer = linea_actual
        else:
            buffer = linea_actual

    # Guardar lo último que quede en buffer
    if buffer:
        resultado.append(buffer)

    return "\n".join(resultado)


def unir_palabras_partidas_por_guiones(texto: str) -> str:
    """
    Une palabras partidas por guiones, validando con un diccionario.
    Pregunta al usuario si no está seguro.
    Maneja también un registro de palabras rechazadas.
    """

    # === Cargar diccionarios externos ===
    if os.path.exists(DICCIONARIO_PATH):
        with open(DICCIONARIO_PATH, "r", encoding="utf-8") as f:
            diccionario_es = set(p.strip().lower() for p in f if p.strip())
    else:
        diccionario_es = set()

    if os.path.exists(RECHAZADAS_PATH):
        with open(RECHAZADAS_PATH, "r", encoding="utf-8") as f:
            palabras_rechazadas = json.load(f)
    else:
        palabras_rechazadas = {}

    palabras_aceptadas = set()

    # === Funciones auxiliares ===
    def palabra_valida(palabra):
        return (
            palabra.lower() in diccionario_es or palabra.lower() in palabras_aceptadas
        )

    def fragmento_rechazado(fragmento):
        return palabras_rechazadas.get(fragmento, 0) >= 3

    # === Variables internas ===
    COLOR_BEGIN = "\033[1;33m"
    COLOR_END = "\033[0m"
    nuevas_lineas = []
    log_lines = []

    lineas = texto.splitlines()

    for i, linea in enumerate(lineas, 1):
        ocurrencias = list(re.finditer(r"(\w+)-\s(\w+)", linea))
        if not ocurrencias:
            nuevas_lineas.append(linea)
            continue

        linea_modificada = linea
        offset = 0

        for match in ocurrencias:
            palabra1, palabra2 = match.group(1), match.group(2)
            palabra_completa = palabra1 + palabra2

            start = match.start() + offset
            end = match.end() + offset
            original_fragmento = linea_modificada[
                start:end
            ]  # ← este fragmento es el que vamos a guardar
            propuesto = palabra_completa

            resaltado_original = f"{COLOR_BEGIN}{original_fragmento}{COLOR_END}"
            resaltado_modificado = f"{COLOR_BEGIN}{propuesto}{COLOR_END}"

            if palabra_valida(palabra_completa):
                linea_modificada = (
                    linea_modificada[:start] + propuesto + linea_modificada[end:]
                )
                offset -= len("- ")
                # print(
                    # f"✔️ Línea {i}: {resaltado_original} → {resaltado_modificado} (automático)"
                # )
                log_lines.append(f"✔️ Línea {i}: {resaltado_original} → {resaltado_modificado} (automático)")

            elif fragmento_rechazado(original_fragmento):
                # print(f"⏩ Línea {i}: {resaltado_original} (rechazo automático)")
                log_lines.append(f"⏩ Línea {i}: {resaltado_original} (rechazo automático)")
                # No hacemos nada, mantenemos la palabra partida

            else:
                print(f"\nLínea {i}:")
                print(f"Opción A (eliminar '- '): {resaltado_modificado}")
                print(f"Opción B (mantener '- '): {resaltado_original}")
                decision = input("¿Eliminar '- '? (y/n) [n]: ").strip().lower()
                if decision == "y":
                    linea_modificada = (
                        linea_modificada[:start] + propuesto + linea_modificada[end:]
                    )
                    offset -= len("- ")
                    palabras_aceptadas.add(palabra_completa.lower())
                    print("✔️ Eliminado.")
                else:
                    palabras_rechazadas[original_fragmento] = (
                        palabras_rechazadas.get(original_fragmento, 0) + 1
                    )
                    print("⏩ Mantenido.")

        nuevas_lineas.append(linea_modificada)

    # === Guardar nuevas palabras aceptadas ===
    if palabras_aceptadas:
        palabras_totales = diccionario_es.union(palabras_aceptadas)
        palabras_ordenadas = sorted(palabras_totales)
        with open(DICCIONARIO_PATH, "w", encoding="utf-8") as f:
            for palabra in palabras_ordenadas:
                f.write(palabra + "\n")

    # === Guardar el registro actualizado de rechazadas ===
    with open(RECHAZADAS_PATH, "w", encoding="utf-8") as f:
        json.dump(palabras_rechazadas, f, ensure_ascii=False, indent=2)

    # === Resultado final ===
    return "\n".join(nuevas_lineas), log_lines


def eliminar_basurita_final(texto: str, basuritas: set) -> str:
    """
    Elimina cadenas específicas del final de las líneas de un texto.
    Muestra en consola los cambios realizados con el fragmento eliminado resaltado.
    """
    COLOR_BEGIN = "\033[1;33m"  # Amarillo
    COLOR_END = "\033[0m"

    nuevas_lineas = []
    log_lines = []

    for linea in texto.splitlines():
        linea_original = linea.rstrip()

        for basura in basuritas:
            # Si la línea termina exactamente con la basura (ignorando espacios)
            if linea_original.endswith(basura):
                inicio_basura = len(linea_original) - len(basura)
                parte_buena = linea_original[:inicio_basura].rstrip()

                resaltado = parte_buena + COLOR_BEGIN + basura + COLOR_END
                # print(
                    # f"✔️ Corrigiendo línea:\nAntes: {resaltado}\nDespués: {parte_buena}\n"
                # )
                log_lines.append(f"✔️ Corrigiendo línea:\nAntes: {resaltado}\nDespués: {parte_buena}\n")

                linea_original = parte_buena  # Actualizamos la línea ya corregida
                break  # Solo quitamos una basura por línea (si hay varias, correría de nuevo en otra pasada)

        nuevas_lineas.append(linea_original)

    return "\n".join(nuevas_lineas), log_lines
