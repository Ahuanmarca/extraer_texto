import re

def parsear_preguntas(texto_multilinea, nombre_archivo):
    bloques = texto_multilinea.strip().split("\n\n")
    preguntas = []

    i = 0
    while i < len(bloques):
        # Extraer pregunta y opciones
        pregunta_bloque = bloques[i]
        solucion_bloque = bloques[i+1] if i+1 < len(bloques) else ""
        comentario_bloque = bloques[i+2] if i+2 < len(bloques) else ""
        i += 3

        # Separar pregunta y opciones
        lineas = pregunta_bloque.strip().splitlines()
        pregunta_texto = ""
        opciones = []
        for linea in lineas:
            if re.match(r"^\d+\.\s", linea):
                pregunta_texto = linea.strip()
            elif re.match(r"^[a-d]\)", linea.strip()):
                opciones.append(linea.strip())

        # Si faltan opciones, rellenar con placeholders
        letras_presentes = {op[0] for op in opciones}
        for letra in ['a', 'b', 'c', 'd']:
            if letra not in letras_presentes:
                opciones.append(f"{letra}) [FALTA OPCIÓN {letra.upper()}]")

        opciones.sort()  # Asegurar orden a, b, c, d

        # Extraer letra de la respuesta correcta
        match_resp = re.search(r"^\d+\.\s*([a-d]\))", solucion_bloque.strip(), re.IGNORECASE)
        correcta = match_resp.group(1) if match_resp else "[RESPUESTA NO DETECTADA]"

        preguntas.append({
            "pregunta": pregunta_texto,
            "opciones": opciones,
            "correcta": correcta,
            "comentario": comentario_bloque.strip(),
        })

    # Formato final en JS
    contenido_js = "const preguntas = [\n"
    for p in preguntas:
        contenido_js += "  {\n"
        contenido_js += f'    pregunta: "{p["pregunta"]}",\n'
        contenido_js += "    opciones: [\n"
        for op in p["opciones"]:
            contenido_js += f'      "{op}",\n'
        contenido_js += "    ],\n"
        contenido_js += f'    correcta: "{p["correcta"]}",\n'
        contenido_js += f'    comentario: `{p["comentario"]}`,\n'
        contenido_js += "  },\n"
    contenido_js += "];\n"

    # Guardar en archivo
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_js)

    return nombre_archivo
