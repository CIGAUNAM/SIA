# Generated by Django 2.0.2 on 2018-02-09 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('difusion_cientifica', '0007_memoriainextenso_editorial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memoriainextenso',
            old_name='issn',
            new_name='isbn',
        ),
    ]
