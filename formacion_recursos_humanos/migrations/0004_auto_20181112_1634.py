# Generated by Django 2.0.6 on 2018-11-12 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formacion_recursos_humanos', '0003_auto_20180803_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asesoriaestudiante',
            name='institucion',
        ),
        migrations.RemoveField(
            model_name='comitecandidaturadoctoral',
            name='institucion',
        ),
        migrations.RemoveField(
            model_name='comitetutoral',
            name='institucion',
        ),
        migrations.RemoveField(
            model_name='direcciontesis',
            name='institucion',
        ),
        migrations.RemoveField(
            model_name='supervisioninvestigadorpostdoctoral',
            name='institucion',
        ),
    ]