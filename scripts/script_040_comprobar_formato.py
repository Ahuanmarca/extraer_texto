import re
import os


def main(texto: str, nombre_archivo_log=None) -> str:
    ruta_log = f"carpeta_trabajo/{nombre_archivo_log}.log"

    bloques = re.split(r'\n(?=\d{1,2}\. )', texto)
    bloques_marcados = []
    problemas = []
    orden_incorrecto = []
    numeros_detectados = []

    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue

        match_num = re.match(r'^(\d{1,2})\.', bloque)
        if not match_num:
            bloques_marcados.append(bloque)
            continue

        numero = int(match_num.group(1))
        numeros_detectados.append(numero)

        # Buscar las opciones tipo a) b) c) d) al final de línea
        opciones = re.findall(r'^([abcd])\) .+\.$', bloque, flags=re.MULTILINE)

        error_detectado = False

        # Comprobar cantidad de opciones
        if len(opciones) != 4:
            problemas.append(
                f"❌ Pregunta {numero}: {len(opciones)} opciones encontradas"
            )
            error_detectado = True

        elif opciones != ["a", "b", "c", "d"]:
            orden_incorrecto.append(
                f"🔀 Pregunta {numero}: orden incorrecto de opciones → {opciones}"
            )
            error_detectado = True

        # Si hay errores, insertar línea de aviso
        if error_detectado:
            bloques_marcados.append("---------- TO FIX ----------\n" + bloque)
        else:
            bloques_marcados.append(bloque)

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
                    "✅ La numeración de preguntas es correcta (1–60 y luego 1–4).\n"
                )

    # === Mostrar resumen en consola ===
    print("\n📝 RESUMEN DE REVISIÓN:")
    if not problemas and not errores_numeracion and not orden_incorrecto:
        print(
            "✅ Todo correcto: 64 preguntas bien numeradas, ordenadas y con 4 opciones."
        )
    else:
        if problemas:
            print(f"❌ Preguntas con número de opciones incorrectas: {len(problemas)}")
        if orden_incorrecto:
            print(f"🔀 Preguntas con opciones desordenadas: {len(orden_incorrecto)}")
        for linea in resumen_consola:
            print(linea)

    print("📄 Detalles registrados en el log.")

    # === Devolver el texto corregido ===
    return "\n\n".join(bloques_marcados)


# Ejemplo de uso:
if __name__ == "__main__":
    texto_entrada = """1. a) Algo.\nb) Otro.\nc) Más.\nd) Último.\n2. a) Error."""
    texto_corregido = main(
        texto_entrada, nombre_archivo_log="log_revision"
    )
    print("\n--- TEXTO CORREGIDO ---\n")
    print(texto_corregido)
