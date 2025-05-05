# TODO

[ ] Hacer que las funciones sean mas "puras".
[ ] En vez de modificar directamente diccionario.txt, retornar nueva versión y que main.py lo guarde, o que lo haga el script que usa la función.
[ ] Que todas las funciones que generan log retornen el log en vez de escribir en archivos log directamente. Que los scripts pasen estos logs a main.py, que main.py sea el único encargado de decidir qué logs se escriben y qué logs no se escriben.
[ ] Al normalizar preguntas, falta lograr separar preguntas pegadas a las opciones (ver wip-eliminar-basurita-opciones). Idealmente también eliminar la basurita en las opciones.
[ ] Separar más los pasos de la normalización de las preguntas / opciones, como las respuestas.
[ ] Lograr que la extracción funcione sin necesidad de separar las preguntas y respuestas en dos carpetas. Tendría que haber lógica para separarlas a partir de las capturas crudas. Lograrlo implicaría refactorizar todo el código que asume dos carpetas.
[ ] Una mejora de lo anterior: Lograr que se haga la extracción con todoas las imágenes crudas en una única carpeta. Esto implicaría que haya lógica para separar los diferentes cuestionarios (repetición de numeraciones?).
[ ] Tener una API o un archivo de configuración para definir ciertos criterios, para que no sean tan rígidos y ajustados a este único caso de captura. Por ejemplo, que se pueda configurar cuantas unidades grandes se tienen que buscar (como cuestionarios comopletos), con qué criterios separarlos (numeraciones), etc.
[ ] Que los pasos no transformen todo el texto una y otra vez. Que los pasos se puedan agregar o pasar a una HOF, y que se haga un loop eficiente.
[ ] Hacer más robustos los pasos individuales, y hacerlos lo más reutlizables posibles, como para que funcionen en cualquier texto capturado.
[ ] Solucionar problema del diccionario" se jode si el usuario decide mal.

