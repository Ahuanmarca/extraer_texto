import pytest
from funciones.normalizadores_v2 import identificar_basurita  # Cambia 'formato' si tu archivo tiene otro nombre

@pytest.mark.parametrize("input_text, esperado", [
    ("""7. Desde el punto de vista tarifario, ¿cómo estructura Renfe Viajeros el servicio que ofrece a los viajeros? A a b C d En servicios públicos y privados. En servicios de baja, media o alta velocidad. En servicios comerciales y servicios sujetos a obligaciones de servicio público. En servicios de precios populares y servicios de primera clase.""",
     "A a b C d"),

    ("""16. ¿Puede un viajero con Título Multiviaje prolongar su recorrido fuera del Núcleo? Sí, debiendo regularizar su pago en ruta. Sí, previa comunicación y regularización de su pago en la estación de origen. No, la prolongación del recorrido está prohibida para todos los títulos y servicios. No, los Títulos Multiviaje no admiten prolongación del recorrido fuera del Núcleo. a b C o d ==""",
     "a b C o d =="),

    ("""24. En los casos en que Rede Viajeros decida limitar o excluir el transporte de mascotas, ¿cuándo debe informar al cliente de esta circunstancia? == a b C d Durante el trayecto. Antes de la compra del viaje. Antes de acceder al tren. Antes de acceder a la estación de origen. a A E""",
     "== a b C d"),

    ("""52. Una vez que un cliente potencial muestra interés en la marca o producto, comienza una fase en la que es esencial que la experiencia de compra sea fluida y satisfactoria, ¿cómo se denomina esa fase? a b C d map Fase de adquisición. Fase de consolidación. Apertura a nuevos mercados. Atracción y captación.""",
     "a b C d map"),

    ("""9. ¿Es posible fumar en las instalaciones y dependencias de Renfe, sin autorización expresa previa? a b C d — Sí, es un derecho del viajero. No, el viajero tiene la obligación de abstenerse de fumar. Sí, sin necesidad de consultar al personal de Renfe. Sí, previa consulta al personal de Renfe. A a""",
     "a b C d —"),

    ("""24. ¿Cuándo está obligada Renfe Viajeros a proporcionar asistencia al viajero en los términos establecidos en la legislación vigente? a b C a a d A En el caso de que el retraso de la salida o de la llegada sea superior a 60 minutos. En el caso de que el retraso de la salida o de la llegada sea superior a 120 minutos. En el caso de que el retraso de la salida o de la llegada sea superior a 30 minutos. Ante cualquier retraso en la salida o la llegada.""",
     "a b C a a d A"),

    ("""46. Cuando hablamos de gestionar y diseñar la experiencia de cliente, ¿cómo se denomina la herramienta o metodología que persigue analizar el porqué de lo que está pasando, empleando ambientes naturales y buscando significado en la información recogida, empleando técnicas como entrevistas o focus groups? Investigación cuantitativa. Investigación cualitativa. Arquetipos de cliente. Perfil de cliente. a b C a a d A""",
     "a b C a a d A"),

    ("""52. Dentro de las Herramientas para el diagnóstico de la Experiencia de Cliente, ¿cómo se denomina la técnica para un análisis holístico, desde la perspectiva del cliente, integrando la estructura y procesos de la compañía, los cuales resultan claves en el ofrecimiento de una experiencia memorable para el cliente? ) Arquetipo de cliente. ) Pasillo del Cliente. ) Mapa de procesos (Service Blueprint). ) Historial del cliente. O gw o""",
     "O gw o"),

    ("""11. ¿Cuál de las siguientes opciones no pertenece a uno de los niveles de la tarjeta Más Renfe? Tarjeta Más Renfe Clásica. Tarjeta Más Renfe Plata. Tarjeta Más Renfe Oro. Tarjeta Más Renfe Diamante. a b C ao? E d =-""",
     "a b C ao? E d =-"),

    ("""34. ¿Con qué hacemos referencia a propiciar las condiciones para lograr un adecuado equilibrio entre las responsabilidades personales, familiares y laborales? — a b C d Descanso personal. Adaptación del puesto de trabajo. Equiparación. Conciliación.""",
     "— a b C d"),

    ("""50. ¿Cómo se denomina la entrega por la empresa de una experiencia unificada, integrada y conectada a través de todos los canales, ya sea que el cliente esté interactuando desde un dispositivo electrónico o en un lugar físico? a b C d _— Omnicanalidad. Soporte electrónico. Experiencia de Cliente Digital. Entorno digital.""",
     "a b C d _—"),

    ("""3. AVLO puede ofrecer el siguiente Servicio en Tierra: Bar Móvil. Enchufes en cada asiento para carga de teléfonos y ordenadores. Servicio PlayRenfe y conexión. Servicio de asistencia para personas con discapacidad o movilidad reducida. — a b c d a E""",
     "— a b c d a E"),
])
def test_identificar_basurita(input_text, esperado):
    assert identificar_basurita(input_text) == esperado
