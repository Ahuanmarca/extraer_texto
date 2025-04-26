from funciones.normalizadores import corregir_numeracion_y_letras

def main():
    lineas_corregidas = corregir_numeracion_y_letras(texto_1)
    print("".join(lineas_corregidas))

texto_1 = """
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


texto_2 = """1. Cc) Servicios de Cercanías.
“Los Servicios Comerciales son aquellos que atienden las necesidades de demanda
de movilidad del mercado y se prestan en régimen de libre competencia y pluralidad
de oferta.
Los servicios considerados comerciales son:
- Alta Velocidad-Larga Distancia.
- Larga Distancia.
Trenes Turísticos, cuyas Condiciones Generales de contratación se encuentran a
disposición de los clientes en la web de Renfe”.
2. d) Real Decreto Legislativo 6/2015, de 30 de octubre, por el que se aprueba
el texto refundido de la Ley sobre Tráfico, Circulación de Vehículos a Motor y
Seguridad Vial.
Los servicios sujetos a obligaciones de servicio público por la Administración General del
Estado, que debe prestar Renfe Viajeros en la red ferroviaria de interés general son los
definidos en Acuerdo del Consejo de Ministros, de conformidad con el Reglamento (CE)
1370/2007 del Parlamento y Consejo, de 23 de octubre de 2007 sobre los servicios públi-
cos de transporte de viajeros por ferrocarril y carretera y con lo dispuesto en el artículo
59.1 de la Ley 38/2015, de 29 de septiembre del sector ferroviario”.
3. b) AVE, Avlo, Alvia, Euromed e Intercity.
Los tipos de servicios sometidos a obligaciones de servicio público son:
- Alta Velocidad-Media Distancia.
Servicios de Media Distancia que circulan por vías de ancho métrico o ibérico/red
de ancho convencional.
Servicios de Cercanías que discurren por vías de ancho métrico o ibérico/red de
ancho convencional.
Por el contrario, “b) AVE, Avlo, Alvia, Euromed e Intercity” son servicios comerciales
regulados por los parámetros de oferta/demanda y costes/beneficios que no pueden
recibir financiación pública porque supondría una competencia desleal para el resto
de operadores de transporte de viajeros”.
b) Título de transporte.
“El título de transporte es el documento que formaliza el contrato de transporte, tan-
to oneroso como gratuito, entre Renfe Viajeros y la persona que viaja, para la presta-
ción de uno o más servicios de transporte, y que faculta al viajero para hacer uso del
servicio”,
a) El cliente tiene la obligación de conservar el título de transporte desde la en-
trada en la estación hasta que acceda al vehículo y tome asiento.
“El cliente debe disponer de un título de transporte valido durante todo el viaje, que
deberá conservar desde la entrada a la estación de origen hasta la salida de la esta-
ción de destino”.
Cc) El sexo del cliente.
“El título de transporte de los servicios con asignación de plaza deberá incluir la si-
guiente información:
- La determinación de la empresa ferroviaria que realiza el transporte.
-  Elorigen del viaje y la hora de salida.
— El destino del viaje y la hora de llegada.
= Identificar número de tren.
= Los transbordos que pudieran producirse con cambio de tren, especificando lu-
gar y hora, en su caso.
= El coche, la clase o tipo de asiento y el número de plaza.
- El peso y volumen del equipaje admitido, o la indicación de dónde se puede
consultar dicha información.
- El previo total del transporte, incluidos los complementos adicionales del trans-
porte, los gastos de gestión si los hubiere, así como la forma de pago.
- El precio de facturación, en su caso, del equipaje.
= La información sobre los seguros u otros afianzamientos Mercantiles que el ser-
vicio tenga cubiertos.
= La hora límite, si la hubiere, de presentación en los controles de seguridad para el
acceso al tren, si el administrador de infraestructuras lo estableciera.
= Indicación de que el transporte queda sometido a las Reglas Uniformes relativas al
contrato de transporte internacional de viajeros y equipajes de ferrocarril (CIV)”:
c) En servicios comerciales y servicios sujetos a obligaciones de servicio público
“Desde el punto de vista tarifario. Renfe Viajeros estructura el servicio que ofrece a
los viajeros en: servicios comerciales y servicios sujetos a obligaciones de servicio
público”.
8. Cc) Acuerdo del Consejo de Ministros.
“Los precios ofertados para los viajes en los trenes de Servicios Comerciales depen-
derán de: tren-fecha, origen-destino, del canal de venta, de las condiciones comer-
ciales que seleccione el cliente, así como de los tributos que legalmente existan en
cada momento”.
9. b) Las estructuras de los sistemas tarifarios, de los cuales derivan los precios
autorizados de los servicios de Media Distancia, son únicas y se aplican en cada
oferta de servicio.
“Las estructuras de los sistemas tarifarios, de los cuales derivan los precios autori-
zados de los servicios de Media Distancia, son únicas y se aplican en cada oferta de
servicio”.
10. d) Títulos de transporte sencillo, colectivo, combinado y multiviaje.
“Renfe viajeros pone a disposición de los clientes las siguientes modalidades de títu-
los de transporte: sencillo, colectivo, combinado y multiviaje”.
11. a) Título de transporte sencillo.
“Títulos de transporte SENCILLO:
Son aquellos cuya adquisición da derecho a viajar a una sola persona en un único
trayecto y fecha, en tren o encaminamiento complementario”.
12. d) Título de transporte colectivo.
“Títulos de transporte COLECTIVO:
Son aquellos cuya adquisición da derecho a viajar a más de una persona en un mismo
trayecto y fecha con único título, en tren o, en su caso, encaminamiento complemen-
tario. Estos títulos de transporte son pluripersonales”.
13. d) Título de transporte combinado.
“Títulos de transporte COMBINADO:
Son aquellos que formalizan distintos contratos de transporte y que dan derecho
a viajar en diferentes modos de transporte, incluyendo, en su caso, otros servicios
asociados, en un único título”,
14. a) Título de transporte multiviaje.
“Títulos de transporte MULTIVIAJE:
Son aquellos que permite realizar distintos viajes, bien limitados a un número o ilimi-
tados, durante su periodo de validez”.
15. d) Todas las anteriores son correctas.
“Las formas de pago admitidas por Rende Viaje son:
a) Metálico en moneda de curso legal en España.
b) Tarjetas de crédito / débito aceptadas por Renfe Viajeros.
c) Puntos de las tarjetas del programa de fidelización de Rende Viajeros.
d) Cualquiera otra regulada al efecto”
16. c) Los gastos de gestión no podrán superar el 10 % del importe del título de
transporte.
“La venta de títulos de transporte para los servicios comerciales puede conllevar gas-
tos de gestión, que se calculan como un porcentaje sobre el precio del transporte o
un importe fijo”.
17. b) Los billetes nominativos son válidos para cualquier cliente que sea portador
del mismo.
*5.1.- Los títulos de transporte solamente son válidos desde su adquisición y hasta la
finalización del viaje (o viajes, en el caso de títulos combinados o multiviajes). En al-
gunos servicios serán válidos durante un plazo determinado, para las fechas, trenes,
trayectos, zonas y tipos de asientos o clases figurados en los mismos. Los viajeros
deberán conservar el título de transporte hasta la finalización de los servicios contra-
tados. En caso de billetes nominativos únicamente son válidos para su titular.
Se deberá portar durante el viaje el título de transporte, en un soporte autorizado por
Renfe Viajeros, formalizado o validado en su caso, con los documentos originales en
vigor que acrediten la identidad del viajero, cuando sea necesario, y las credenciales
justificativas para la obtención de los descuentos a los que tenga derecho”
18. a) Desde su adquisición y hasta la finalización del viaje (o viajes, en el caso de
títulos combinados o multiviajes).
“5.1.- Los títulos de transporte solamente son válidos desde su adquisición y hasta la
finalización del viaje (o viajes, en el caso de títulos combinados o multiviajes). En al-
gunos servicios serán válidos durante un plazo determinado, para las fechas, trenes,
trayectos, zonas y tipos de asientos o clases figurados en los mismos. Los viajeros
deberán conservar el título de transporte hasta la finalización de los servicios contra-
tados. En caso de billetes nominativos únicamente son válidos para su titular.
Se deberá portar durante el viaje el título de transporte, en un soporte autorizado por
Renfe Viajeros, formalizado o validado en su Caso, con los documentos originales en
vigor que acrediten la identidad del viajero, cuando sea necesario, y las credenciales
justificativas para la obtención de los descuentos a los que tenga derecho”
19. d) Todas las anteriores son correctas.
"Se deberá portar durante el viaje el título de transporte, en un soporte autori-
zado por Renfe Viajeros, formalizado o validado en su caso, con los documentos
originales en vigor que acrediten la identidad del viajero, cuando sea necesario, y
las credenciales justificativas para la obtención de los descuentos a los que tenga
derecho”.
20. d) Será válido para su fecha o periodo de utilización, sin que el viajero deba
abonar, o le sea abonada, diferencia alguna.
“Cualquier título de transporte adquirido antes de una revisión de precios al alza o
a la baja, será válido para su fecha o periodo de utilización, sin que el viajero deba
abonar, o le sea abonada, diferencia alguna”."""

if __name__ == "__main__":
    main()