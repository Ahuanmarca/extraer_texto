from scripts import (
    script_01_extraer_preguntas as script_01,
    script_02_normalizar_preguntas as script_02,
    script_03_limpiar_guiones as script_03,
)

def main():
    script_01.main()
    script_02.main()
    script_03.main()

if __name__ == "__main__":
    main()
