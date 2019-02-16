from django.db import models
from nucleo.models import User, Estado, Ciudad, Evento
from investigacion.models import ProyectoInvestigacion
from django.urls import reverse


# Create your models here.


class FormatoServicioTransporte(models.Model):
    fecha = models.DateField(auto_now_add=True)
    uso = models.CharField(max_length=20, choices=(('', '-------'), ('DOCENCIA', 'Docencia'),
                                                   ('INVESTIGACION', 'Investigación')))
    num_pasajeros = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=(('', '-------'), ('LOCAL', 'Local'), ('FORANEO', 'Foraneo')))
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    km_aprox = models.PositiveIntegerField()
    gasto_casetas = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    salidas_diarias = models.PositiveIntegerField(blank=True, null=True)
    tiempo_completo = models.PositiveIntegerField(blank=True, null=True)
    objetivo = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.fecha_inicio, self.usuario)

    def natural_key(self):
        return "{} : {}".format(self.fecha_inicio, self.usuario)

    def get_absolute_url(self):
        return reverse('formato_servicio_transporte_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio', 'usuario']
        verbose_name = 'Formato de solicitud de servicio de transporte'
        verbose_name_plural = 'Formatos de solicitud de servicio de transporte'


class FormatoLicenciaGoceSueldo(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    tipo_participacion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    importancia = models.TextField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    presupuesto_personal = models.BooleanField(default=False)
    carta_invitacion = models.BooleanField(default=False)
    aceptacion_ponencia = models.BooleanField(default=False)
    otro_anexo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.fecha_inicio, self.usuario)

    def natural_key(self):
        return "{} : {}".format(self.fecha_inicio, self.usuario)

    def get_absolute_url(self):
        return reverse('formato_licencia_goce_sueldo_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'usuario']
        verbose_name = 'Formato de licencia con goce de sueldo'
        verbose_name_plural = 'Formatos de licencia con goce de sueldo'


class FormatoPagoViatico(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, related_name='formato_pago_viatico_usuario', on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    actividades = models.TextField()
    importe = models.DecimalField(max_digits=20, decimal_places=2)
    num_acta = models.PositiveIntegerField()
    nombre_cheque = models.ForeignKey(User, related_name='formato_pago_viatico_nombre_cheque_usuario',
                                      on_delete=models.DO_NOTHING)
    cargo_papiit = models.BooleanField(default=False)
    cargo_conacyt = models.BooleanField(default=False)
    cargo_papime = models.BooleanField(default=False)
    cargo_ie = models.BooleanField(default=False)
    cargo_po = models.BooleanField(default=False)
    cargo_paep = models.BooleanField(default=False)
    cargo_otro = models.BooleanField(default=False)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.fecha_salida, self.usuario)

    def natural_key(self):
        return "{} : {}".format(self.fecha_salida, self.usuario)

    def get_absolute_url(self):
        return reverse('formato_pago_viatico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_salida', 'usuario']
        verbose_name = 'Formato de pago de viaticos'
        verbose_name_plural = 'Formatos de pago de viaticos'
