from scripts import script_210_combinar_preguntas_respuestas as script_210

def test_combinar_preguntas_respuestas():
    texto_preguntas = (
        "1. Pregunta uno\n"
        "a) Opción 1\n"
        "b) Opción 2\n"
        "c) Opción 3\n"
        "d) Opción 4\n"
        "\n"
        "2. Pregunta dos (con problemas)\n"
        "a) Opción A\n"
        "b) Opción B\n"
    )

    texto_respuestas = (
        "1. a) Respuesta correcta uno\n"
        "\n"
        "2. b) Respuesta correcta dos\n"
    )

    esperado = (
        "1. Pregunta uno\n"
        "a) Opción 1\n"
        "b) Opción 2\n"
        "c) Opción 3\n"
        "d) Opción 4\n"
        "\n"
        "1. a) Respuesta correcta uno\n"
        "\n"
        "2. Pregunta dos (con problemas)\n"
        "a) Opción A\n"
        "b) Opción B\n"
        "\n"
        "2. b) Respuesta correcta dos"
    )

    resultado = script_210.main(texto_preguntas, texto_respuestas)

    assert resultado.strip() == esperado.strip()
