# Generated by Django 2.0.1 on 2018-01-10 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distinciones', '0002_auto_20180107_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='participacionsociedadcientifica',
            name='ambito',
            field=models.CharField(choices=[('', '-------'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
