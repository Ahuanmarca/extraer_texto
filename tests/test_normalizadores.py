import pytest
from funciones.normalizadores import limpiar_lineas_heic

def test_limpiar_lineas_heic():
    texto_entrada = """
===== IMG_1234.heic =====
1. ¿Cuál es la capital de Perú?
a) Lima
b) Arequipa
===== IMG_5678.heic =====
c) Cusco
d) Trujillo
""".strip()

    texto_esperado = """
1. ¿Cuál es la capital de Perú?
a) Lima
b) Arequipa
c) Cusco
d) Trujillo
""".strip()

    resultado = limpiar_lineas_heic(texto_entrada)
    assert resultado.strip() == texto_esperado


def test_lineas_heic_con_espacios_y_en_medio():
    texto_entrada = """
1. ¿Cuál es la capital?
a) Lima
   ===== IMG_0001.heic =====  
b) Cusco
""".strip()

    texto_esperado = """
1. ¿Cuál es la capital?
a) Lima
b) Cusco
""".strip()

    resultado = limpiar_lineas_heic(texto_entrada)
    assert resultado.strip() == texto_esperado
