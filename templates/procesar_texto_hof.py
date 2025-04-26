def procesar_texto(entrada, salida, *funciones):
    # Leer archivo de entrada
    with open(entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    log = []

    # Aplicar cada función procesadora en orden
    for funcion in funciones:
        lineas, log_entries = funcion(lineas)
        log.extend(log_entries)

    # Guardar resultado en archivo de salida
    with open(salida, 'w', encoding='utf-8') as f:
        f.writelines(lineas)

    return lineas, log
