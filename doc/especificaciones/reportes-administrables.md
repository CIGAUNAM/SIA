# Reportes administrables desde Django

Fecha: 29 de septiembre de 2026. Estado: requisito confirmado y propuesta funcional para discusión. Sin implementación ni ADR aceptado.

## Objetivo confirmado por el usuario

El SIA debe permitir administrar dentro de Django los reportes, sus secciones, la información que toman y sus agrupaciones y agregaciones. La configuración debe apoyarse en el contenido de informes institucionales públicos y en los materiales previos compartidos.

Esto amplía el objetivo inicial: además de ajustar catálogos, se necesita una capacidad de composición de reportes reutilizable. Trimestral, anual CIC y anual de dirección son necesidades comunicadas; sus definiciones exactas siguen en validación.

## Base documental

La [Memoria UNAM 2024 del CIGA](https://www.planeacion.unam.mx/Memoria/2024/PDF/7.30-CIGA.pdf) combina personal al cierre, producción durante el año, proyectos, convenios, eventos, docencia y divulgación. Incluye totales, desgloses, promedios y narrativas. Es evidencia de que no basta un listado con un filtro anual.

El [informe de dirección 2024–2025](https://www.ciga.unam.mx/images/CIGA/informes/Segundo-Informe-CIGA-2024-2025.pdf) organiza resultados por ejes y anexos, con cortes distintos. Se propone reproducir esa flexibilidad sin convertir sus cortes históricos en una obligación permanente.

Los anexos locales aportan el detalle de campos y categorías. La investigación y sus límites están en [Reportes públicos](../reportes-publicos.md). No se inventará una plantilla oficial trimestral o CIC a partir de documentos de otras entidades.

## Qué debe poder administrar una persona autorizada

| Elemento | Configuración requerida |
| --- | --- |
| Tipo de reporte | Nombre, finalidad, destinatario, periodicidad, responsables y formato de salida |
| Estructura | Secciones y subsecciones, títulos, orden, visibilidad, introducciones y notas |
| Bloque de contenido | Indicador, tabla de detalle, tabla agregada, serie temporal, gráfica o texto narrativo |
| Fuente de información | Conjunto de datos disponible, unidad de registro y campos utilizables |
| Selección | Filtros combinables, población, roles de participantes, estados y exclusiones |
| Regla temporal | Fecha del hecho, rango, corte de vigencia, acumulado y excepciones explícitas por bloque |
| Columnas | Campos, etiquetas, orden, formato, unidades y tratamiento de faltantes |
| Agrupación | Una o varias dimensiones, jerarquías, categorías de salida y equivalencias |
| Agregación | Conteos, conteos únicos, sumas, mínimos, máximos, promedios, proporciones y razones entre indicadores |
| Presentación | Subtotales, total general, orden de categorías, precisión y visualización |
| Comparación | Ediciones anteriores, periodos equivalentes y reglas compatibles |
| Narrativa y aportes | Textos de contexto y datos externos identificados con su procedencia |

Los formatos finales exactos —Excel, Word, PDF, gráficas o envío a sistemas externos— siguen pendientes de priorización. El diseño de los datos debe permitir varias presentaciones de una misma definición.

## Flujo funcional propuesto

1. Crear un tipo de reporte o copiar uno existente.
2. Agregar secciones y bloques; seleccionar fuentes con nombres comprensibles, como Publicaciones, Tesis o Eventos.
3. Elegir qué se cuenta: productos, personas, participaciones, horas u otra medida disponible.
4. Configurar filtros, fechas, dimensiones y cálculos con controles de formulario.
5. Ver una previsualización con resultados, faltantes y registros que explican cada cifra.
6. Revisar y publicar una versión de la definición.
7. Crear una edición para un periodo concreto, incorporar comentarios o aportes y validarla.
8. Cerrar la edición, conservando lo que se entregó y la configuración utilizada.

Los pasos 6–8 son una propuesta para asegurar reproducibilidad. Se debe acordar quién valida y si se requiere aprobación formal. No confundir este flujo con pedir permiso al usuario para continuar documentando.

## Entidades conceptuales propuestas

Estos nombres describen responsabilidades, no son instrucciones de crear exactamente estas tablas.

| Concepto | Responsabilidad y relaciones |
| --- | --- |
| Definición de reporte | Identidad reutilizable del reporte y sus versiones |
| Versión de definición | Configuración de estructura y reglas; una versión publicada conserva su significado |
| Sección | Pertenece a una versión; puede tener subsecciones y bloques ordenados |
| Bloque | Presenta datos de un conjunto o indicadores, o contenido narrativo |
| Fuente disponible | Declara qué representa una fila, identificador, campos, relaciones y medidas compatibles |
| Conjunto de datos configurado | Selecciona una fuente, población, filtros y reglas temporales; reutilizable entre bloques |
| Indicador | Define cálculo, unidad, clave de conteo, agrupaciones y, cuando aplique, numerador y denominador |
| Clasificación de salida | Mapea categorías de captura a categorías de un reporte sin renombrar los datos originales |
| Edición de reporte | Instancia de una versión para fechas y destinatario concretos; varias ediciones pueden compartir el año |
| Ejecución | Resultado calculado en una fecha, con versión, parámetros, procedencia y observaciones |
| Aporte editorial o externo | Texto, dato o corrección explícita ligado a edición/bloque, con fuente y responsable |

Una gráfica y una tabla deben poder reutilizar el mismo indicador. No deben recalcularlo con reglas independientes por accidente. Las dependencias entre indicadores deben detectarse y no permitir ciclos.

## Semántica de cálculo que debe quedar explícita

### Unidad e identidad

Cada fuente debe declarar si una fila representa una publicación, una persona, una participación o una oferta de curso. El usuario configura el conteo sobre esa identidad. Al combinar autores, índices y proyectos no se deben multiplicar silenciosamente los productos ni sus importes.

Un total institucional cuenta productos únicos cuando esa sea su definición. La suma de participaciones individuales es otra medida. Para sumas, la deduplicación se realiza por identidad del hecho, nunca por igualdad de su valor numérico: dos cursos diferentes de diez horas suman veinte.

### Tiempo

Configurar separadamente:

- Hechos ocurridos durante un intervalo, como publicaciones o exámenes.
- Registros cuya vigencia se solapa con el periodo, como proyectos.
- Situación en una fecha de corte, como plantilla o tesis en proceso.
- Flujo del trimestre frente a acumulado desde el inicio del año.

Las fechas inicial/final deben tener una convención inequívoca. Para fechas incompletas, vigencias abiertas y registros sin fecha debe elegirse una política visible. El estado actual de una tesis no permite reconstruir por sí solo su estado histórico: la configuración no sustituye datos temporales faltantes.

### Agrupaciones y población

La clasificación debe poder ser exclusiva, con prioridad de reglas, o permitir varias pertenencias. Si un proyecto tiene varios ODS, el total de proyectos se calcula sobre identidades únicas, no sumando los grupos.

Las equivalencias pueden ser diferentes por reporte o versión. Un programa académico puede agruparse como posgrado sin perder su nivel de maestría o doctorado en la captura. Un valor sin correspondencia aparece como pendiente de clasificar; no se transforma automáticamente en cero u Otro.

La adscripción, categoría o nivel que decide la población debe corresponder a la fecha o regla acordada, no al estado actual de acceso de una cuenta.

### Promedios y razones

Separar promedio de participaciones por persona de productos institucionales únicos divididos entre personal elegible. Permitir denominadores provenientes de otro conjunto compatible, indicar si incluye personas con cero producción y definir qué ocurre con un denominador cero. No promediar porcentajes de grupos sin considerar sus tamaños.

### Reproducibilidad

Una edición cerrada debe identificar la definición y datos utilizados. Propuesta: conservar resultados entregados y su detalle de procedencia; una corrección posterior produce una revisión identificable. Antes de decidir el mecanismo técnico hay que acordar si se necesita recalcular exactamente desde datos históricos o basta consultar la edición preservada.

## Alcance de la administración

El requisito es que cambios de secciones, filtros, categorías de salida, agrupaciones y cálculos soportados no requieran editar código. Se propone un constructor con operadores y relaciones declarados, no campos para introducir SQL o Python.

Las fuentes disponibles necesitan exponer información con significado estable. Incorporar una fuente enteramente nueva, un campo que aún no se captura o una operación no soportada puede requerir implementación. Esto debe mostrarse como una necesidad pendiente, no resolverse permitiendo acceso indiscriminado a cualquier modelo, contraseña, dato personal o relación interna de Django.

Para métricas de unidades o laboratorios que no proceden de registros académicos, se propone permitir indicadores de captura manual con tipo, unidad, periodo, fuente y evidencia. Deben aparecer como aportes externos/manuales y no sustituir silenciosamente un cálculo automático.

La previsualización, el detalle y las exportaciones deben aplicar los permisos correspondientes. La configuración es institucional; queda pendiente si también habrá reportes personales configurables y quién puede publicar definiciones compartidas.

## Ejemplos de configuración por validar

Son ejemplos derivados de las necesidades observadas, no transcripciones de reglas oficiales ni resultados conciliados.

| Bloque | Fuente y selección | Agrupación | Operación |
| --- | --- | --- | --- |
| Producción publicada | Publicaciones elegibles cuya fecha de publicación cae en el periodo | Tipo e indización según equivalencias aprobadas | Número de productos únicos |
| Proyectos vigentes | Proyectos cuya vigencia se solapa con el periodo | Programa financiador o modalidad | Proyectos únicos; detalle por papel de participación por separado |
| Planta al corte | Trayectoria académica vigente en la fecha de corte | Tipo, categoría, PRIDE o SNII | Personas únicas |
| Tesis defendidas | Tesis con examen dentro del intervalo | Nivel e institución | Tesis únicas; atribuciones por rol como vista distinta |
| Tesis en proceso | Situación histórica al corte | Nivel y programa | Tesis únicas, sin sumar inventarios de trimestres |
| Organización de eventos | Eventos elegibles del periodo | Tipo, ámbito o unidad organizadora | Eventos únicos; asistentes del evento sin repetirlos por organizador |
| Docencia | Ofertas de curso y participaciones docentes | Nivel, programa y clase de curso | Cursos únicos y horas docentes como medidas separadas |
| Avances de una unidad | Aportes de la unidad para la edición | Línea de actividad | Narrativa y métricas tipadas con evidencia |

## Casos de aceptación propuestos para Claude

1. Desde la administración se crea una sección, se cambia su orden y se agrega un desglose sin modificar código.
2. Un artículo con tres autores y dos índices suma uno en productos únicos; sus participaciones pueden sumar tres. El grupo de indización se determina por la regla configurada.
3. Dos cursos de diez horas suman veinte. Añadir dos participantes a uno no duplica sus horas totales; las horas personales se calculan desde su medida específica.
4. Un proyecto asociado a tres ODS aparece en tres grupos y conserva un total general de uno.
5. Una tesis vigente durante cuatro trimestres no se convierte en cuatro tesis anuales. Una tesis defendida después del corte puede aparecer en proceso en una edición anterior si existe la información histórica necesaria.
6. Una cuenta desactivada conserva la producción histórica elegible de la persona y no obtiene acceso por aparecer en un reporte.
7. Trimestral, anual CIC y dirección pueden coexistir para el mismo año con estructuras y periodos distintos.
8. La edición cerrada conserva sus resultados cuando cambia la clasificación para la siguiente edición. Las correcciones se identifican como revisión.
9. Toda cifra permite consultar registros y reglas que la producen. Cuando falta una fuente o dimensión necesaria, se informa expresamente y no se muestra un cero aparente.
10. Numerador, denominador, valores faltantes y redondeo son verificables; el resultado de una proporción coincide con sus componentes.
11. Un filtro inválido, una relación que multiplicaría filas o una dependencia circular se detectan antes de publicar la definición.
12. Usuarios sin permisos no pueden obtener campos o registros restringidos mediante filtros, previsualizaciones o exportaciones.

Estos casos son especificaciones para implementación futura; no se crearon ni ejecutaron pruebas en esta revisión.

## Relación con la propuesta del nuevo SIA

El código disponible es la propuesta del usuario, no el SIA anterior. Las decisiones siguientes pueden reconsiderar esa propuesta sin asumir compatibilidad con una implementación anterior que no se ha revisado. La conservación de información histórica es un problema distinto de conservar estructuras de código.

`PeriodoInforme.anio` es único, lo que no representa por sí solo varios tipos y ediciones del mismo año. Las reglas del tablero están en una lista de Python y la exportación institucional reutiliza el CV. Esos son puntos de integración a revisar; no se propone sustituirlos ahora ni duplicar toda la captura.

Los cierres de captura y la publicación de una edición son decisiones relacionadas pero diferentes. Cerrar un reporte no debería bloquear accidentalmente otro reporte que usa los mismos registros. El ADR deberá precisar ese comportamiento y cómo ajustar los cierres incluidos en la propuesta. No se presupone que existan cierres operativos que deban migrarse.

## Pendientes antes del ADR

- Identificar formato/destinatario del trimestral y entrega exacta de CIC.
- Acordar formatos de exportación prioritarios y facultades de quienes configuran, validan y consultan.
- Definir política futura de periodos y compatibilidad con ediciones anteriores.
- Elegir una primera sección completa para validar el constructor, incluyendo detalle, total y caso de duplicación.
- Acordar si los indicadores manuales y narrativas de unidades entran en la primera implementación.

No se asume que «se» del mensaje inicial significaba especificación. Esta especificación funcional se incorpora por el nuevo requisito explícito del constructor de reportes.
