# Alineación del SIA con informes institucionales previos

Esta carpeta reúne el diagnóstico, las preguntas de negocio y las futuras decisiones para que Claude implemente los cambios acordados. La revisión inicial es del 29 de septiembre de 2026, sobre la referencia Git `eabb1ba`.

## Contexto confirmado del proyecto

El repositorio revisado es la **propuesta del nuevo SIA desarrollada por el usuario**, que continúa trabajando con Claude. No es el código del SIA anterior. Ese sistema es independiente y su código no está disponible para esta revisión.

La propuesta se construyó con información parcial. Los informes y bases ahora disponibles permiten completar las necesidades y mejorar su diseño. Las referencias al «código actual» en estos documentos describen exclusivamente esta propuesta; no demuestran cómo funciona el sistema anterior.

Los datos legacy y el convertidor presentes en el repositorio son insumos para estudiar la recuperación de información. No convierten al repositorio en el sistema anterior ni obligan a conservar su estructura. El alcance de la importación histórica se debe acordar por separado del diseño del nuevo sistema.

La revisión busca definir qué necesita el nuevo SIA, aprovechar lo útil de la propuesta y reconsiderar sus decisiones con evidencia adicional. No se presupone que esté desplegada en producción ni que su comportamiento actual constituya un requisito institucional.

El usuario aclaró que los materiales son **informes previos de referencia**, no exclusivamente el informe 2025. Sus años y fechas deben conservarse al comparar resultados, pero no limitan el alcance a una sola edición.

## Documentos

- [Diagnóstico inicial](diagnostico-inicial.md): comprensión del sistema, brechas y oportunidades.
- [Matriz de salidas](matriz-de-salidas.md): correspondencia entre informes, modelos y preguntas.
- [Preguntas pendientes](preguntas-pendientes.md): decisiones de negocio que necesitamos conversar.
- [Inventario de fuentes](inventario-de-fuentes.md): cobertura y límites de la barrida.
- [Reportes públicos](reportes-publicos.md): búsqueda oficial y distinción entre dirección, CIC/CISIC, Memoria UNAM y reporte trimestral.
- [Reportes administrables](especificaciones/reportes-administrables.md): requisito confirmado, propuesta de configuración en Django y casos de aceptación para Claude.
- [Plantilla de ADR](adr/plantilla.md): formato para registrar decisiones después de discutirlas.

## Estado y forma de trabajo

**Diagnóstico preliminar; no hay ADR aceptados ni una especificación de implementación aprobada.** Los hallazgos describen lo observado. Las propuestas son hipótesis de trabajo y no autorizan eliminar modelos, campos o información histórica.

**Requisito confirmado después del diagnóstico:** el usuario quiere administrar en Django los reportes, secciones, información seleccionada, agrupaciones y agregaciones. La especificación funcional distingue ese objetivo de las decisiones técnicas aún abiertas.

La secuencia propuesta es elegir las salidas prioritarias, acordar su significado y reglas de conteo, documentar necesidades, resolver alternativas en ADR y después preparar tareas para Claude con ejemplos verificables y tratamiento de datos históricos.

Los archivos originales de informes y los datos personales permanecen en sus ubicaciones originales. Esta carpeta no contiene copias de bases ni credenciales. En esta revisión se agregaron únicamente documentos; no se modificaron código, migraciones ni bases de datos.

La expresión «se» del mensaje inicial queda pendiente de aclaración antes de crear una categoría documental con ese nombre.

El usuario añadió tres necesidades potenciales: reporte trimestral, anual CIC y anual de dirección, este último entendido inicialmente como año natural. La existencia del trimestral se conserva como necesidad comunicada; su formato y destinatario siguen pendientes. Los ejemplos públicos de dirección muestran cortes diferentes del año natural. Ver la investigación enlazada antes de fijar reglas.
