import os

def main(entrada, salida, archivo_log):
    # === LECTURA DEL ARCHIVO DE ENTRADA ===
    if not os.path.isfile(entrada):
        print(f"❌ No se encontró el archivo de entrada: {entrada}")
        return

    with open(entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # === TODO: Procesamiento personalizado ===
    # Aquí puedes aplicar funciones que modifiquen la lista `lineas`
    # Por ejemplo:
    # lineas = limpiar_lineas_heic(lineas)
    # lineas = aplicar_normalizacion(lineas)
    # etc.

    # === GUARDAR EL ARCHIVO DE SALIDA ===
    with open(salida, 'w', encoding='utf-8') as f:
        for linea in lineas:
            f.write(linea)

    # === GUARDAR EL LOG (si es necesario) ===
    with open(archivo_log, 'a', encoding='utf-8') as log:
        log.write("✅ Archivo procesado correctamente.\n")
        log.write(f"📥 Entrada: {entrada}\n")
        log.write(f"📤 Salida: {salida}\n")
        log.write(f"📝 Total líneas procesadas: {len(lineas)}\n")

    print("✅ Proceso completado con éxito.")

if __name__ == "__main__":
    # Ejemplo de uso manual para pruebas:
    # main("carpeta_trabajo/archivo_original.txt", "carpeta_trabajo/archivo_modificado.txt", "carpeta_trabajo/archivo.log")

    # O usar argumentos si lo deseas en el futuro con sys.argv
    pass
