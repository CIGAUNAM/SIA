from django.db import models
from nucleo.models import User, Institucion, Dependencia, Financiamiento
from investigacion.models import ProyectoInvestigacion
from vinculacion.models import RedAcademica


# Create your models here.


class MovilidadAcademica(models.Model):
    tipo = models.CharField(max_length=30, choices=(('INVITACION', 'Invitación'),
                                                    ('ESTANCIA', 'Estancia de colaboración'),
                                                    ('SABATICO', 'Sabático')))
    academico = models.ForeignKey(User, related_name='movilidad_academica_academico', on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.ForeignKey(Financiamiento, on_delete=models.DO_NOTHING)
    redes_academicas = models.ManyToManyField(RedAcademica, related_name='vinculacion_redes_academicas', blank=True)
    proyecto_investigacion = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True,
                                               on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, related_name='movilidad_academica_usuario', on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag, related_name='vinculacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(str(self.academico), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Actividad de vinculación'
        verbose_name_plural = 'Actividades de vinculación'
