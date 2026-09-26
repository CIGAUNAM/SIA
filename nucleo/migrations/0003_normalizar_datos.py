from django.db import migrations

from nucleo.normalizacion import normalizar


def aplicar(apps, schema_editor):
    sede = apps.get_model('nucleo', 'Pais').objects.filter(nombre='México').values_list('pk', flat=True).first()
    normalizar(apps.get_model, sede)


class Migration(migrations.Migration):
    dependencies = [
        ('nucleo', '0002_confirmacioninforme_evidencia_and_more'),
        ('difusion_cientifica', '0003_alter_participacioneventoacademico_ambito_and_more'),
        ('divulgacion_cientifica', '0003_alter_participacioneventodivulgacion_ambito_and_more'),
        ('investigacion', '0003_alter_articulocientifico_agradecimientos_and_more'),
    ]

    operations = [migrations.RunPython(aplicar, migrations.RunPython.noop)]
