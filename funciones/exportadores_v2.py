import re

def parsear_preguntas_v2(texto_multilinea, nombre_archivo):
    lineas = texto_multilinea.strip().splitlines()
    preguntas = []
    i = 0

    while i < len(lineas):
        # Paso 1: buscar una línea que empiece con un número seguido de punto (ej: "23.")
        match_preg = re.match(r"^(\d+)\.\s+(.*)", lineas[i])
        if not match_preg:
            i += 1
            continue

        numero = match_preg.group(1)            # número de la pregunta (ej: "23")
        enunciado = match_preg.group(0).strip() # línea completa como texto de la pregunta
        i += 1

        # Paso 2: buscar las 4 opciones que empiecen con a), b), c) o d)
        opciones = []
        while i < len(lineas) and len(opciones) < 4:
            linea = lineas[i].strip()
            if re.match(r"^[a-d]\)", linea):
                opciones.append(linea)
            elif linea == "":
                pass  # ignoramos líneas vacías entre opciones
            i += 1

        # Paso 3: si faltan opciones, rellenar con placeholders visibles
        letras_presentes = {op[0] for op in opciones}
        for letra in ['a', 'b', 'c', 'd']:
            if letra not in letras_presentes:
                opciones.append(f"{letra}) [FALTA OPCIÓN {letra.upper()}]")

        opciones.sort()  # ordenar por letra para mantener consistencia

        # Paso 4: buscar la respuesta usando el mismo número seguido de letra, ej: "23. c)"
        correcta = "[RESPUESTA NO DETECTADA]"
        if i < len(lineas):
            match_resp = re.match(rf"^{numero}\.\s*([a-d]\))", lineas[i].strip())
            if match_resp:
                correcta = match_resp.group(1)
                i += 1  # avanzar a la línea siguiente (comentario)

        # Paso 5: capturar la línea de comentario si existe
        comentario = ""
        if i < len(lineas):
            comentario = lineas[i].strip()
            i += 1

        # Paso 6: almacenar todo en la lista de preguntas
        preguntas.append({
            "pregunta": enunciado,
            "opciones": opciones,
            "correcta": correcta,
            "comentario": comentario,
        })

    # Paso 7: escribir las preguntas en un archivo JavaScript como array
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

    # Paso 8: guardar el resultado en archivo
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_js)

    return nombre_archivo