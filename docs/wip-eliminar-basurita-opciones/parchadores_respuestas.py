import re


def eliminar_basurita_final_preguntas_pegadas_con_opciones(texto: str) -> str:
    """
    Elimina cualquier 'basurita' al final del bloque de texto,
    quedándose con todo hasta el último punto final.
    """
    idx = texto.rfind(".")
    if idx == -1:
        return texto  # No hay punto final, no recortamos nada
    return texto[: idx + 1]


def separar_en_oraciones(texto: str) -> str:
    """
    Separa un bloque de texto en 5 oraciones: 1 pregunta + 4 opciones.
    Devuelve un string multilínea.
    """
    # Detecta los finales de oración: ".", "?" o ":"
    oraciones = re.split(r"(?<=[\.\?:])\s+", texto.strip())

    if len(oraciones) < 5:
        raise ValueError("No se detectaron al menos 5 oraciones")

    # Junta las cinco primeras oraciones (pueden contener basurita al final)
    return "\n".join(oraciones[:5])
