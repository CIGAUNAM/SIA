from django.db import models
from nucleo.models import User, Institucion, Dependencia, Cargo
from django.urls import reverse


# Create your models here.


class Comision(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('comision_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Comisiones'


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


class CargoAcademicoAdministrativo(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "[ {} : {} ] : {} : {} : {} : {}".format(self.usuario, self.cargo, self.dependencia.nombre_dependencia,
                                                        self.dependencia.institucion_dependencia, self.fecha_inicio, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('cargo_academico_administrativo_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Cargos Académico-Administrativos'
        unique_together = ('cargo', 'usuario', 'dependencia', 'fecha_inicio')
        ordering = ['-fecha_inicio']
        get_latest_by = ['user', 'cargo']


class RepresentacionOrganoColegiado(models.Model):
    representacion = models.ForeignKey(Representacion, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag, related_name='representante_ante_organo_colegiado_tags', blank=True)

    def __str__(self):
        return "{} : {} : {} ".format(self.representacion, self.dependencia, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('representacion_organo_colegiado_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Representantes Ante Organos Colegiados'
        unique_together = ('usuario', 'representacion', 'fecha_inicio')
        ordering = ['-fecha_inicio']


class ComisionAcademica(models.Model):
    comision_academica = models.ForeignKey(Comision, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    es_evaluacion = models.BooleanField(default=False)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
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
