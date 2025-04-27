import pytest
from funciones.normalizadores import corregir_numeracion_y_letras
from funciones.normalizadores import corregir_letras_duplicadas
from funciones.normalizadores import insertar_linea_vacia_antes_numeracion
from funciones.normalizadores import unir_oraciones_partidas
from funciones.normalizadores import unir_palabras_partidas_por_guiones
from funciones.normalizadores import reemplazar_texto_por_linea_vacia
from funciones.normalizadores import insertar_espacio_entre_punto_y_letra
from funciones.normalizadores import unir_numeracion_con_letra
from funciones.normalizadores import insertar_espacio_tras_letra_y_parentesis


def test_corregir_numeracion_y_letras():
    texto_entrada = """
1. Cc) Servicios de Cercanías.
"Los Servicios Comerciales son..."
2. d) Real Decreto Legislativo 6/2015...
3. b) AVE, Avlo, Alvia, Euromed e Intercity.
b) Título de transporte.
a) El cliente tiene la obligación de...
Cc) El sexo del cliente.
c) En servicios comerciales...
8. Cc) Acuerdo del Consejo de Ministros.
""".strip()

    texto_esperado = """
1. Cc) Servicios de Cercanías.
"Los Servicios Comerciales son..."
2. d) Real Decreto Legislativo 6/2015...
3. b) AVE, Avlo, Alvia, Euromed e Intercity.
4. b) Título de transporte.
5. a) El cliente tiene la obligación de...
6. c) El sexo del cliente.
7. c) En servicios comerciales...
8. Cc) Acuerdo del Consejo de Ministros.
""".strip()

    resultado = corregir_numeracion_y_letras(texto_entrada)
    assert resultado.strip() == texto_esperado.strip()


def test_corregir_letras_duplicadas():
    texto_entrada = """
1. Cc) Servicios de Cercanías.
2. d) Real Decreto Legislativo 6/2015.
3. Bb) AVE, Avlo, Alvia, Euromed e Intercity.
4. aa) Título de transporte.
5. b) El cliente tiene la obligación de conservar el título de transporte.
6. c) El sexo del cliente.
"""

    texto_esperado = """
1. c) Servicios de Cercanías.
2. d) Real Decreto Legislativo 6/2015.
3. b) AVE, Avlo, Alvia, Euromed e Intercity.
4. a) Título de transporte.
5. b) El cliente tiene la obligación de conservar el título de transporte.
6. c) El sexo del cliente.
"""

    resultado = corregir_letras_duplicadas(texto_entrada)
    assert resultado.strip() == texto_esperado.strip()


def test_insertar_linea_vacia_antes_numeracion():
    texto_entrada = """1. c) Servicios de Cercanías.
Texto cualquiera.
2. d) Real Decreto Legislativo.
Más texto aquí.
8. c) Error de numeración (debería ignorarse).
3. b) AVE, Avlo, Alvia, Euromed e Intercity.
Texto final.
"""
    texto_esperado = """1. c) Servicios de Cercanías.
Texto cualquiera.

2. d) Real Decreto Legislativo.
Más texto aquí.
8. c) Error de numeración (debería ignorarse).

3. b) AVE, Avlo, Alvia, Euromed e Intercity.
Texto final.
""".strip()

    resultado = insertar_linea_vacia_antes_numeracion(texto_entrada)
    assert resultado.strip() == texto_esperado


def test_unir_oraciones_partidas():
    texto_entrada = """Hola, me
llamo Renzo.

7. c) En servicios comerciales y servicios sujetos a obligaciones de servicio público
“Desde el punto de vista tarifario. Renfe Viajeros estructura el servicio que ofrece a
los viajeros en: servicios comerciales y servicios sujetos a obligaciones de servicio
público”."""

    texto_esperado = """Hola, me llamo Renzo.

7. c) En servicios comerciales y servicios sujetos a obligaciones de servicio público
“Desde el punto de vista tarifario. Renfe Viajeros estructura el servicio que ofrece a los viajeros en: servicios comerciales y servicios sujetos a obligaciones de servicio público”."""

    resultado = unir_oraciones_partidas(texto_entrada)
    assert resultado.strip() == texto_esperado.strip()


# Vamos a "simular" el input del usuario para los tests
# usando un mock (parcheo de la función built-in input)


def test_unir_palabras_partidas_por_guiones(monkeypatch):
    texto_entrada = (
        "Este es un ejemplo públi- cos de palabras par- tidas.\n"
        "Aquí hay más tan- to errores.\n"
        "Aquí NO hay errores.\n"
    )

    # Simulamos siempre responder 'y' (yes) cuando pregunte
    monkeypatch.setattr("builtins.input", lambda _: "y")

    texto_esperado = (
        "Este es un ejemplo públicos de palabras partidas.\n"
        "Aquí hay más tanto errores.\n"
        "Aquí NO hay errores.\n"
    )

    resultado = unir_palabras_partidas_por_guiones(texto_entrada)

    assert resultado.strip() == texto_esperado.strip()


def test_reemplazar_texto_por_linea_vacia():
    # Caso 1: En medio de la línea
    texto = "Lorem Ipsum Preguntas de reserva Hello World"
    esperado = "Lorem Ipsum\n\nHello World"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado

    # Caso 2: Línea propia
    texto = "Lorem Ipsum\nPreguntas de reserva\nHello World"
    esperado = "Lorem Ipsum\n\nHello World"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado

    # Caso 3: Final de línea
    texto = "Lorem Ipsum Preguntas de reserva\nHello World"
    esperado = "Lorem Ipsum\n\nHello World"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado

    # Caso 4: Inicio de línea
    texto = "Lorem Ipsum\nPreguntas de reservaHello World"
    esperado = "Lorem Ipsum\n\nHello World"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado

    # Caso 5: Varias apariciones
    texto = "A Preguntas de reserva B Preguntas de reserva C"
    esperado = "A\n\nB\n\nC"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado

    # Caso 6: No cambia otras líneas vacías
    texto = "A\n\nPreguntas de reserva\n\nB"
    esperado = "A\n\n\n\nB"
    assert reemplazar_texto_por_linea_vacia(texto, "Preguntas de reserva") == esperado


def test_insertar_espacio_entre_punto_y_letra():
    # Casos que deberían ser corregidos
    texto_entrada = "1.a) Lorem Ipsum\n24.c) Hello World\n60.b) Otro texto"
    texto_esperado = "1. a) Lorem Ipsum\n24. c) Hello World\n60. b) Otro texto"
    assert (
        insertar_espacio_entre_punto_y_letra(texto_entrada).rstrip()
        == texto_esperado.rstrip()
    )

    # Casos que NO deberían ser modificados
    texto_entrada_no_cambiar = "2.Lorem Ipsum\n15.Otra frase\n5. Hello World"
    texto_esperado_no_cambiar = "2.Lorem Ipsum\n15.Otra frase\n5. Hello World"
    assert (
        insertar_espacio_entre_punto_y_letra(texto_entrada_no_cambiar).rstrip()
        == texto_esperado_no_cambiar.rstrip()
    )

    # Mezcla de corregibles y no corregibles
    texto_entrada_mixto = "1.a) Primera\n2.Lorem Ipsum\n3.b) Segunda\n4.Hola Mundo"
    texto_esperado_mixto = "1. a) Primera\n2.Lorem Ipsum\n3. b) Segunda\n4.Hola Mundo"
    assert (
        insertar_espacio_entre_punto_y_letra(texto_entrada_mixto).rstrip()
        == texto_esperado_mixto.rstrip()
    )


def test_unir_numeracion_con_letra():
    texto_entrada = (
        "1.\n"
        "a) Lorem Ipsum\n"
        "2.\n"
        "Cc) Otro ejemplo\n"
        "3. c) Todo bien\n"
        "4.\n"
        "b) Final feliz\n"
        "5.\n"
        "Texto sin opción"  # No es opción, no debe unirse
    )

    texto_esperado = (
        "1. a) Lorem Ipsum\n"
        "2. c) Otro ejemplo\n"
        "3. c) Todo bien\n"
        "4. b) Final feliz\n"
        "5.\n"
        "Texto sin opción"
    )

    resultado = unir_numeracion_con_letra(texto_entrada)
    assert resultado == texto_esperado


def test_insertar_espacio_tras_letra_y_parentesis():
    texto_entrada = (
        "a)Lorem Ipsum\n"
        "b)Dolor sit amet\n"
        "Aquí no cambia nada\n"
        "c)Otro ejemplo\n"
        "Texto normal d)Más texto seguido"
    )

    texto_esperado = (
        "a) Lorem Ipsum\n"
        "b) Dolor sit amet\n"
        "Aquí no cambia nada\n"
        "c) Otro ejemplo\n"
        "Texto normal d) Más texto seguido"
    )

    resultado = insertar_espacio_tras_letra_y_parentesis(texto_entrada)

    assert resultado == texto_esperado


if __name__ == "__main__":
    pytest.main()
