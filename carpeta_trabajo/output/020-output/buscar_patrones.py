import os
import re
import argparse
from datetime import datetime

# Define aquí los patrones que quieres buscar (pueden ser strings o regex)

PATRONES = (
    # r"^\d{1,2}\. [a-z]\) .+",       # Correcto: "1. c) Lorem Ipsum."
    # r"^\d{1,2}\. [a-z]\)[^\s].*",   # Incorrecto: sin espacio después del paréntesis: "4. a)Lorem Ipsum."
    # r"^[a-z]\) .+",                 # Incorrecto: sin número al inicio: "b) Lorem Ipsum."
    # r"^[a-z]\)[^\s].*",             # Incorrecto: sin número y sin espacio tras el paréntesis: "a)Lorem Ipsum."
    # r"\bTODO\b",
    r"^\d{1,2}\. (?![a-z]\) ).+",
)


LOG_FILENAME = "reporte_patrones.log"


def buscar_patrones_en_archivo(nombre_archivo, patrones):
    resultados = []
    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        for i, linea in enumerate(f, start=1):
            for patron in patrones:
                if re.search(patron, linea):
                    resultados.append((patron, i, linea.strip()))
    return resultados


def obtener_archivos_a_revisar(sufijo, extension):
    archivos = []
    for f in os.listdir("."):
        if not os.path.isfile(f) or f.endswith(".py"):
            continue
        if sufijo and not f.endswith(sufijo):
            continue
        if extension and not f.lower().endswith("." + extension.lower()):
            continue
        archivos.append(f)
    return sorted(archivos)


def main():
    parser = argparse.ArgumentParser(
        description="Buscar patrones en archivos de texto."
    )
    parser.add_argument(
        "--comentario",
        type=str,
        help="Comentario opcional para incluir en el encabezado del log.",
    )
    parser.add_argument(
        "--termina_con",
        type=str,
        help="Solo analizar archivos cuyo nombre termine con este string.",
    )
    parser.add_argument(
        "--ext", type=str, help="Solo analizar archivos con esta extensión (sin punto)."
    )
    args = parser.parse_args()

    archivos = obtener_archivos_a_revisar(args.termina_con, args.ext)
    total_incidencias = 0
    archivos_con_resultados = 0
    reporte = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte.append(f"=== Reporte generado el {timestamp} ===")
    if args.comentario:
        reporte.append(f"Comentario: {args.comentario}")
    if args.termina_con:
        reporte.append(
            f'Filtro de sufijo: archivos que terminan con "{args.termina_con}"'
        )
    if args.ext:
        reporte.append(f'Filtro de extensión: solo archivos ".{args.ext}"')
    reporte.append("")  # línea en blanco después del encabezado

    for archivo in archivos:
        resultados = buscar_patrones_en_archivo(archivo, PATRONES)
        if resultados:
            archivos_con_resultados += 1
            reporte.append(f"Archivo: {archivo}\n" + "-" * (9 + len(archivo)))
            for patron, linea_num, linea_texto in resultados:
                reporte.append(
                    f'  Línea {linea_num:>4}: patrón "{patron}"\n    → {linea_texto}'
                )
            reporte.append("")
            total_incidencias += len(resultados)

    if total_incidencias > 0:
        with open(LOG_FILENAME, "a", encoding="utf-8") as log:
            log.write("\n".join(reporte))
            log.write("\n\n==========\n\n")  # separador visual
    else:
        print("No se encontraron incidencias.")

    print(
        f"\nSe encontraron {total_incidencias} incidencias en {archivos_con_resultados} archivos."
    )
    print(f'Revisa el archivo "{LOG_FILENAME}" para más detalles.')


if __name__ == "__main__":
    main()
