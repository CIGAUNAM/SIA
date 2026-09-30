# Diagnóstico inicial de alineación

Fecha: 29 de septiembre de 2026. Estado: preliminar para discusión.

## Comprensión de la propuesta del nuevo sistema

**Aclaración del usuario:** este repositorio contiene su propuesta del nuevo SIA, elaborada antes de disponer de todos los informes e insumos actuales. El código del SIA anterior no está disponible. Los hallazgos siguientes evalúan la propuesta frente a las necesidades documentadas; no son una auditoría del sistema anterior ni de una instalación en producción.

El SIA registra actividad académica del CIGA con una aplicación Django por dominio. La interfaz utiliza el administrador de Django. `nucleo` concentra personas, cuentas, instituciones, programas, revistas, libros, eventos, evidencias, periodos de informe y utilidades compartidas.

La propuesta ya incluye simplificaciones importantes: una persona puede existir sin cuenta; instituciones y dependencias comparten una jerarquía; eventos y revistas se reutilizan; los programas académicos distinguen nivel; autores y otros participantes usan relaciones explícitas. También existen importación bibliográfica, fusión de duplicados, permisos, confirmación de informes y bitácora de numerosos modelos. Son bases aprovechables, sujetas a revisión con las necesidades recién identificadas.

Los materiales de referencia combinan tres productos diferentes: currículums y participaciones individuales, resultados institucionales únicos y narrativas de unidades, laboratorios y comisiones. Una misma actividad puede alimentar los tres. La estructura de carpetas del código no tiene por qué coincidir con los ejes editoriales del informe.

## Hallazgos prioritarios

### 1. El informe institucional necesita reglas propias

`nucleo/vistas.py` construye Mi informe y el detalle de Excel con `secciones_cv`. La exportación contiene apartado, texto del registro y académicos asociados. El resumen usa nueve indicadores definidos en `SIA/tablero.py`.

Los Excel y anexos de referencia requieren desgloses adicionales: financiamiento, indización, origen de publicaciones, grupos de personal, instituciones, tipos de cursos y entidades organizadoras. El modelo puede contener parte de esa información aunque la exportación no la exponga como columnas.

**Propuesta por discutir:** describir cada salida como un conjunto de datos con columnas y reglas de selección, separado de su presentación en el CV. No hace falta decidir todavía si eso supone una nueva aplicación Django.

### 2. Los periodos y las fechas de conteo no son uniformes

`PeriodoInforme` guarda un año y una fecha límite, sin inicio y fin del periodo reportado. El CV filtra por años; el tablero utiliza una fecha específica por indicador; el cierre usa año de publicación, término de actividad o fecha puntual.

En `Eje2_Proyectos&Publicaciones_GC.xlsx`, hoja `Artículos`, aparecen simultáneamente «Informes CIGA (jul año 1-jun año 2)» e «Informe Anual CIC (enero-dic maso)». Documentos de unidades indican septiembre–agosto. La gráfica de tesis indica agosto 2025–julio 2026. Esto prueba que hay distintas referencias temporales, pero no determina por sí solo cuáles son las reglas oficiales.

Por ejemplo, el tablero cuenta proyectos iniciados en un año; una salida titulada proyectos desarrollados durante un periodo puede necesitar todos los vigentes. Son indicadores distintos, no necesariamente un error del tablero.

**Pendiente:** fechas de corte por salida; inclusión por inicio, conclusión o vigencia; tratamiento de fechas incompletas y actividades que cruzan periodos.

Actualización durante la conversación: se añadieron reportes trimestral y anual CIC, además del de dirección. La [búsqueda pública](reportes-publicos.md) encontró una explicación explícita de los diferentes cortes en el informe de dirección 2024–2025. Por tanto, esta brecha temporal tiene evidencia documental adicional y debe resolverse antes de fijar catálogos exclusivamente para una salida.

### 3. Separar producto único de participación individual

La exportación evita repetir el mismo objeto dentro de un apartado, pero no puede reconocer automáticamente dos objetos diferentes que representan un mismo hecho. `CursoEscolarizado` pertenece a una cuenta y guarda horas; las bases distinguen titular, otros docentes, curso y asistentes. Un curso con varios docentes necesita una definición de identidad y de reparto de horas.

Algo equivalente ocurre con organización de eventos: existe `Evento` compartido, pero las organizaciones se registran por usuario. Debe acordarse cuándo contar eventos y cuándo participaciones. Las tesis ya distinguen director, codirector y tutores, mientras el indicador de tesis concluidas se atribuye al director.

**Pendiente:** total institucional, aportación por académico y denominador de promedios. No deben tratarse como cifras intercambiables.

### 4. La historia académica no equivale a la cuenta actual

La base de planta académica conserva categoría/nivel y PRIDE/SNII por año. En el sistema, tipo de personal, PRIDE y SNII son campos actuales de `User`. Hay experiencia profesional con nombramiento y fechas, pero no una trayectoria temporal equivalente para todos esos atributos. `nucleo/historial.py` excluye `User` del registro automático de historial.

Además, `academicos_del_periodo` exige cuenta activa hoy para construir el detalle del informe, mientras `academicos_activos` del tablero no usa ese filtro. Un académico dado de baja podría aparecer de forma diferente en ambos conjuntos. Es una diferencia de implementación comprobable por lectura; no se evaluó su efecto en la base activa.

**Propuesta por discutir:** distinguir acceso a la plataforma de pertenencia institucional y situación académica en una fecha. Conservar cortes históricos aunque cambie el perfil actual.

### 5. Hay una brecha explícita con las reseñas

El Anexo 1 contiene «G.4 Reseñas» y la base de proyectos/publicaciones tiene una hoja `Reseñas`. El README y `convertir_legacy.py` indican que se omiten reseñas durante la conversión. No se encontró un modelo actual dedicado a ellas.

Esto debe resolverse antes de considerar completa la cobertura de publicaciones. Falta decidir si serán un subtipo de publicación u otra entidad, cómo se contará la obra reseñada y cómo recuperar el legado. No se propone reincorporarlas sin revisar sus registros y equivalencias.

### 6. Financiamiento y prioridades mezclan dimensiones

Los proyectos tienen un conjunto fijo de opciones que combina programas (PAPIIT/PAPIME), una entidad financiadora (etiquetada CONAHCYT), ingresos extraordinarios y ausencia de recursos propios. Las bases usan SECIHTI, institución, programa, clave, clasificación para gráfica, prioridad estratégica e impacto social como datos distintos.

Los ODS ya son una relación múltiple, adecuada para proyectos que contribuyen a varios objetivos. No se identificó un campo específico para prioridad estratégica equivalente a la columna de la base. `impacto_social` es texto libre.

**Propuesta por discutir:** separar conceptos y definir equivalencias históricas, evitando reemplazar etiquetas antiguas sin conservar su significado. Solo crear relaciones de múltiples financiadores si los casos reales lo exigen.

### 7. Bibliometría y origen necesitan definiciones

El Anexo 1 distingue WoS/Scopus, otros índices, no indizados y nacional/internacional. `Revista.indices` no expresa vigencia temporal. `MetricaRevista` sí distingue año y fuente, lo cual ofrece una base útil, pero exige un valor de factor de impacto incluso cuando lo disponible podría ser únicamente el cuartil. El artículo puede conservar un factor propio que prevalece sobre el de revista.

La base contiene columnas distintas para factor WoS y cuartil SCImago. La base de citas indica fuente y fecha de análisis. No se identificó un modelo dedicado a series de citas.

**Pendiente:** fuente y año de cada métrica, categoría temática cuando corresponda, forma de contabilizar múltiples índices, definición de origen nacional/internacional y precedencia de valores históricos. El país de edición no demuestra por sí solo el alcance académico de una publicación.

### 8. La actividad institucional excede el registro personal

El Anexo 2 agrupa divulgación por UCSC, comisiones, otras dependencias y personal académico. Los documentos de laboratorios y unidades contienen servicios, actividad colectiva y resultados narrativos. Hay modelos de comisiones y apoyo institucional, pero no se encontró una estructura específica que cubra de forma uniforme unidades, laboratorios, sus indicadores y cortes.

**Pendiente de alcance:** si el SIA producirá todo el informe o solamente la parte académica. No se justifica construir módulos de servicios, administración o analítica web hasta resolverlo.

### 9. Algunas categorías pueden simplificarse mediante equivalencias

«Vinculación académica» del informe agrupa registros hoy distribuidos entre difusión, vinculación, distinciones, movilidad y compromiso institucional. Esa diferencia editorial no obliga a fusionar sus modelos.

En cursos, el informe distingue educación continua, diplomados, extraordinarios y apoyo al posgrado; el sistema combina tipo, modalidad y una clasificación más limitada. Son dimensiones que deben mapearse antes de eliminar opciones.

Hay un posible solapamiento entre `DesarrolloTecnologico` y ciertos tipos de `PublicacionTecnica`. También conviene precisar los límites de comisiones de expertos, institucionales y de arbitraje. Son candidatos a revisión, no duplicaciones demostradas de registros.

### 10. Los insumos son documentos de trabajo, con decisiones editoriales

Se encontraron hojas llamadas `FALTA ARREGLAR Asesorias extern`, campos «Clase p/Grafica», notas de coherencia, valores «?» y advertencias sobre periodos CISIC. Hay más de una versión del Anexo 1 y documentos repetidos en distintas carpetas.

**Propuesta por discutir:** conservar procedencia, equivalencia aplicada y motivo de exclusión. Una cifra aprobada y una cifra recalculada con reglas nuevas deben poder distinguirse. El cierre actual restringe edición de producción, pero no equivale a guardar una edición inmutable del informe: el Excel se reconstruye al descargarlo y Administración puede modificar registros.

## Orden sugerido para continuar

1. Elegir las salidas prioritarias y la fuente que manda cuando hay diferencias.
2. Acordar población, periodo, unidad de conteo y reglas históricas.
3. Resolver cobertura faltante y equivalencias de catálogos.
4. Redactar ADR para las alternativas que realmente cambien arquitectura o relaciones.
5. Preparar especificaciones pequeñas para Claude, con ejemplos de entrada/salida y conciliación contra informes previos.

Esta revisión fue estática y orientada al dominio. No se inició Django, no se consultó la base activa, no se ejecutaron pruebas ni migraciones y no se conciliaron todas las cifras. No constituye una auditoría exhaustiva de seguridad, rendimiento o calidad de cada registro.
