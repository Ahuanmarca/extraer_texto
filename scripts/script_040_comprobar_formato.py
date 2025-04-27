import re
import os

def main(texto: str, nombre_archivo_log=None) -> str:
    ruta_log = f"carpeta_trabajo/{nombre_archivo_log}.log"

    lineas = texto.splitlines()
    bloques_marcados = []
    problemas = []
    orden_incorrecto = []
    numeros_detectados = []

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        if not linea:
            i += 1
            continue

        # Detectar si es respuesta (ej: 2. a) Lorem Ipsum.)
        match_respuesta = re.match(r"^(\d+)\.\s*[a-dA-D]\)", linea)

        # Detectar si es pregunta (ej: 2. Lorem Ipsum?)
        match_pregunta = re.match(r"^(\d+)\.\s+", linea)

        if match_respuesta:
            # Es una respuesta, copiar el bloque tal cual
            bloque = []
            while i < len(lineas):
                bloque.append(lineas[i])
                i += 1
                if i < len(lineas):
                    siguiente = lineas[i].strip()
                    if re.match(r"^\d+\.", siguiente):
                        break
            bloques_marcados.append("\n".join(bloque))
            continue

        elif match_pregunta:
            # Es una pregunta, analizar el bloque
            numero = int(match_pregunta.group(1))
            numeros_detectados.append(numero)

            bloque = []
            while i < len(lineas):
                bloque.append(lineas[i])
                i += 1
                if i < len(lineas):
                    siguiente = lineas[i].strip()
                    if re.match(r"^\d+\.", siguiente):
                        break

            bloque_texto = "\n".join(bloque)

            # Buscar las opciones a), b), c), d)
            opciones = re.findall(r"^[\-\s]*([abcd])\)", bloque_texto, flags=re.MULTILINE)

            error_detectado = False

            if len(opciones) != 4:
                problemas.append(f"❌ Pregunta {numero}: {len(opciones)} opciones encontradas")
                error_detectado = True
            elif opciones != ["a", "b", "c", "d"]:
                orden_incorrecto.append(f"🔀 Pregunta {numero}: orden incorrecto de opciones → {opciones}")
                error_detectado = True

            if error_detectado:
                bloques_marcados.append("---------- TO FIX ----------\n" + bloque_texto)
            else:
                bloques_marcados.append(bloque_texto)

            continue

        else:
            # Si la línea no es pregunta ni respuesta, agregarla igual
            bloques_marcados.append(linea)
            i += 1

    # === Validación de numeración general ===
    errores_numeracion = []
    resumen_consola = []

    esperados = list(range(1, 65))  # Preguntas 1–64
    repetidos = [n for n in numeros_detectados if numeros_detectados.count(n) > 1]
    faltantes = [n for n in esperados if n not in numeros_detectados]
    extras = [n for n in numeros_detectados if n not in esperados]

    if repetidos:
        errores_numeracion.append(f"🔁 Números duplicados: {sorted(set(repetidos))}")
        resumen_consola.append(f"🔁 Duplicados: {sorted(set(repetidos))}")
    if faltantes:
        errores_numeracion.append(f"❌ Números faltantes: {faltantes}")
        resumen_consola.append(f"❌ Faltantes: {faltantes}")
    if extras:
        errores_numeracion.append(f"⚠️ Números fuera de rango esperado: {extras}")
        resumen_consola.append(f"⚠️ Fuera de rango: {extras}")

    # === Guardar log ===
    if nombre_archivo_log:
        os.makedirs("carpeta_trabajo", exist_ok=True)
        with open(ruta_log, "a", encoding="utf-8") as log:
            log.write("\n--- REVISIÓN DE PREGUNTAS ---\n")
            if problemas:
                for p in problemas:
                    log.write(p + "\n")
                log.write(
                    f"\nTotal con error en número de opciones: {len(problemas)}\n"
                )
            else:
                log.write(
                    "✅ Todas las preguntas tienen 4 opciones correctamente formateadas.\n"
                )

            if orden_incorrecto:
                log.write("\n--- ORDEN INCORRECTO DE OPCIONES ---\n")
                for o in orden_incorrecto:
                    log.write(o + "\n")

            if errores_numeracion:
                log.write("\n--- PROBLEMAS DE NUMERACIÓN ---\n")
                for e in errores_numeracion:
                    log.write(e + "\n")
            else:
                log.write(
                    "✅ La numeración de preguntas es correcta (1–64).\n"
                )

    # === Mostrar resumen en consola ===
    # print("\n📝 RESUMEN DE REVISIÓN:")
    if not problemas and not errores_numeracion and not orden_incorrecto:
        print(
            "✅ Todo correcto: 64 preguntas bien numeradas, ordenadas y con 4 opciones."
        )
    # else:
        # if problemas:
            # print(f"❌ Preguntas con número de opciones incorrectas: {len(problemas)}")
        # if orden_incorrecto:
            # print(f"🔀 Preguntas con opciones desordenadas: {len(orden_incorrecto)}")
        # for linea in resumen_consola:
            # print(linea)

    # print("📄 Detalles registrados en el log.")

    return "\n\n".join(bloques_marcados)
