from django.db import migrations


def renombrar(apps, schema_editor, anterior, nuevo):
    Group = apps.get_model('auth', 'Group')
    if not Group.objects.filter(name=nuevo).exists():
        Group.objects.filter(name=anterior).update(name=nuevo)


class Migration(migrations.Migration):
    """El grupo "Investigadores" pasa a llamarse "Académicos" (incluye técnicos y posdoctorantes)."""

    dependencies = [
        ('nucleo', '0009_persona_nombre_para_mostrar'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(lambda apps, se: renombrar(apps, se, 'Investigadores', 'Académicos'),
                             lambda apps, se: renombrar(apps, se, 'Académicos', 'Investigadores')),
    ]
