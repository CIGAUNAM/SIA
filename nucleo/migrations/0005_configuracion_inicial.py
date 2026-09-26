from django.db import migrations


def crear(apps, schema_editor):
    """Configuración inicial de esta instalación (antes vivía en settings/.env)."""
    ConfiguracionEntidad = apps.get_model('nucleo', 'ConfiguracionEntidad')
    if ConfiguracionEntidad.objects.exists():
        return
    ConfiguracionEntidad.objects.create(
        nombre='Centro de Investigaciones en Geografía Ambiental',
        siglas='CIGA',
        ciudad='Morelia, Michoacán',
        direccion=('Antigua carretera a Pátzcuaro 8701, Col. Ex Hacienda de San José de la Huerta, C.P. 58190, '
                   'Morelia, Michoacán, México'),
        pais_sede=apps.get_model('nucleo', 'Pais').objects.filter(nombre='México').first(),
    )


class Migration(migrations.Migration):
    dependencies = [('nucleo', '0004_configuracion_entidad')]

    operations = [migrations.RunPython(crear, migrations.RunPython.noop)]
