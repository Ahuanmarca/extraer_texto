import re
import os
from collections import Counter
from funciones.debug import guardar_texto_con_timestamp

# NORMALIZADORES V1
from funciones.normalizadores import unir_palabras_partidas_por_guiones

# NORMALIZADORES V2
from funciones.normalizadores_v2 import eliminar_referencias_imagen
from funciones.normalizadores_v2 import eliminar_basurita_suelta
from funciones.normalizadores_v2 import insertar_espacio_tras_letra_y_parentesis_v2
from funciones.normalizadores_v2 import reemplazar_inicio_linea
from funciones.normalizadores_v2 import agregar_numeracion_respuestas_v2
from funciones.normalizadores_v2 import reemplazar_linea
from funciones.normalizadores_v2 import unir_oraciones_partidas_v3
from funciones.normalizadores_v2 import insertar_espacios_en_titulos_v1

# === RUTAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")


def main(texto, nombre_archivo_log=None):
    archivo_log = os.path.join(CARPETA_TRABAJO, f"{nombre_archivo_log}.log")
    log_advertencias = []
    nuevas_lineas = texto

    """
    Notas de acciones de normalización:
    - No se inserta posible espacio faltante tras numeración y punto, como "1.a)" - Al parecer no hay incidencias
    - No se elimina basurita al final de las líneas. Al parecer no es necesario en este caso, pero debería ser parte estándar del proceso.
    - Se eliminan "basuritas" manualmente porque no he logrado limpiarlas con un algoritmo más general.
    - Se reemplazan varias líneas manualmente porque no he logrado normalizarlas con un algoritmo más general.
    Se tendrían que corregir estos puntos para que esta herramienta pueda usarse en diferentes proyectos.
    Los pasos de limpieza deberían ser muy muy pequeños y robustos.
    Muchos pasos pequeños y robustos antes de hacer transformaciones grandes.
    """

    nuevas_lineas = eliminar_referencias_imagen(texto)
    nuevas_lineas = eliminar_basurita_suelta(
        nuevas_lineas,
        {
            "Ue",
            "*",
            "59%",
            "e",
            "”",
            "24,",
            "L",
            "9;",
            "19;",
            "32:",
            "SEL",
            "(6)",
            "|",
            "Preguntas de reserva",
        },
    )

    # PARCHANDO LÍNEAS UNA POR UNA - De forma manual e ineficiente!!
    # TODO: QUE FUNCIÓN LO HAGA EN UN SOLO VIAJE
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "1. a) Tanto en Cercanías como en Media Distancia Convencional podrá viajar de",
        "a) Tanto en Cercanías como en Media Distancia Convencional podrá viajar de",
    )
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "2. a)El protocolo rige para la totalidad de las personas pertenecientes a la empre-",
        "a) El protocolo rige para la totalidad de las personas pertenecientes a la empre-",
    )

    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "1. Cc) A una indemnización equivalente al 50 por ciento del precio del título de",
        "c) A una indemnización equivalente al 50 por ciento del precio del título de",
    )
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "2. b) Mediante la comunicación y la formación.",
        "b) Mediante la comunicación y la formación.",
    )
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "4. Abstenerse de fumar, distribuir publicidad, pegar carteles, mendigar, organizar ri- fas o",
        "Nr. 4. Abstenerse de fumar, distribuir publicidad, pegar carteles, mendigar, organizar ri- fas o",
    )
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "3. Arecibir antes del viaje, cuando así lo soliciten, la siguiente información:",
        "Nr. 3. Arecibir antes del viaje, cuando así lo soliciten, la siguiente información:",
    )
    nuevas_lineas = reemplazar_linea(
        nuevas_lineas,
        "2. Atender las indicaciones que les formule el personal de Renfe Viajeros o el personal",
        "Nr. 2. Atender las indicaciones que les formule el personal de Renfe Viajeros o el personal",
    )
    # nuevas_lineas = reemplazar_linea(
        # nuevas_lineas,
        # "Para calcular el NPS se pide a lo clientes",
        # "Nr. 1. NPS (Net Promoter Score) (...) Para calcular el NPS se pide a los clientes calificar",
    # )
    # TODO: ESTO LO DEBERÍA PILLAR LA FUNCIÓN insertar_espacio_tras_letra_y_parentesis_v2,
    # PERO NO LO HACE. NO SÉ LA CAUSA
    nuevas_lineas = reemplazar_linea(nuevas_lineas, "a)JPpi:", "a) JPpi:")
    nuevas_lineas = reemplazar_linea(nuevas_lineas, "4. a)NPS.", "a) NPS.")

    # OJO OJO --> Si lo pongo antes de reemplazar_linea, tengo que cambiar los strings en reemplazar_linea
    # OJO OJO --> No está pillando "a)JPpi:" en el último archivo.
    nuevas_lineas, log_lines = insertar_espacio_tras_letra_y_parentesis_v2(
        nuevas_lineas
    )

    # TODO: Volver a usar versión que sólo mira 8 primeros caracteres
    # TODO: Pasar líneas largas por función reemplazar_linea
    nuevas_lineas = reemplazar_inicio_linea(
        nuevas_lineas,
        [
            ("a) Asistencia psicológica. -En ", "-> a) Asistencia psicológica. -En "),
            (
                "b) Restitución de las víctimas. -En",
                "-> b) Restitución de las víctimas. -En",
            ),
            (
                "c) Seguimiento de incidentes de acoso. -Si",
                "-> c) Seguimiento de incidentes de acoso. -Si",
            ),
            ("Cc)", "c)"),
            ("cc)", "c)"),
            ("3Ma)", "a)"),
            ("C)", "c)"),
            ("1. NPS", "Nr. 1. NPS"),
            ("4. Abstenerse", "Nr. 4. Abstenerse"),
            ("4. A recibir", "Nr.4. A recibir")
        ],
    )

    nuevas_lineas, log_lines = agregar_numeracion_respuestas_v2(nuevas_lineas)
    nuevas_lineas = unir_oraciones_partidas_v3(nuevas_lineas)

    guardar_texto_con_timestamp(nuevas_lineas, "PRE")
    nuevas_lineas = insertar_espacios_en_titulos_v1(nuevas_lineas)
    guardar_texto_con_timestamp(nuevas_lineas, "POST")

    # === GUARDAR RESULTADOS ===
    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write("\nAdvertencias en proceso de normalización:\n")
        for advertencia in log_advertencias:
            f.write(advertencia + "\n")

    return nuevas_lineas


if __name__ == "__main__":
    main()
