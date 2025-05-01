import os
import argparse
from datetime import datetime
import string

IGNORAR_EXT_O_NOMBRES = (".py", ".log", ".DS_Store")
LOG_FILENAME = "reporte_diferencias.log"

def sanitizar(linea):
    try:
        return linea.encode("utf-8", errors="replace").decode("utf-8")
    except:
        return "[ERROR AL DECODIFICAR LINEA]"

def tiene_no_imprimibles(linea):
    return any(c not in string.printable and c not in '\n\r\t' for c in linea)

def contiene_null_bytes(path):
    try:
        with open(path, "rb") as f:
            chunk = f.read(2048)
            return b"\x00" in chunk
    except:
        return True  # Si no se puede leer, mejor asumir que es binario

def leer_lineas(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()

def comparar_archivos(archivo_a, archivo_b):
    diferencias = []
    lineas_a = leer_lineas(archivo_a)
    lineas_b = leer_lineas(archivo_b)
    max_lineas = max(len(lineas_a), len(lineas_b))

    for i in range(max_lineas):
        linea_a = lineas_a[i].rstrip("\n") if i < len(lineas_a) else "[Línea ausente]"
        linea_b = lineas_b[i].rstrip("\n") if i < len(lineas_b) else "[Línea ausente]"
        if linea_a != linea_b:
            diferencias.append((i + 1, linea_a, linea_b))

    return diferencias

def main():
    parser = argparse.ArgumentParser(
        description="Compara archivos por pares en una carpeta."
    )
    parser.add_argument(
        "--comentario", type=str, help="Comentario opcional que aparecerá en el log."
    )
    args = parser.parse_args()

    archivos_validos = []
    archivos_ignorados = []

    for f in sorted(os.listdir(".")):
        if not os.path.isfile(f):
            continue
        if any(f.endswith(ext) or f == ext for ext in IGNORAR_EXT_O_NOMBRES):
            continue
        if contiene_null_bytes(f):
            archivos_ignorados.append(f)
            continue
        archivos_validos.append(f)

    if archivos_ignorados:
        print("Archivos ignorados por contener null bytes (posibles binarios):")
        for archivo in archivos_ignorados:
            print(f"  - {archivo}")
        print()

    pares = [(archivos_validos[i], archivos_validos[i + 1]) for i in range(0, len(archivos_validos) - 1, 2)]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte = [f"=== Comparación realizada el {timestamp} ==="]
    if args.comentario:
        reporte.append(f"Comentario: {args.comentario}")
    reporte.append("")

    lineas_sospechosas = 0

    for archivo_a, archivo_b in pares:
        diferencias = comparar_archivos(archivo_a, archivo_b)
        if diferencias:
            reporte.append(f"Comparando: {archivo_a} vs {archivo_b}")
            reporte.append("-" * (len(reporte[-1])))
            for num_linea, linea_a, linea_b in diferencias:
                if tiene_no_imprimibles(linea_a) or tiene_no_imprimibles(linea_b):
                    lineas_sospechosas += 1
                reporte.append(f"Línea {num_linea}:")
                reporte.append(f"  {archivo_a}: {sanitizar(linea_a)}")
                reporte.append(f"  {archivo_b}: {sanitizar(linea_b)}")
                reporte.append("")  # Separador entre líneas
            reporte.append("")  # Separador entre comparaciones

    if lineas_sospechosas > 0:
        aviso = f"⚠️  Se detectaron {lineas_sospechosas} líneas con caracteres no imprimibles. Fueron sanitizadas."
        reporte.append(aviso)
        print("\n" + aviso)

    with open(LOG_FILENAME, "a", encoding="utf-8", errors="replace") as log:
        log.write("\n".join(reporte))
        log.write("\n\n==========\n\n")

    print(f'\n{len(pares)} pares comparados. Revisa "{LOG_FILENAME}" para ver diferencias.')

if __name__ == "__main__":
    main()
