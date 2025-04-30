import re
import pytest
from funciones.normalizadores_v2 import eliminar_referencias_imagen
from funciones.normalizadores_v2 import insertar_espacio_tras_letra_y_parentesis_v2


def test_eliminar_referencias_imagen():
    entrada = """===== IMG_1234.heic =====
Primera línea
Segunda línea
===== IMG_5678.heic =====
Tercera línea"""

    esperado = """Primera línea
Segunda línea
Tercera línea"""

    assert eliminar_referencias_imagen(entrada) == esperado


def test_insertar_espacio_basico():
    texto = """a)Opción uno
b)Opción dos
c)Tercera opción
d)Última opción"""
    esperado = """a) Opción uno
b) Opción dos
c) Tercera opción
d) Última opción"""

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado


def test_insertar_espacio_con_lineas_bien_formateadas():
    texto = """a) Opción uno
b) Opción dos
c) Tercera opción
d) Última opción"""
    esperado = texto  # No debería cambiar

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado


def test_no_insertar_si_patron_en_medio_de_linea():
    texto = """Este es un ejemplo a)b)mal puesto.
O esta otra línea d)sin corregir."""
    esperado = """Este es un ejemplo a)b)mal puesto.
O esta otra línea d)sin corregir."""  # No debe cambiar nada

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado


def test_lineas_que_no_coinciden():
    texto = """1. Algo
X) Algo más
cc) Algo diferente"""
    esperado = texto  # No debería cambiar

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado


def test_patrones_minusculas_y_mayusculas():
    texto = """A)Primera
b)Segunda
C)Tercera
d)Cuarta"""
    esperado = """A) Primera
b) Segunda
C) Tercera
d) Cuarta"""

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado


def test_linea_vacia_y_lineas_normales():
    texto = """a)Primera opción

Texto normal sin cambios.

b)Segunda opción"""
    esperado = """a) Primera opción

Texto normal sin cambios.

b) Segunda opción"""

    assert insertar_espacio_tras_letra_y_parentesis_v2(texto) == esperado



from funciones.normalizadores_v2 import eliminar_basuritas_inicio


def test_eliminar_basuritas_inicio_basico():
    texto = """#$hello, world
I took CS50!#$
FooBarRenzo
FooBarFooBarBelon
Esta linea no se debería modificar."""
    esperado = """hello, world
I took CS50!#$
Renzo
FooBarBelon
Esta linea no se debería modificar."""

    resultado = eliminar_basuritas_inicio(texto, {"#$", "FooBar"})
    assert resultado == esperado


def test_eliminar_basuritas_inicio_no_cambia_lineas_sanas():
    texto = """Hola mundo
Prueba normal
Sin basura al inicio"""
    esperado = texto

    resultado = eliminar_basuritas_inicio(texto, {"#$", "FooBar"})
    assert resultado == esperado


def test_eliminar_basuritas_inicio_solo_una_vez():
    texto = """FooBarFooBarFooBarHola"""
    esperado = """FooBarFooBarHola"""

    resultado = eliminar_basuritas_inicio(texto, {"FooBar"})
    assert resultado == esperado


def test_eliminar_basuritas_inicio_multiple_sets():
    texto = """ABChello
XYZworld
123test"""
    esperado = """hello
world
test"""

    resultado = eliminar_basuritas_inicio(texto, {"ABC", "XYZ", "123"})
    assert resultado == esperado


# def test_eliminar_basuritas_inicio_con_espacios():
#     texto = """  FooBarHola mundo
#       #$Prueba"""
#     esperado = """  FooBarHola mundo
#       Prueba"""
    
#     resultado = eliminar_basuritas_inicio(texto, {"#$"})
#     assert resultado == esperado



def test_eliminar_basuritas_inicio_linea_vacia():
    texto = """

FooBarTexto"""
    esperado = """

Texto"""

    resultado = eliminar_basuritas_inicio(texto, {"FooBar"})
    assert resultado == esperado


def test_eliminar_basuritas_inicio_no_elimina_medio_linea():
    texto = """Hola FooBarMundo"""
    esperado = """Hola FooBarMundo"""

    resultado = eliminar_basuritas_inicio(texto, {"FooBar"})
    assert resultado == esperado
