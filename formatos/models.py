from django.conf import settings
from django.db import models

from nucleo.models import Evento, validar_periodo


class Formato(models.Model):
    """Base de las solicitudes administrativas que se imprimen en PDF."""
    fecha = models.DateField('fecha de solicitud', auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')

    plantilla_pdf = None

    class Meta:
        abstract = True
        ordering = ['-fecha', '-pk']


class ServicioTransporte(Formato):
    class Uso(models.TextChoices):
        DOCENCIA = 'DOCENCIA', 'Docencia'
        INVESTIGACION = 'INVESTIGACION', 'Investigación'

    class Tipo(models.TextChoices):
        LOCAL = 'LOCAL', 'Local'
        FORANEO = 'FORANEO', 'Foráneo'

    uso = models.CharField(max_length=20, choices=Uso.choices)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    num_pasajeros = models.PositiveIntegerField('número de pasajeros')
    km_aprox = models.PositiveIntegerField('kilómetros aproximados')
    gasto_casetas = models.DecimalField('gasto en casetas', max_digits=12, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_fin = models.DateField('fecha de término')
    salidas_diarias = models.PositiveIntegerField(null=True, blank=True)
    tiempo_completo = models.PositiveIntegerField('días de tiempo completo', null=True, blank=True)
    objetivo = models.TextField()

    plantilla_pdf = 'formatos/servicio_transporte.html'

    class Meta(Formato.Meta):
        verbose_name = 'solicitud de servicio de transporte'
        verbose_name_plural = 'solicitudes de servicio de transporte'

    def __str__(self):
        return f'Transporte {self.fecha_inicio:%d/%m/%Y} — {self.usuario}'

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_inicio, self.fecha_fin)


class LicenciaGoceSueldo(Formato):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    tipo_participacion = models.CharField('tipo de participación', max_length=255)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_fin = models.DateField('fecha de término')
    importancia = models.TextField('importancia para la entidad')
    costo = models.DecimalField('costo total (MXN)', max_digits=12, decimal_places=2)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    presupuesto_personal = models.BooleanField(default=False)
    carta_invitacion = models.BooleanField('anexa carta de invitación', default=False)
    aceptacion_ponencia = models.BooleanField('anexa aceptación de ponencia', default=False)
    otro_anexo = models.CharField(max_length=255, blank=True)

    plantilla_pdf = 'formatos/licencia_goce_sueldo.html'

    class Meta(Formato.Meta):
        verbose_name = 'solicitud de licencia con goce de sueldo'
        verbose_name_plural = 'solicitudes de licencia con goce de sueldo'

    def __str__(self):
        return f'Licencia: {self.evento} — {self.usuario}'

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_inicio, self.fecha_fin)


class PagoViaticos(Formato):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    actividades = models.TextField('actividades a realizar')
    importe = models.DecimalField('importe solicitado (MXN)', max_digits=12, decimal_places=2)
    num_acta = models.CharField('acta de consejo interno', max_length=30, blank=True)
    beneficiario = models.CharField('nombre del cheque', max_length=255,
                                    help_text='Persona a cuyo nombre se expide el cheque.')
    cargo_papiit = models.BooleanField('con cargo a PAPIIT', default=False)
    cargo_conacyt = models.BooleanField('con cargo a CONAHCYT', default=False)
    cargo_papime = models.BooleanField('con cargo a PAPIME', default=False)
    cargo_ie = models.BooleanField('con cargo a ingresos extraordinarios', default=False)
    cargo_po = models.BooleanField('con cargo a presupuesto operativo', default=False)
    cargo_paep = models.BooleanField('con cargo a PAEP', default=False)
    cargo_otro = models.BooleanField('con cargo a otro', default=False)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)

    plantilla_pdf = 'formatos/pago_viaticos.html'

    class Meta(Formato.Meta):
        verbose_name = 'solicitud de pago de viáticos'
        verbose_name_plural = 'solicitudes de pago de viáticos'

    def __str__(self):
        return f'Viáticos: {self.evento} — {self.usuario}'

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_salida, self.fecha_regreso, 'fecha_regreso')


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
