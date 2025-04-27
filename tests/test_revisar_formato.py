# tests/test_revisar_formato.py

import scripts.script_040_comprobar_formato as script_040

def test_revisar_formato_preguntas_respuestas():
    texto_entrada = (
        "1. ¿Cuál es la capital de Francia?\n"
        "a) París.\n"
        "b) Madrid.\n"
        "c) Londres.\n"
        "d) Berlín.\n"
        "\n"
        "1. a) París.\n"
        "París es la capital de Francia.\n"
        "\n"
        "2. ¿Cuánto es 2+2?\n"
        "a) 3.\n"
        "b) 5.\n"
        "c) 4.\n"
        "d) 6.\n"
        "\n"
        "2. c) 4.\n"
        "Es el resultado de sumar dos más dos.\n"
        "\n"
        "3. Esta pregunta está rota porque faltan opciones.\n"
        "a) Primera.\n"
        "b) Segunda.\n"
        "\n"
        "3. a) Primera.\n"
        "Explicación de la respuesta."
    )

    texto_corregido = script_040.main(texto_entrada)

    assert "---------- TO FIX ----------" in texto_corregido
    assert "1. ¿Cuál es la capital de Francia?" in texto_corregido
    assert "2. ¿Cuánto es 2+2?" in texto_corregido
    assert "3. Esta pregunta está rota" in texto_corregido
