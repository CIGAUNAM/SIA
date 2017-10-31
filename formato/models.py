from django.db import models
from nucleo.models import User, Estado, Ciudad
from django.core.urlresolvers import reverse

# Create your models here.


class FormatoServicioTransporte(models.Model):
    fecha = models.DateField(auto_now_add=True)
    uso = models.CharField(max_length=20, choices=(('', '-------'), ('DOCENCIA' 'Docencia'), ('INVESTIGACION', 'Investigaciòn')))
    num_pasajeros = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=(('', '-------'), ('LOCAL', 'Local'), ('FORANEO', 'Foraneo')))
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    km_aprox = models.PositiveIntegerField()
    gasto_casetas = models.DecimalField(decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    salidas_diarias = models.PositiveIntegerField(blank=True, null=True)
    tiempo_completo = models.PositiveIntegerField(blank=True, null=True)
    objetivo = models.TextField()
    usuario = models.ForeignKey(User)

    def __str__(self):
        return "{} : {}".format(self.fecha, self.usuario)

    def natural_key(self):
        return "{} : {}".format(self.fecha, self.usuario)

    def get_absolute_url(self):
        return reverse('formato_servicio_transporte_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'usuario']
        verbose_name = 'Formato de solicitud de servicio de transporte'
        verbose_name_plural = 'Formatos de solicitud de servicio de transporte'