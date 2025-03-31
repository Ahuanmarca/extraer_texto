import re
import os

# === DICCIONARIO BÁSICO (puedes ampliarlo o cargarlo desde archivo) ===
diccionario_es = {
    "distancia", "transporte", "viajeros", "mercado", "servicio", "movilidad",
    "contrato", "billete", "viaje", "seguridad", "cliente", "media", "larga",
    "normativa", "plaza", "grupo", "personal", "documento", "acceso", "título",
    "oferta", "coche", "clase", "asiento", "factura", "validez", "anulación",
    "anterior", "posterior", "valor", "precio", "conductor", "renfe"
    # Añade más palabras según necesites
}

def palabra_valida(palabra):
    return palabra.lower() in diccionario_es

# === ENTRADA ===
nombre_archivo = input("Introduce el nombre del archivo .txt a revisar (sin extensión): ").strip()
archivo_entrada = f"{nombre_archivo}.txt"
archivo_salida = f"{nombre_archivo}_modificado.txt"
archivo_log = f"{nombre_archivo}_log.txt"

# === LECTURA ===
with open(archivo_entrada, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

nuevas_lineas = []
log_modificaciones = []

# Secuencia ANSI para resaltar (color amarillo en negrita)
COLOR_BEGIN = "\033[1;33m"
COLOR_END = "\033[0m"

# Procesamos cada línea (separamos por líneas para facilitar el log)
for i, linea in enumerate(lineas, 1):
    # Buscamos ocurrencias del patrón: palabra-guión-espacio-palabra
    ocurrencias = list(re.finditer(r'(\w+)-\s(\w+)', linea))
    if not ocurrencias:
        nuevas_lineas.append(linea)
        continue

    linea_modificada = linea  # inicializamos
    offset = 0  # compensación por cambios de longitud

    for match in ocurrencias:
        # Extraemos las dos partes
        palabra1, palabra2 = match.group(1), match.group(2)
        palabra_completa = palabra1 + palabra2

        start, end = match.start() + offset, match.end() + offset
        original_fragmento = linea_modificada[start:end]
        propuesto = palabra_completa  # al eliminar "- " se unen las dos partes

        # Preparar versiones resaltadas para el prompt
        # Se resalta la parte a modificar en el contexto de la línea
        destacado_original = (
            linea_modificada[:start] +
            COLOR_BEGIN + linea_modificada[start:end] + COLOR_END +
            linea_modificada[end:]
        )
        destacado_propuesto = (
            linea_modificada[:start] +
            COLOR_BEGIN + propuesto + COLOR_END +
            linea_modificada[end:]
        )

        # Si la palabra resultante existe en el diccionario, corregimos automáticamente
        if palabra_valida(palabra_completa):
            linea_modificada = linea_modificada[:start] + propuesto + linea_modificada[end:]
            offset -= len("- ")
            print(f"✔️ Línea {i}: '{original_fragmento}' corregido automáticamente a '{propuesto}'")
        else:
            # Mostrar el prompt con contexto y resaltado
            print(f"\nLínea {i}:")
            print(f"Original : {linea.strip()}\n")
            print(f"Opción A (eliminar '- '):")
            print(f"{destacado_propuesto}")
            print(f"Opción B (mantener '- '):")
            print(f"{destacado_original}")
            decision = input("¿Eliminar '- '? (y/n) [n]: ").strip().lower()
            if decision == 'y':
                linea_modificada = linea_modificada[:start] + propuesto + linea_modificada[end:]
                offset -= len("- ")
                print("✔️ Eliminado.")
            else:
                print("⏩ Mantenido.")

    if linea_modificada != linea:
        log_modificaciones.append(
            f"Línea {i}:\n- Original : {linea.strip()}\n- Modificada: {linea_modificada.strip()}\n"
        )
    nuevas_lineas.append(linea_modificada)

# === GUARDAR RESULTADOS ===
with open(archivo_salida, 'w', encoding='utf-8') as f:
    f.writelines(nuevas_lineas)

with open(archivo_log, 'w', encoding='utf-8') as f:
    for entrada in log_modificaciones:
        f.write(entrada + '\n')

print(f"\n✅ Archivo modificado guardado como: {archivo_salida}")
print(f"📝 Log de cambios guardado como: {archivo_log}")
