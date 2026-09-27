from django.db import migrations, models


def celular_a_telefono(apps, schema_editor):
    User = apps.get_model('nucleo', 'User')
    User.objects.filter(telefono='').exclude(celular='').update(telefono=models.F('celular'))


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0006_correo_como_usuario'),
    ]

    operations = [
        migrations.RenameField(model_name='user', old_name='direccion', new_name='domicilio'),
        migrations.AlterField(
            model_name='user',
            name='domicilio',
            field=models.TextField(blank=True, help_text='Domicilio donde realiza sus actividades académicas.'),
        ),
        migrations.RunPython(celular_a_telefono, migrations.RunPython.noop),
        migrations.RemoveField(model_name='user', name='celular'),
    ]
