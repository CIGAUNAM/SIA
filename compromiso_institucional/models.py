from django.db import models
from nucleo.models import User, Institucion, Dependencia, Cargo, InstitucionSimple
from django.urls import reverse


# Create your models here.


class ComisionInstitucional(models.Model):
    comisioninstitucional_nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.comisioninstitucional_nombre

    def natural_key(self):
        return self.comisioninstitucional_nombre

    def get_absolute_url(self):
        return reverse('comisioninstitucional_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Comisión Institucional'
        verbose_name_plural = 'Comisiones Institucionales'


class ActividadApoyo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('actividad_apoyo_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Actividad de apoyo'
        verbose_name_plural = 'Actividades de apoyo'


class Representacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('representacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Representación'
        verbose_name_plural = 'Representaciones'


class LaborDirectivaCoordinacion(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING, null=True, blank=True)
    tipo_cargo = models.CharField(max_length=255) # sacar el texto de cargo
    institucion2 = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "[{} : {}] : {} : {}".format(self.tipo_cargo, self.dependencia,
                                                        self.fecha_inicio, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('cargo_academico_administrativo_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Labores Directivaa y de Coordinación'
        unique_together = ('tipo_cargo', 'usuario', 'dependencia', 'fecha_inicio')
        ordering = ['-fecha_inicio']
        get_latest_by = ['user', 'tipo_cargo']


class RepresentacionOrganoColegiadoUNAM(models.Model):
    tipo_representacion = models.CharField(max_length=30, choices=(('', '-------'), ('DENTRO', 'Dentro de la UNAM'), ('REPRESENTACION', 'Con representacion UNAM (Solo por designación)')))
    representacion_dentro_unam = models.CharField(max_length=30, choices=(('', '-------'), ('PRIDE', 'PRIDE'), ('CAACS', 'CAACS'), ('CONSEJO_INTERNO', 'Consejo interno'),
                                                                          ('COMISION_DICTAMINADORA', 'Comisión dictaminadora'), ('COMISION_EVALUADORA', 'Comisiòn evaluadora'),
                                                                          ('OTRA', 'Otra')), blank=True, null=True)
    representacion_dentro_unam_otra = models.CharField(max_length=250, blank=True, null=True)
    representacion_fuera_unam = models.CharField(max_length=250, blank=True, null=True)

    institucion_dentro_unam = models.ForeignKey(InstitucionSimple, blank=True, null=True, related_name='representacion_organo_colegiado_dentrounam', on_delete=models.DO_NOTHING)
    institucion_fuera_unam = models.ForeignKey(InstitucionSimple, blank=True, null=True, related_name='representacion_organo_colegiado_fueraunam', on_delete=models.DO_NOTHING)

    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {} ".format(self.usuario, self.tipo_representacion, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('representacion_organo_colegiado_unam_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Representantes Ante Organos Colegiados'
        unique_together = ('usuario', 'tipo_representacion', 'fecha_inicio')
        ordering = ['-fecha_inicio']


class ComisionInstitucionalCIGA(models.Model):
    comision_academica = models.ForeignKey(ComisionInstitucional, null=True, blank=True, on_delete=models.DO_NOTHING)
    tipo_comision = models.CharField(max_length=255) # sacar el texto de comision_academica
    # es_evaluacion = models.BooleanField(default=False)
    tipo_institucion = models.CharField(max_length=30, choices=(('', '-------'), ('INTERIOR', 'Al interior del CIGA'), ('EXTERIOR', 'Al exterior del CIGA')))
    institucion2 = models.ForeignKey(Institucion, null=True, blank=True, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, null=True, blank=True, on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)

    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "[{}] : {} : {} : {}".format(self.usuario, self.comision_academica, self.fecha_inicio, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('comision_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Comisiones Académicas'
        unique_together = ('comision_academica', 'usuario', 'fecha_inicio')
        ordering = ['fecha_inicio']
        get_latest_by = ['user', 'comision_academica']


class ApoyoTecnico(models.Model):
    actividad_apoyo = models.ForeignKey(ActividadApoyo, on_delete=models.DO_NOTHING)
    descripcion = models.TextField()
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "[{}] : {} : {}".format(self.usuario, self.actividad_apoyo, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('apoyo_tecnico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Apoyos de Técnicos'
        unique_together = ('actividad_apoyo', 'usuario', 'dependencia', 'fecha_inicio')
        ordering = ['-fecha_inicio']
        get_latest_by = ['usuario', 'actividad_apoyo']


class ApoyoOtraActividad(models.Model):
    actividad_apoyo = models.ForeignKey(ActividadApoyo, on_delete=models.DO_NOTHING)
    descripcion = models.TextField()
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "[{}] : {} : {}".format(self.usuario, self.actividad_apoyo, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('apoyo_otra_actividad_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Apoyos en Otras Actividades'
        unique_together = ('actividad_apoyo', 'usuario', 'dependencia', 'fecha_inicio')
        ordering = ['-fecha_inicio']
        get_latest_by = ['usuario', 'actividad_apoyo']
