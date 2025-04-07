import re
import os

def main(nombre_archivo=None):
    if not nombre_archivo:
        nombre_archivo = input("Nombre base del archivo (sin extensión): ").strip()

    ruta_txt = f"carpeta_trabajo/{nombre_archivo}_extr_norm_limp.txt"
    ruta_log = f"carpeta_trabajo/{nombre_archivo}.log"

    if not os.path.isfile(ruta_txt):
        print(f"❌ No se encontró el archivo: {ruta_txt}")
        return

    with open(ruta_txt, 'r', encoding='utf-8') as f:
        contenido = f.read()

    bloques = re.split(r'\n(?=\d{1,2}\. )', contenido)
    problemas = []
    orden_incorrecto = []
    numeros_detectados = []

    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue

        match_num = re.match(r'^(\d{1,2})\.', bloque)
        if not match_num:
            continue

        numero = int(match_num.group(1))
        numeros_detectados.append(numero)

        opciones = re.findall(r'^([abcd])\) .+\.$', bloque, flags=re.MULTILINE)

        if len(opciones) != 4:
            problemas.append(f"❌ Pregunta {numero}: {len(opciones)} opciones encontradas")
        elif opciones != ['a', 'b', 'c', 'd']:
            orden_incorrecto.append(f"🔀 Pregunta {numero}: orden incorrecto de opciones → {opciones}")

    # === Validación de numeración ===
    errores_numeracion = []
    resumen_consola = []

    esperados = list(range(1, 61)) + list(range(1, 5))
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

    # === Registrar en el log
    with open(ruta_log, 'a', encoding='utf-8') as log:
        log.write("\n--- REVISIÓN DE PREGUNTAS ---\n")

        if problemas:
            for p in problemas:
                log.write(p + "\n")
            log.write(f"\nTotal con error en número de opciones: {len(problemas)}\n")
        else:
            log.write("✅ Todas las preguntas tienen 4 opciones correctamente formateadas.\n")

        if orden_incorrecto:
            log.write("\n--- ORDEN INCORRECTO DE OPCIONES ---\n")
            for o in orden_incorrecto:
                log.write(o + "\n")

        if errores_numeracion:
            log.write("\n--- PROBLEMAS DE NUMERACIÓN ---\n")
            for e in errores_numeracion:
                log.write(e + "\n")
        else:
            log.write("✅ La numeración de preguntas es correcta (1–60 y luego 1–4).\n")

    # === RESUMEN EN CONSOLA ===
    print("\n📝 RESUMEN DE REVISIÓN:")
    if not problemas and not errores_numeracion and not orden_incorrecto:
        print("✅ Todo correcto: 64 preguntas bien numeradas, ordenadas y con 4 opciones.")
    else:
        if problemas:
            print(f"❌ Preguntas con número de opciones incorrectas: {len(problemas)}")
        if orden_incorrecto:
            print(f"🔀 Preguntas con opciones desordenadas: {len(orden_incorrecto)}")
        for linea in resumen_consola:
            print(linea)

    print("📄 Detalles registrados en el log.")

if __name__ == "__main__":
    main()
