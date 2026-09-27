"""La cuenta apunta a su persona (User.persona) y la persona tiene un solo nombre en formato de cita.

Antes: Persona.usuario (opcional) y Persona.nombre + Persona.apellidos.
"""

import django.db.models.deletion
from django.db import migrations, models

PARTICULAS = {'de', 'del', 'la', 'las', 'los', 'y', 'e', 'da', 'das', 'do', 'dos', 'van', 'von', 'der', 'di'}


def _iniciales(nombres):
    resultado = []
    for palabra in (nombres or '').replace('.', '. ').split():
        if palabra.lower() in PARTICULAS:
            continue
        partes = [p for p in palabra.strip('.').split('-') if p]
        letras = ['{}.'.format(next((c for c in parte if c.isalpha()), '').upper()) for parte in partes]
        if letras and all(len(x) > 1 for x in letras):
            resultado.append('-'.join(letras))
    return ' '.join(resultado)


def _formato_cita(nombres, apellidos):
    """Copia congelada de `nucleo.nombres.formato_cita` (las migraciones no deben depender del código vivo)."""
    nombres, apellidos = ' '.join((nombres or '').split()), ' '.join((apellidos or '').split())
    if not apellidos:
        return nombres
    abreviado = _iniciales(nombres)
    return f'{apellidos}, {abreviado}' if abreviado else apellidos


def adelante(apps, schema_editor):
    Persona = apps.get_model('nucleo', 'Persona')
    User = apps.get_model('nucleo', 'User')
    for persona in Persona.objects.all().iterator():
        Persona.objects.filter(pk=persona.pk).update(nombre=_formato_cita(persona.nombre, persona.apellidos)[:300])
        if persona.usuario_id:
            User.objects.filter(pk=persona.usuario_id).update(persona=persona.pk)
    for user in User.objects.filter(persona__isnull=True):
        nombre = _formato_cita(user.first_name, user.last_name) or user.email.split('@')[0]
        user.persona = Persona.objects.create(nombre=nombre, verificado=True)
        user.save(update_fields=['persona'])


def atras(apps, schema_editor):
    Persona = apps.get_model('nucleo', 'Persona')
    User = apps.get_model('nucleo', 'User')
    for user in User.objects.all():
        Persona.objects.filter(pk=user.persona_id).update(usuario=user.pk)
    for persona in Persona.objects.all().iterator():
        apellidos, _, nombres = persona.nombre.rpartition(',')
        if not apellidos:
            apellidos, nombres = persona.nombre, ''
        Persona.objects.filter(pk=persona.pk).update(nombre=nombres.strip()[:150] or '—', apellidos=apellidos.strip()[:150])


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0008_genero_y_sni'),
    ]

    operations = [
        # 1. Esquema intermedio: conviven la relación vieja y la nueva.
        migrations.AlterField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                       related_name='+', to='nucleo.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='persona',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT,
                                       related_name='usuario', to='nucleo.persona'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='historicalpersona',
            name='nombre',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='persona',
            name='apellidos',
            field=models.CharField(blank=True, max_length=150),
        ),
        # 2. Datos.
        migrations.RunPython(adelante, atras),
        # 3. Esquema final.
        migrations.RemoveField(model_name='persona', name='usuario'),
        migrations.RemoveField(model_name='historicalpersona', name='usuario'),
        migrations.RemoveField(model_name='persona', name='apellidos'),
        migrations.RemoveField(model_name='historicalpersona', name='apellidos'),
        migrations.AlterField(
            model_name='user',
            name='persona',
            field=models.OneToOneField(
                help_text='Cómo figura el académico en las publicaciones. Solo un administrador puede cambiarla.',
                on_delete=django.db.models.deletion.PROTECT, related_name='usuario', to='nucleo.persona'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(
                help_text='Como aparece en las publicaciones: apellidos, iniciales. Por ejemplo: Pérez García, J. C.',
                max_length=300, verbose_name='nombre para mostrar'),
        ),
        migrations.AlterField(
            model_name='historicalpersona',
            name='nombre',
            field=models.CharField(
                help_text='Como aparece en las publicaciones: apellidos, iniciales. Por ejemplo: Pérez García, J. C.',
                max_length=300, verbose_name='nombre para mostrar'),
        ),
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['nombre']},
        ),
        migrations.AddConstraint(
            model_name='persona',
            constraint=models.UniqueConstraint(condition=models.Q(('orcid', ''), _negated=True), fields=('orcid',),
                                               name='orcid_unico'),
        ),
    ]
