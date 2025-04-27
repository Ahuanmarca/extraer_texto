import re

def es_linea_pregunta(linea):
    return bool(re.match(r'^(\d+)\.\s*(.*)', linea))

def normalizar_opcion(linea):
    match = re.match(r'^[\-\s]*([a-dA-D])[a-dA-D]?\)+\s*(.*)', linea)
    if match:
        letra = match.group(1).lower()
        texto = match.group(2).strip()
        return f"{letra}) {texto}", letra
    return None, None

def es_referencia_imagen(linea):
    return "===== IMG_" in linea and ".heic =====" in linea
