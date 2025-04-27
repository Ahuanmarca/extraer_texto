import re

def main(texto_preguntas: str, texto_respuestas: str) -> str:
    """
    Combina las preguntas y respuestas basándose en la numeración.
    Ya no maneja bloques especiales como '---------- TO FIX ----------'.
    """

    # === Dividir preguntas ===
    bloques_preguntas = re.split(r"(?=^\d+\.\s)", texto_preguntas, flags=re.MULTILINE)
    preguntas = {}

    for bloque in bloques_preguntas:
        bloque = bloque.strip()
        if not bloque:
            continue

        match = re.match(r"^(\d+)\.\s", bloque)
        if match:
            numero = int(match.group(1))
            preguntas[numero] = bloque

    # === Dividir respuestas ===
    bloques_respuestas = re.split(r"(?=^\d+\.\s)", texto_respuestas, flags=re.MULTILINE)
    respuestas = {}

    for bloque in bloques_respuestas:
        bloque = bloque.strip()
        if not bloque:
            continue

        match = re.match(r"^(\d+)\.\s", bloque)
        if match:
            numero = int(match.group(1))
            respuestas[numero] = bloque

    # === Combinar preguntas y respuestas ===
    numeros_combinados = sorted(set(preguntas.keys()) | set(respuestas.keys()))
    combinados = []

    for numero in numeros_combinados:
        # Primero agregamos la pregunta (si existe)
        if numero in preguntas:
            combinados.append(preguntas[numero])
            combinados.append("")  # Línea vacía entre pregunta y respuesta
        else:
            combinados.append(f"---------- PREGUNTA {numero} NO ENCONTRADA ----------")
            combinados.append("")

        # Luego agregamos la respuesta (si existe)
        if numero in respuestas:
            combinados.append(respuestas[numero])
            combinados.append("")  # Línea vacía entre respuesta y próxima pregunta
        else:
            combinados.append(f"---------- RESPUESTA {numero} NO ENCONTRADA ----------")
            combinados.append("")

    return "\n".join(combinados).strip()

# Ejemplo de uso
if __name__ == "__main__":
    texto_preguntas = """..."""
    texto_respuestas = """..."""
    resultado = main(texto_preguntas, texto_respuestas)
    print(resultado)
