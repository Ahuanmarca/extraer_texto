EXTRAER TEXTO DE IMÁGENES (.jpg, .png, .heic) USANDO PYTHON Y TESSERACT
======================================================================

1️⃣ Requisitos (solo la primera vez)
-----------------------------------
Instala las herramientas necesarias ejecutando en Terminal:

brew install tesseract libheif
pip install pillow pillow-heif pytesseract

2️⃣ Uso
-------
1. Coloca las imágenes que quieras procesar en una carpeta.
2. Abre Terminal y navega a la carpeta donde guardaste este proyecto.
3. Ejecuta el script:

   python extraer_texto.py

4. Cuando el script te pida el nombre de la carpeta con imágenes, 
   escribe el nombre (por ejemplo: "ejemplo").

5. El texto extraído se guardará en un archivo `.txt` con el mismo nombre
   que la carpeta (por ejemplo: `ejemplo.txt`).

6. Si hay errores, se guardarán en `ejemplo_errores.log`.

3️⃣ Compatibilidad
------------------
El script acepta imágenes en formato:
- .jpg
- .jpeg
- .png
- .heic (se convierten automáticamente a .jpg antes de procesar)

