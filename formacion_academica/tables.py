
from formacion_academica.models import CursoEspecializacion
from table import Table
from table.columns import Column


class TablaCursos(Table):
    nombre_curso = Column(field='nombre', header='Nombre de curso')
    horas = Column(field='horas', header='Horas')
    fecha_inicio = Column(field='fecha_inicio', header='Fecha de inicio')
    area_conocimiento = Column(field='area_conocimiento', header='Área de conocimiento')


    class Meta:
        model = CursoEspecializacion