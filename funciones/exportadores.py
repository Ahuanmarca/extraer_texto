import re

def generar_javascript(texto_multilinea):
    lineas = texto_multilinea.strip().splitlines()
    preguntas = []
    errores = []
    i = 0

    def es_pregunta(linea):
        return re.match(r"^\d+\.\s+\S", linea)

    def es_opcion(linea):
        return re.match(r"^[a-d]\)\s+\S", linea)

    def es_respuesta(linea):
        return re.match(r"^\d+\.\s+[a-d]\)\s+\S", linea)

    while i < len(lineas):
        # Buscar pregunta
        while i < len(lineas) and not es_pregunta(lineas[i]):
            i += 1
        if i >= len(lineas):
            break
        pregunta_linea = lineas[i].strip()
        numero = re.match(r"^(\d+)\.", pregunta_linea).group(1)
        i += 1

        # Buscar opciones (máx 4)
        opciones = []
        while i < len(lineas) and len(opciones) < 4:
            linea = lineas[i].strip()
            if es_respuesta(linea) or es_pregunta(linea):
                break
            if es_opcion(linea):
                opciones.append(linea)
            i += 1

        if len(opciones) < 4:
            errores.append(f"Pregunta {numero}: solo se detectaron {len(opciones)} opción(es)")

        # Si faltan opciones, completar con placeholders
        letras_presentes = {op[0] for op in opciones}
        for letra in ['a', 'b', 'c', 'd']:
            if letra not in letras_presentes:
                opciones.append(f"{letra}) [FALTA OPCIÓN {letra.upper()}]")
        opciones.sort()

        # Buscar respuesta
        correcta = "[RESPUESTA NO DETECTADA]"
        while i < len(lineas):
            if es_respuesta(lineas[i]):
                match = re.match(rf"^{numero}\.\s+([a-d]\)\s+.+)", lineas[i])
                if match:
                    correcta = match.group(1)  # Captura "c) texto completo"
                i += 1
                break
            i += 1

        # Leer comentario (hasta la siguiente pregunta o EOF)
        comentario_lineas = []
        while i < len(lineas) and not es_pregunta(lineas[i]) and not es_respuesta(lineas[i]) and not es_opcion(lineas[i]):
            if lineas[i].strip() != "":
                comentario_lineas.append(lineas[i].strip())
            i += 1
        comentario = "\n".join(comentario_lineas)

        preguntas.append({
            "pregunta": pregunta_linea,
            "opciones": opciones,
            "correcta": correcta,
            "comentario": comentario,
        })

    # Generar JS
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

    return contenido_js, errores
