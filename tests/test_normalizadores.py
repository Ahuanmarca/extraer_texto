import pytest
from funciones.normalizadores import corregir_numeracion_y_letras
from funciones.normalizadores import corregir_letras_duplicadas
from funciones.normalizadores import insertar_linea_vacia_antes_numeracion
from funciones.normalizadores import unir_oraciones_partidas

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


if __name__ == "__main__":
    pytest.main()
