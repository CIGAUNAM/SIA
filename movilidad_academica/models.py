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

    def __str__(self):
        return "{} : {}".format(str(self.academico), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Actividad de vinculación'
        verbose_name_plural = 'Actividades de vinculación'


class InvitadoMovilidad(models.Model):
    invitado = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.CharField(max_length=50, choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'), ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    redes_academicas = models.ManyToManyField(RedAcademica, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.invitado), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Invitado'
        verbose_name_plural = 'Invitados'


class EstanciaMovilidad(models.Model):
    anfitrion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.CharField(max_length=50, choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'), ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    redes_academicas = models.ManyToManyField(RedAcademica, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.anfitrion), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Estancia'
        verbose_name_plural = 'Estancias'


class SabaticoMovilidad(models.Model):
    anfitrion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.CharField(max_length=50, choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'), ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    redes_academicas = models.ManyToManyField(RedAcademica, blank=True)
    proyecto = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.anfitrion), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Sabático'
        verbose_name_plural = 'Sabático'