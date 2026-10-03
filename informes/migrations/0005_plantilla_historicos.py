"""La plantilla base muestra la historia completa: evolución de la planta (2007 en adelante), PRIDE y SNII desde
2020-2021 (los años sin datos por persona salen de las cifras históricas)."""

from django.db import migrations


def actualizar(apps, schema_editor):
    Informe = apps.get_model('informes', 'Informe')
    Grafica = apps.get_model('informes', 'Grafica')
    plantilla = Informe.objects.filter(nombre='Informe anual (plantilla)', es_plantilla=True).first()
    if plantilla is None:
        return
    plantilla.graficas.filter(indicador__in=['pride', 'snii']).update(periodos=6)
    if not plantilla.graficas.filter(indicador='evolucion_planta').exists():
        Grafica.objects.create(informe=plantilla, orden=0, seccion='Eje 2 · Personal académico',
                               indicador='evolucion_planta', tipo='columnas', periodos=20,
                               titulo='Evolución de la planta académica del {entidad}',
                               subtitulo='Investigador@s, técnic@s y cátedras/IxM por año',
                               colores='#7A8B3A, #4A7C8C, #C4A85A')


class Migration(migrations.Migration):
    dependencies = [('informes', '0004_cifras_historicas')]
    operations = [migrations.RunPython(actualizar, migrations.RunPython.noop)]
