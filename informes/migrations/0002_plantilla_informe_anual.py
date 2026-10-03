"""Plantilla base: las gráficas del informe anual 2025-2026, de donde parten los informes nuevos."""

from django.db import migrations

OLIVA, PETROLEO, TERRACOTA, OCRE, GRIS = '#7A8B3A', '#4A7C8C', '#B87333', '#C4A85A', '#949A90'

GRAFICAS = [
    # (sección, indicador, tipo, título, subtítulo, periodos, colores)
    ('Eje 2 · Personal académico', 'planta', 'columnas', 'Distribución de la planta académica',
     'Por categoría, nivel y género · {anio}', 1, ''),
    ('Eje 2 · Personal académico', 'antiguedad', 'rango', 'Antigüedad del personal académico del {entidad} en {anio}',
     'Amplitud (mín–máx) y promedio de años, por categoría y nivel', 1, ''),
    ('Eje 2 · Personal académico', 'contratos', 'columnas', 'Personal académico por tipo de contrato',
     'Investigador@s y técnic@s · {anio}', 1, f'{OCRE}, {OLIVA}, {PETROLEO}, {TERRACOTA}'),
    ('Eje 2 · Personal académico', 'pride', 'columnas', 'Distribución de la planta académica por nivel del PRIDE',
     'Por periodo', 4, f'{OCRE}, {PETROLEO}, {OLIVA}'),
    ('Eje 2 · Personal académico', 'snii', 'columnas', 'Distribución del personal académico por nivel del SNII',
     'Por periodo', 4, f'{OCRE}, {PETROLEO}, {OLIVA}, {TERRACOTA}'),
    ('Eje 2 · Investigación', 'proyectos_financiamiento', 'pastillas', 'Número de proyectos e instancias financiadoras',
     'Por periodo', 3, f'{PETROLEO}, {OCRE}, {OLIVA}'),
    ('Eje 2 · Investigación', 'tipos_proyectos', 'anillos', 'Tipos de proyectos que se desarrollaron en el {entidad}',
     'Entre {inicio} y {fin}: modalidad, alcance y temática de género', 1, ''),
    ('Eje 2 · Investigación', 'ods', 'rosa', 'Proyectos por Objetivo de Desarrollo Sostenible',
     'Un proyecto puede atender varios objetivos', 1, ''),
    ('Eje 2 · Investigación', 'prioridades', 'barras', 'Problemas Nacionales Prioritarios (SECIHTI)',
     'Número de proyectos que abordan cada problema nacional', 1, ''),
    ('Eje 2 · Producción', 'publicaciones', 'columnas', 'Productos publicados por personal del {entidad}',
     'Por tipo de publicación y origen · julio {inicio} – junio {fin}', 1, f'{PETROLEO}, {TERRACOTA}'),
    ('Eje 2 · Producción', 'cuartiles', 'anillos', 'Factor de impacto y cuartil de calidad de las revistas',
     'Núcleo: cuartil SCImago · anillo externo: rango de factor de impacto', 1,
     f'{OLIVA}, {PETROLEO}, {OCRE}, {TERRACOTA}, {GRIS}'),
    ('Eje 2 · Vinculación académica', 'vinculacion', 'semicirculo', 'Acciones de vinculación académica',
     'Julio {inicio} – junio {fin}', 1,
     f'{TERRACOTA}, {OCRE}, #A5B07A, #3F6672, #C08A4A, {GRIS}, {OLIVA}, #4F7F94, #6E8A3A'),
    ('Eje 3 · Docencia', 'cursos_posgrado', 'columnas',
     'Cursos por programa, categoría académica y nivel de participación', 'Participaciones de cada académico', 1,
     f'{OLIVA}, {PETROLEO}'),
    ('Eje 3 · Docencia', 'tesis', 'barras', 'Tesis defendidas y en proceso de dirección',
     'Personal del {entidad} · julio {inicio} – junio {fin}, por grado académico e institución vinculada', 1,
     f'{OLIVA}, {TERRACOTA}'),
]


def crear(apps, schema_editor):
    Informe = apps.get_model('informes', 'Informe')
    Grafica = apps.get_model('informes', 'Grafica')
    plantilla = Informe.objects.create(
        nombre='Informe anual (plantilla)', periodo='2025-2026', es_plantilla=True,
        descripcion='Las gráficas del informe anual 2025-2026. Créale un informe nuevo para cada año con '
                    '«Nuevo informe a partir de este».')
    for orden, (seccion, indicador, tipo, titulo, subtitulo, periodos, colores) in enumerate(GRAFICAS, start=1):
        Grafica.objects.create(informe=plantilla, orden=orden, seccion=seccion, indicador=indicador, tipo=tipo,
                               titulo=titulo, subtitulo=subtitulo, periodos=periodos, colores=colores)


def quitar(apps, schema_editor):
    apps.get_model('informes', 'Informe').objects.filter(nombre='Informe anual (plantilla)', es_plantilla=True).delete()


class Migration(migrations.Migration):
    dependencies = [('informes', '0001_initial')]
    operations = [migrations.RunPython(crear, quitar)]
