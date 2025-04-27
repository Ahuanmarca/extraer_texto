# === IMPORTS ===
import re
import os
from collections import Counter
from funciones.normalizadores import unir_palabras_partidas_por_guiones
from funciones.normalizadores import corregir_numeracion_preguntas_reserva_general
from funciones.normalizadores import eliminar_basurita_final

# === BASE_DIR Y RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")


# === FUNCIONES AUXILIARES ===


def eliminar_referencias_imagen(texto):
    lineas = texto.splitlines()
    lineas_filtradas = [
        linea
        for linea in lineas
        if not ("===== IMG_" in linea and ".heic =====" in linea)
    ]
    return "\n".join(lineas_filtradas)


def corregir_letras_opciones(texto):
    def corregir_linea(linea):
        match = re.match(r"^(\d+)\.\s*([a-dA-D])[a-dA-D]?\)(.*)", linea)
        if match:
            numero, letra, resto = match.groups()
            letra = letra.lower()
            return f"{numero}. {letra}){resto.strip()}"
        return linea

    lineas = texto.splitlines()
    lineas_corregidas = [corregir_linea(linea) for linea in lineas]
    return "\n".join(lineas_corregidas)


def detectar_y_normalizar_preguntas(texto):
    nuevas_lineas = []
    log_advertencias = []
    pregunta_actual = ""
    opciones_actuales = []
    letras_actuales = []

    def guardar_bloque():
        if not pregunta_actual:
            return

        errores = []
        if len(opciones_actuales) != 4:
            errores.append(
                f"⚠️ Pregunta con {len(opciones_actuales)} respuestas: {pregunta_actual[:100]}"
            )

        letra_counts = Counter(letras_actuales)
        duplicadas = [letra for letra, count in letra_counts.items() if count > 1]
        if duplicadas:
            errores.append(
                f"⚠️ Letras duplicadas ({', '.join(duplicadas)}): {pregunta_actual[:100]}"
            )

        if errores:
            log_advertencias.extend(errores)

        nuevas_lineas.append(pregunta_actual.strip())
        nuevas_lineas.extend([op.strip() for op in opciones_actuales])
        nuevas_lineas.append("")

    lineas = texto.splitlines()

    for linea in lineas:
        linea = linea.rstrip()
        if not linea:
            continue

        match_pregunta = re.match(r"^(\d+)\.\s*(.*)", linea)
        if match_pregunta:
            guardar_bloque()
            numero, contenido = match_pregunta.groups()
            pregunta_actual = f"{numero}. {contenido.strip()}"
            opciones_actuales = []
            letras_actuales = []
            continue

        match_opcion = re.match(r"^[\-\s]*([a-dA-D])[a-dA-D]?\)+\s*(.*)", linea)
        if match_opcion:
            letra, contenido = match_opcion.groups()
            opciones_actuales.append(f"{letra.lower()}) {contenido.strip()}")
            letras_actuales.append(letra.lower())
            continue

        # Continuaciones
        if opciones_actuales:
            opciones_actuales[-1] += f" {linea.strip()}"
        elif pregunta_actual:
            pregunta_actual += f" {linea.strip()}"

    guardar_bloque()

    texto_normalizado = "\n".join(nuevas_lineas)
    return texto_normalizado, log_advertencias


def guardar_log(advertencias, nombre_archivo_log):
    ruta = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in advertencias:
            f.write(advertencia + "\n")


# === MAIN ===
def main(texto: str = None, nombre_archivo_log=None):
    if not texto or not nombre_archivo_log:
        print("❌ Faltan argumentos.")
        return ""

    log_advertencias = []

    # === 2. ELIMINAR REFERENCIAS A IMÁGENES ===
    texto = eliminar_referencias_imagen(texto)

    # === 3. CORREGIR LETRAS RARAS EN OPCIONES ===
    texto = corregir_letras_opciones(texto)

    # === 4. DETECTAR Y NORMALIZAR PREGUNTAS Y OPCIONES ===
    texto, advertencias = detectar_y_normalizar_preguntas(texto)
    log_advertencias.extend(advertencias)

    # === 5. UNIR PALABRAS PARTIDAS POR GUIONES ===
    texto, log_lines = unir_palabras_partidas_por_guiones(texto)
    # log_advertencias.extend(log_lines)

    # === 6. CORREGIR NUMERACION PREGUNTAS RESERVA ===
    texto = corregir_numeracion_preguntas_reserva_general(texto)

    # === 7. ELIMINAR BASURITA FINAL ===

    basuritas = {
        "p A E",
        " :",
        " Ae",
        " Preguntas de reserva",
        "En MADTEST tienes más preguntas, y todos tus avances quedan hy SN registrados y se reflejan en el ranking. IS ¡Supera tus límites con MADTEST! o MA A rr ronene",
    }
    texto, log_lines = eliminar_basurita_final(texto, basuritas)
    log_advertencias.extend(log_lines)

    # === 8. GUARDAR LOG ===
    guardar_log(log_advertencias, nombre_archivo_log)

    # === 9. RETORNAR TEXTO NORMALIZADO ===
    return texto


if __name__ == "__main__":
    texto_resultado = main()
