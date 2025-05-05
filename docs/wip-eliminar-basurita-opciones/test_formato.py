import pytest
from funciones.normalizadores_v2 import extraer_pregunta_formateada  # Cambia 'formato' si tu archivo se llama distinto

def test_caso_1():
    input_text = """7. Desde el punto de vista tarifario, ¿cómo estructura Renfe Viajeros el servicio que ofrece a los viajeros? A a b C d En servicios públicos y privados. En servicios de baja, media o alta velocidad. En servicios comerciales y servicios sujetos a obligaciones de servicio público. En servicios de precios populares y servicios de primera clase."""
    esperado = """7. Desde el punto de vista tarifario, ¿cómo estructura Renfe Viajeros el servicio que ofrece a los viajeros?
a) En servicios públicos y privados.
b) En servicios de baja, media o alta velocidad.
c) En servicios comerciales y servicios sujetos a obligaciones de servicio público.
d) En servicios de precios populares y servicios de primera clase."""
    assert extraer_pregunta_formateada(input_text) == esperado

def test_caso_2():
    input_text = """16. ¿Puede un viajero con Título Multiviaje prolongar su recorrido fuera del Núcleo? Sí, debiendo regularizar su pago en ruta. Sí, previa comunicación y regularización de su pago en la estación de origen. No, la prolongación del recorrido está prohibida para todos los títulos y servicios. No, los Títulos Multiviaje no admiten prolongación del recorrido fuera del Núcleo. a b C o d =="""
    esperado = """16. ¿Puede un viajero con Título Multiviaje prolongar su recorrido fuera del Núcleo?
a) Sí, debiendo regularizar su pago en ruta.
b) Sí, previa comunicación y regularización de su pago en la estación de origen.
c) No, la prolongación del recorrido está prohibida para todos los títulos y servicios.
d) No, los Títulos Multiviaje no admiten prolongación del recorrido fuera del Núcleo."""
    assert extraer_pregunta_formateada(input_text) == esperado

def test_caso_3():
    input_text = """34. ¿Con qué hacemos referencia a propiciar las condiciones para lograr un adecuado equilibrio entre las responsabilidades personales, familiares y laborales? — a b C d Descanso personal. Adaptación del puesto de trabajo. Equiparación. Conciliación."""
    esperado = """34. ¿Con qué hacemos referencia a propiciar las condiciones para lograr un adecuado equilibrio entre las responsabilidades personales, familiares y laborales?
a) Descanso personal.
b) Adaptación del puesto de trabajo.
c) Equiparación.
d) Conciliación."""
    assert extraer_pregunta_formateada(input_text) == esperado

def test_caso_4_output_b_aceptable():
    input_text = """52. Dentro de las Herramientas para el diagnóstico de la Experiencia de Cliente, ¿cómo se denomina la técnica para un análisis holístico, desde la perspectiva del cliente, integrando la estructura y procesos de la compañía, los cuales resultan claves en el ofrecimiento de una experiencia memorable para el cliente? ) Arquetipo de cliente. ) Pasillo del Cliente. ) Mapa de procesos (Service Blueprint). ) Historial del cliente. O gw o"""
    output = extraer_pregunta_formateada(input_text)
    assert "52. Dentro de las Herramientas" in output
    assert output.count("\n") >= 4
    assert all(letra in output for letra in ["a)", "b)", "c)", "d)"])

def test_error_si_menos_de_cuatro_opciones():
    texto = """1. ¿Qué día es hoy? Mañana. Pasado mañana. Ayer."""
    with pytest.raises(ValueError):
        extraer_pregunta_formateada(texto)
