import re

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
                    nueva_linea = f"{numero_en_progreso}. {letra}) {linea.strip()[len(match_opcion.group(0)):].strip()}"
                    resultado.append(nueva_linea)
                    numero_en_progreso += 1
                    i += 1
                    continue

        resultado.append(linea)
        i += 1

    return "\n".join(resultado)
