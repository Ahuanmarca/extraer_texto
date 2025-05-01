import os
import argparse
from datetime import datetime
import unicodedata
from collections import defaultdict

LOG_FILENAME = "caracteres_raros.log"
EXTENSION_IGNORADA = ".py"

def clasificar_caracter(c):
    if c in '\n\r\t':
        return None  # Permitidos básicos
    if c.isprintable():
        return None
    try:
        nombre = unicodedata.name(c)
        categoria = unicodedata.category(c)
        return f"{nombre} (U+{ord(c):04X}, {categoria})"
    except ValueError:
        return f"UNKNOWN (U+{ord(c):04X})"

def analizar_archivo(path):
    conteo = defaultdict(int)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()
            for c in contenido:
                clasificacion = clasificar_caracter(c)
                if clasificacion:
                    conteo[clasificacion] += 1
    except Exception as e:
        conteo[f"ERROR: {str(e)}"] += 1
    return conteo

def main():
    parser = argparse.ArgumentParser(description="Detecta caracteres sospechosos en archivos de texto.")
    parser.add_argument("--termina_en", type=str, help="Filtra solo archivos cuyo nombre termine con este string.")
    args = parser.parse_args()

    archivos = [
        f for f in os.listdir(".")
        if os.path.isfile(f)
        and not f.endswith(EXTENSION_IGNORADA)
        and (args.termina_en is None or f.endswith(args.termina_en))
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte = [f"=== Reporte de caracteres raros generado el {timestamp} ===", ""]

    for archivo in sorted(archivos):
        conteo = analizar_archivo(archivo)
        if conteo:
            reporte.append(f"Archivo: {archivo}")
            for clasificacion, cantidad in sorted(conteo.items(), key=lambda x: -x[1]):
                reporte.append(f"  {clasificacion}: {cantidad}")
            reporte.append("")  # Separador

    with open(LOG_FILENAME, "a", encoding="utf-8", errors="replace") as log:
        log.write("\n".join(reporte))
        log.write("\n\n==========\n\n")

    print(f"\n{len(archivos)} archivos analizados. Revisa '{LOG_FILENAME}' para ver resultados.")

if __name__ == "__main__":
    main()
