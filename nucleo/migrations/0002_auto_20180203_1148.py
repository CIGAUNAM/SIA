# Generated by Django 2.0.2 on 2018-02-03 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='tipo_cargo',
            field=models.CharField(choices=[('', '-------'), ('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), ('DIRECTIVO', 'Directivo'), ('OTRO', 'Otro')], max_length=20),
        ),
    ]
