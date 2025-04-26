# Función "pura".
# Recibe todo lo que necesita por argumentos.
# Para implementarla a futuro.

import re

def unir_palabras_partidas_por_guiones(texto: str, diccionario: set[str], confirmar: bool = False) -> str:
    """
    Une palabras partidas por guiones ('-\n') si la palabra resultante es válida según un diccionario.
    Opcionalmente puede pedir confirmación para unir palabras no reconocidas.

    Args:
        texto (str): El texto de entrada.
        diccionario (set[str]): Conjunto de palabras válidas.
        confirmar (bool): Si True, pedirá confirmación para unir palabras desconocidas. Si False, no unirá.

    Returns:
        str: El texto corregido.
    """

    nuevas_lineas = []
    palabras_aceptadas = set()

    # Separamos en líneas
    lineas = texto.splitlines()

    for i, linea in enumerate(lineas, 1):
        ocurrencias = list(re.finditer(r'(\w+)-\s(\w+)', linea))
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

            if palabra_completa.lower() in diccionario or palabra_completa.lower() in palabras_aceptadas:
                # Si la palabra ya es válida, unir automáticamente
                linea_modificada = linea_modificada[:start] + palabra_completa + linea_modificada[end:]
                offset -= len("- ")
            elif confirmar:
                # Si hay que confirmar manualmente
                print(f"\nLínea {i}:")
                print(f"Opción A (unir): {palabra_completa}")
                print(f"Opción B (mantener): {palabra1}- {palabra2}")
                decision = input("¿Unir palabras? (y/n) [n]: ").strip().lower()
                if decision == "y":
                    linea_modificada = linea_modificada[:start] + palabra_completa + linea_modificada[end:]
                    offset -= len("- ")
                    palabras_aceptadas.add(palabra_completa.lower())
                # Si no, simplemente dejamos la palabra partida

        nuevas_lineas.append(linea_modificada)

    return "\n".join(nuevas_lineas)
