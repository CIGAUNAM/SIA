from django.db import models

from nucleo.models import Participante, Persona


class DesarrolloTecnologico(models.Model):
    nombre = models.CharField(max_length=254, unique=True)
    descripcion = models.TextField('descripción')
    version = models.CharField('versión', max_length=100, blank=True)
    patente = models.CharField(max_length=255, blank=True)
    licencia = models.CharField(max_length=254, blank=True)
    url = models.URLField('URL', blank=True)
    fecha = models.DateField(null=True, blank=True)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    autores = models.ManyToManyField(Persona, through='DesarrolloTecnologicoAutor', related_name='desarrollos_tecnologicos')

    class Meta:
        ordering = ['-fecha', 'nombre']
        verbose_name = 'desarrollo tecnológico'
        verbose_name_plural = 'desarrollos tecnológicos'

    def __str__(self):
        return self.nombre


class DesarrolloTecnologicoAutor(Participante):
    desarrollo = models.ForeignKey(DesarrolloTecnologico, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['desarrollo', 'persona'], name='desarrollo_autor_unico')]


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
