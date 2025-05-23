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


def test_corregir_numeracion_preguntas_reserva_general():
    texto = (
        "60. ¿Cómo se denomina la era donde el acceso y la gestión de datos se convirtieron en un activo estratégico y, con el surgimiento de Internet y las tecnologías de la información, las empresas comenzaron a recopilar datos sobre sus clientes de manera más sistemática?\n"
        "a) Era de la información.\n"
        "b) Era de la distribución.\n"
        "c) Era digital.\n"
        "d) Era de la producción. Preguntas de reserva\n"
        "1. ¿Puede un cliente de Cercanías y Media Distancia Convencional sin plazas asignadas viajar de pie?\n"
        "a) Tanto en Cercanías como en Media Distancia Convencional podrá viajar de pie u ocupar un asiento, si está libre.\n"
        "b) Tanto en Cercanías como en Media Distancia Convencional se encuentra prohíbo viajar de pie.\n"
        "c) Podrá viajar de pie en Cercanías pero no en Media Distancia Convencional.\n"
        "d) Podrá viajar de pie en Media Distancia Convencional pero no en Cercanías.\n"
        "2. ¿Cuál es el ámbito personal de aplicación del Protocolo para la prevención de 4 ? los casos de acoso sexual, acoso por razón de sexo y acoso moral de Renfe?\n"
        "a) El protocolo rige para la totalidad de las personas pertenecientes a la empresa Renfe-Operadora.\n"
        "b) El protocolo rige para el personal directivo de Renfe-Operadora.\n"
        "c) El protocolo rige para los empleados de Renfe-Operadora que denuncien conductas de acoso sexual, acoso por razón de sexo o acoso moral.\n"
        "d) El protocolo rige para para todos los clientes de Renfe-Operadora.\n"
        "3. ¿Cuál de los siguientes no es uno de los principios de Cultura de Seguridad del Grupo Renfe?\n"
        "a) Seguridad como valor esencial.\n"
        "b) Apertura y confianza.\n"
        "c) Responsabilidad personal.\n"
        "d) Principio de legalidad.\n"
        "4. ¿Cuál de las siguientes fechas marcó el inicio de la era de la información?\n"
        "a) 1960.\n"
        "b) 1990\n"
        "c) 2010\n"
        "d) 1998 En MADTEST tienes más preguntas, y todos tus avances quedan hy SN registrados y se reflejan en el ranking. IS ¡Supera tus límites con MADTEST! o MA A rr ronene\n"
    )

    texto_esperado = (
        "60. ¿Cómo se denomina la era donde el acceso y la gestión de datos se convirtieron en un activo estratégico y, con el surgimiento de Internet y las tecnologías de la información, las empresas comenzaron a recopilar datos sobre sus clientes de manera más sistemática?\n"
        "a) Era de la información.\n"
        "b) Era de la distribución.\n"
        "c) Era digital.\n"
        "d) Era de la producción. Preguntas de reserva\n"
        "61. ¿Puede un cliente de Cercanías y Media Distancia Convencional sin plazas asignadas viajar de pie?\n"
        "a) Tanto en Cercanías como en Media Distancia Convencional podrá viajar de pie u ocupar un asiento, si está libre.\n"
        "b) Tanto en Cercanías como en Media Distancia Convencional se encuentra prohíbo viajar de pie.\n"
        "c) Podrá viajar de pie en Cercanías pero no en Media Distancia Convencional.\n"
        "d) Podrá viajar de pie en Media Distancia Convencional pero no en Cercanías.\n"
        "62. ¿Cuál es el ámbito personal de aplicación del Protocolo para la prevención de 4 ? los casos de acoso sexual, acoso por razón de sexo y acoso moral de Renfe?\n"
        "a) El protocolo rige para la totalidad de las personas pertenecientes a la empresa Renfe-Operadora.\n"
        "b) El protocolo rige para el personal directivo de Renfe-Operadora.\n"
        "c) El protocolo rige para los empleados de Renfe-Operadora que denuncien conductas de acoso sexual, acoso por razón de sexo o acoso moral.\n"
        "d) El protocolo rige para para todos los clientes de Renfe-Operadora.\n"
        "63. ¿Cuál de los siguientes no es uno de los principios de Cultura de Seguridad del Grupo Renfe?\n"
        "a) Seguridad como valor esencial.\n"
        "b) Apertura y confianza.\n"
        "c) Responsabilidad personal.\n"
        "d) Principio de legalidad.\n"
        "64. ¿Cuál de las siguientes fechas marcó el inicio de la era de la información?\n"
        "a) 1960.\n"
        "b) 1990\n"
        "c) 2010\n"
        "d) 1998 En MADTEST tienes más preguntas, y todos tus avances quedan hy SN registrados y se reflejan en el ranking. IS ¡Supera tus límites con MADTEST! o MA A rr ronene\n"
    )

    from funciones.normalizadores import corregir_numeracion_preguntas_reserva_general

    resultado = corregir_numeracion_preguntas_reserva_general(texto)
    assert resultado == texto_esperado


def test_eliminar_basurita_final(capsys):
    texto_entrada = (
        "d) Oferta-demanda. p A E\n"
        "b) Otra línea buena.\n"
        "c) Sin problema p A E\n"
        "d) Línea limpia\n"
    )
    texto_esperado = (
        "d) Oferta-demanda.\n"
        "b) Otra línea buena.\n"
        "c) Sin problema\n"
        "d) Línea limpia"
    )

    basuritas = {"p A E"}

    from funciones.normalizadores import eliminar_basurita_final

    resultado = eliminar_basurita_final(texto_entrada, basuritas)

    assert resultado == texto_esperado

    # Verificar que mostró algo en consola
    captured = capsys.readouterr()
    assert "Corrigiendo línea" in captured.out
    assert "Antes:" in captured.out
    assert "Después:" in captured.out


def test_reemplazar_letras_en_bloques():
    texto_entrada = (
        "15. d) Todas las anteriores son correctas.\n"
        "\u201cLas formas de pago admitidas por Rende Viaje son:\n"
        "a) Met\u00e1lico en moneda de curso legal en Espa\u00f1a.\n"
        "b) Tarjetas de cr\u00e9dito / d\u00e9bito aceptadas por Renfe Viajeros.\n"
        "c) Puntos de las tarjetas del programa de fidelizaci\u00f3n de Rende Viajeros.\n"
        "d) Cualquiera otra regulada al efecto\u201d\n"
        "16. c) Los gastos de gesti\u00f3n no podr\u00e1n superar el 10 % del importe del t\u00edtulo de\n"
        "transporte."
    )

    texto_esperado = (
        "15. d) Todas las anteriores son correctas.\n"
        "\u201cLas formas de pago admitidas por Rende Viaje son:\n"
        "- Met\u00e1lico en moneda de curso legal en Espa\u00f1a.\n"
        "- Tarjetas de cr\u00e9dito / d\u00e9bito aceptadas por Renfe Viajeros.\n"
        "- Puntos de las tarjetas del programa de fidelizaci\u00f3n de Rende Viajeros.\n"
        "- Cualquiera otra regulada al efecto\u201d\n"
        "16. c) Los gastos de gesti\u00f3n no podr\u00e1n superar el 10 % del importe del t\u00edtulo de\n"
        "transporte."
    )

    from funciones.normalizadores import reemplazar_letras_en_bloques
    resultado = reemplazar_letras_en_bloques(texto_entrada)

    assert resultado.strip() == texto_esperado.strip()


if __name__ == "__main__":
    pytest.main()
