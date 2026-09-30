# Preguntas para precisar necesidades

Estado: abiertas. No asumir respuestas por la forma actual de los Excel.

Contexto resuelto: el repositorio es la propuesta del nuevo SIA del usuario, construida con información inicialmente parcial. No se dispone del código del sistema anterior. No volver a tratar esta distinción como una pregunta pendiente ni asumir que la propuesta ya está en producción.

Ya se confirmó que las secciones, selección de información, agrupaciones y agregaciones deben administrarse dentro de Django. No hace falta volver a preguntar si se desea un constructor de reportes; ver la [especificación funcional](especificaciones/reportes-administrables.md).

## Primera conversación

1. **Salidas prioritarias.** ¿El objetivo inicial es reconstruir los anexos 1–3 y las bases para gráficas, o generar también todo el informe de dirección, incluidas unidades, laboratorios y administración?
2. **Fuente de autoridad.** Si una cifra o categoría difiere entre SIA, CISIC, Excel, anexo y gráfica final, ¿cuál manda y quién valida la diferencia? ¿Qué versión del Anexo 1 usamos como referencia?
3. **Periodos y destinatarios.** El usuario indica reporte trimestral, anual CIC y anual de dirección, inicialmente entendido como año natural. ¿A quién se entrega el trimestral y cómo se llama su formato o plataforma? ¿El anual de dirección por año natural es una nueva regla o se refiere a Memoria UNAM? El informe público 2024–2025 explicita cortes diferentes por anexo. ¿Debemos conservarlos para reproducir el pasado y unificarlos hacia adelante?
4. **Población.** ¿Quiénes cuentan como personal institucional en cada salida: investigadores, técnicos, posdoctorantes, IxM/cátedras, estudiantes, jubilados y bajas? ¿Basta estar adscrito durante parte del periodo o se toma una fecha de corte?
5. **Documentación.** En «adr y se y docs», ¿«se» significa especificaciones u otro tipo de documento? No se creó esa categoría todavía.

## Conteo y relaciones

6. Si dos académicos imparten un curso, ¿se reporta un curso y dos participaciones? ¿Cómo se atribuyen las horas y asistentes?
7. ¿Un producto coescrito por varias personas cuenta una sola vez para la entidad y una vez para cada participante? ¿Puede pertenecer simultáneamente a grupos de investigadores y posdoctorantes?
8. En tesis, ¿qué salidas incluyen codirección, tutoría y sinodalía? ¿Se cuenta la defensa, el grado obtenido o el término administrativo?
9. ¿Los proyectos se cuentan por vigencia, inicio o conclusión? ¿Se necesitan varios financiadores y convocatorias para un proyecto?
10. ¿Se debe registrar una actividad institucional sin atribuirla artificialmente a una cuenta individual? ¿Qué unidades necesitan reportar así?

## Catálogos y cobertura

11. ¿Reseñas y todos los tipos de «otras publicaciones» del Anexo 1 deben recuperarse y mantenerse en el nuevo SIA?
12. ¿Cómo se determina nacional/internacional en libros y artículos: editorial, revista, país, colaboración u otra regla? ¿Es diferente del ámbito de un evento?
13. ¿WoS/Scopus y otros índices son grupos excluyentes? ¿La clasificación corresponde al momento de publicación o al corte del informe?
14. ¿Prioridad estratégica, problema nacional e impacto social son catálogos distintos? ¿Quién los mantiene y qué versiones hay que conservar?
15. ¿Qué categorías de cursos son permanentes y cuáles solo agrupaciones del informe? ¿Educación continua/MIP/programa institucional deben distinguirse del tipo taller/diplomado y de la modalidad presencial/en línea?
16. ¿Qué instituciones y programas se consideran equivalentes? ¿Un mismo programa puede pertenecer a varias instituciones?
17. ¿Qué distingue desarrollo tecnológico, publicación técnica e informe técnico para evitar registrar o contar dos veces un mismo producto?

## Historia, operación y aceptación

18. ¿Reproducir un informe previo significa obtener exactamente lo aprobado en su momento o recalcularlo con datos corregidos? ¿Deben coexistir ambas versiones?
19. ¿Hay fuentes históricas confiables para vigencias de categoría, PRIDE, SNII y adscripción, más allá de los cortes de Excel?
20. ¿Qué captura resulta hoy difícil o repetitiva para académicos y administradores? ¿Cuáles son los tres catálogos que más limpieza requieren?
21. ¿Qué cambios ya está implementando Claude y qué decisiones ya se acordaron? La revisión local no permite conocer compromisos de su conversación.
22. ¿Qué exportaciones necesita el equipo: bases tabulares, anexos Word, gráficas, carga para CISIC u otras? ¿Qué ejemplos concretos consideraríamos una implementación aceptable?

## Temas candidatos a ADR

No están decididos ni numerados como decisiones aceptadas:

- Periodos de reporte y reglas temporales por salida.
- Constructor administrable, fuentes disponibles, composición de indicadores y versiones de definición.
- Identidad de actividades y atribución de participaciones.
- Trayectoria académica y población histórica independiente de la cuenta de acceso.
- Taxonomías de salida y equivalencias con catálogos de captura.
- Cobertura de publicaciones y recuperación de reseñas.
- Reproducibilidad de ediciones del informe y procedencia de los datos.

Las listas de columnas, correcciones de etiquetas y requisitos de interfaz pueden documentarse como especificaciones sin convertir cada ajuste en un ADR.
