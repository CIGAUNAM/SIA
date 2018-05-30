# Generated by Django 2.0.5 on 2018-05-03 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nucleo', '0001_initial'),
        ('investigacion', '0001_initial'),
        ('formatos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formatoserviciotransporte',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Ciudad'),
        ),
        migrations.AddField(
            model_name='formatoserviciotransporte',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Estado'),
        ),
        migrations.AddField(
            model_name='formatoserviciotransporte',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formatopagoviatico',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Evento'),
        ),
        migrations.AddField(
            model_name='formatopagoviatico',
            name='nombre_cheque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='formato_pago_viatico_nombre_cheque_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formatopagoviatico',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='formatopagoviatico',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='formato_pago_viatico_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='formatolicenciagocesueldo',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Evento'),
        ),
        migrations.AddField(
            model_name='formatolicenciagocesueldo',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='formatolicenciagocesueldo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
