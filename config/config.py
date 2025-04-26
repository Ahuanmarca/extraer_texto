import os

# === BASE_DIR: carpeta raíz del proyecto ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === RUTAS RELATIVAS ===
CARPETA_TRABAJO = os.path.join(BASE_DIR, "carpeta_trabajo")
IMAGENES_CRUDAS = os.path.join(BASE_DIR, "imagenes_crudas")
DICCIONARIO_PATH = os.path.join(BASE_DIR, "diccionario.txt")
