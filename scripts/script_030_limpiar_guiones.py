import re
import os

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
IMAGENES_CRUDAS = os.path.join(BASE_DIR, "imagenes_crudas")
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")

def main(nombre_archivo=None, nombre_salida=None, nombre_archivo_log=None):
    # === COLORES ===
    COLOR_BEGIN = "\033[1;33m"
    COLOR_END = "\033[0m"

    # === CARGAR DICCIONARIO EXTERNO ===
    # diccionario_path = "diccionario.txt"
    if os.path.exists(DICCIONARIO_PATH):
        with open(DICCIONARIO_PATH, 'r', encoding='utf-8') as f:
            diccionario_es = set(p.strip().lower() for p in f if p.strip())
        print(f"📘 Diccionario cargado con {len(diccionario_es)} palabras.")
    else:
        diccionario_es = set()
        print("⚠️ No se encontró el archivo 'diccionario.txt'. Se usará un diccionario vacío.")

    nuevas_lineas = []
    log_modificaciones = []
    palabras_aceptadas = set()

    def palabra_valida(palabra):
        return palabra.lower() in diccionario_es or palabra.lower() in palabras_aceptadas

    # === ENTRADA ===
    if not nombre_archivo:
        nombre_archivo = input("Archivo .txt a limpiar (sin extensión): ").strip()
    if not nombre_salida:
        nombre_salida = nombre_archivo + "_limp_test"
    archivo_entrada = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo}.txt")
    archivo_salida = os.path.join(CARPETA_TRABAJO, f"{nombre_salida}.txt")
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")

    # === LECTURA ===
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # === PROCESAMIENTO ===
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
            original_fragmento = linea_modificada[start:end]
            propuesto = palabra_completa

            resaltado_original = f"{COLOR_BEGIN}{original_fragmento}{COLOR_END}"
            resaltado_modificado = f"{COLOR_BEGIN}{propuesto}{COLOR_END}"

            if palabra_valida(palabra_completa):
                linea_modificada = linea_modificada[:start] + propuesto + linea_modificada[end:]
                offset -= len("- ")
                print(f"✔️ Línea {i}: {resaltado_original} → {resaltado_modificado} (automático)")
                log_modificaciones.append(f"Línea {i}: {original_fragmento} → {palabra_completa}")
            else:
                print(f"\nLínea {i}:")
                print(f"Opción A (eliminar '- '): {resaltado_modificado}")
                print(f"Opción B (mantener '- '): {resaltado_original}")
                decision = input("¿Eliminar '- '? (y/n) [n]: ").strip().lower()
                if decision == 'y':
                    linea_modificada = linea_modificada[:start] + propuesto + linea_modificada[end:]
                    offset -= len("- ")
                    palabras_aceptadas.add(palabra_completa.lower())
                    print("✔️ Eliminado.")
                    log_modificaciones.append(f"Línea {i}: {original_fragmento} → {palabra_completa}")
                else:
                    print("⏩ Mantenido.")

        nuevas_lineas.append(linea_modificada)

    # === GUARDAR ARCHIVO MODIFICADO ===
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)

    # === ACTUALIZAR DICCIONARIO ===
    if palabras_aceptadas:
        palabras_totales = diccionario_es.union(palabras_aceptadas)
        palabras_ordenadas = sorted(palabras_totales)
        with open(DICCIONARIO_PATH, 'w', encoding='utf-8') as f:
            for palabra in palabras_ordenadas:
                f.write(palabra + '\n')

    # === GUARDAR LOG ===
    with open(archivo_log, 'a', encoding='utf-8') as f:
        f.write("\nLog de limpieza de guiones:\n")
        if palabras_aceptadas:
            lista = ', '.join(sorted(palabras_aceptadas))
            f.write(f"Palabras agregadas a diccionario.txt: {lista}\n\n")
        for entrada in log_modificaciones:
            f.write(entrada + '\n')

    # === MENSAJE FINAL ===
    print(f"\n✅ Archivo modificado guardado como: {archivo_salida}")
    print(f"📝 Log de cambios guardado como: {archivo_log}")
    if palabras_aceptadas:
        print(f"📚 Palabras nuevas agregadas al diccionario: {', '.join(sorted(palabras_aceptadas))}")

if __name__ == "__main__":
    main()
