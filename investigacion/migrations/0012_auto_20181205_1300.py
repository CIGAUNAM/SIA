# Generated by Django 2.0.6 on 2018-12-05 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0011_auto_20181205_1300'),
        ('investigacion', '0011_remove_proyectoinvestigacion_institucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='institucion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Institucion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articulocientifico',
            name='status',
            field=models.CharField(choices=[('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado')], max_length=20),
        ),
    ]
