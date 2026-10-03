"""Correcciones de datos para alinear el SIA con el informe anual oficial, que el importador no puede deducir solo.

El Excel y el informe son la versión oficial; cuando un registro que ya estaba en el SIA los contradice y la fila no
alcanza para corregirlo (p. ej. el contrato de alguien que causó baja), la corrección queda aquí, con su motivo en el
historial. Se pueden aplicar varias veces. Sin --aplicar es un simulacro.
"""

from datetime import date

from cities_light.models import Country
from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo.fusion import fusionar
from nucleo.models import Institucion, Revista, SituacionAcademica

#: (apellidos de la cuenta, contrato, motivo): baja en el corte; el informe lo cuenta con su contrato anterior.
CONTRATOS = [('Bocco Verdinelli', SituacionAcademica.Contrato.DEFINITIVO,
              'Contrato definitivo hasta su baja (así lo cuenta el informe)')]
#: (nombre de la revista, país, motivo)
PAISES_REVISTA = [('Revista Cartográfica', 'Desconocido', 'Revista del IPGH, internacional según el informe'),
                  ('Revista de urbanismo', 'Chile', 'Revista de la Universidad de Chile')]
#: (inicio del título, cambios, motivo): artículos que el Excel da por aceptados y ya se publicaron (el informe los cuenta).
ARTICULOS_PUBLICADOS = [
    ('De territorios excluidos a territorios de inclusión en el periurbano de Morelia',
     {'status': 'PUBLICADO', 'fecha_publicado': date(2026, 6, 1), 'numero': '54',
      'doi': '10.5354/0717-5051.2026.81172',
      'url': 'https://revistaurbanismo.uchile.cl/index.php/RU/article/view/81172'},
     'Publicado en Revista de Urbanismo 54 (junio de 2026)'),
]
#: (nombre que queda, siglas, nombres que se le unen): dependencias de la UNAM escritas de varias formas.
DEPENDENCIAS_UNAM = [('Instituto de Geografía (IGg)', ['Instituto de Geografía', 'IGg', 'IGG',
                                                       'Instituto de Geografía de la UNAM'])]


class Command(BaseCommand):
    help = 'Aplica las correcciones de datos que alinean el SIA con el informe anual oficial.'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true')

    def handle(self, aplicar=False, **options):
        with transaction.atomic():
            for apellidos, contrato, motivo in CONTRATOS:
                for s in SituacionAcademica.objects.filter(usuario__last_name=apellidos).exclude(contrato=contrato):
                    s.contrato, s._change_reason = contrato, motivo
                    s.save()
                    self.stdout.write(f'  Contrato {s.anio} de {s.usuario}: {s.get_contrato_display()}')
            for nombre, pais, motivo in PAISES_REVISTA:
                destino = Country.objects.get(name=pais)
                for r in Revista.objects.filter(nombre=nombre).exclude(pais=destino):
                    r.pais, r._change_reason = destino, motivo
                    r.save()
                    self.stdout.write(f'  País de «{r.nombre}»: {pais}')
            from investigacion.models import ArticuloCientifico

            for inicio, cambios, motivo in ARTICULOS_PUBLICADOS:
                for a in ArticuloCientifico.objects.filter(titulo__istartswith=inicio):
                    if any(getattr(a, k) != v for k, v in cambios.items()):
                        for k, v in cambios.items():
                            setattr(a, k, v)
                        a._change_reason = motivo
                        a.save()
                        self.stdout.write(f'  Publicado: «{a.titulo[:60]}»')
            mexico = Country.objects.get(code2='MX')
            for final, nombres in DEPENDENCIAS_UNAM:
                # Solo las de México sin institución padre ajena a la UNAM (no el «Instituto de Geografía» de otra).
                grupo = [i for i in Institucion.objects.filter(nombre__in=[final, *nombres], pais=mexico)
                         .select_related('padre')
                         if i.padre is None or i.padre.pertenece_unam or 'UNAM' in i.padre.nombre]
                if not grupo:
                    continue
                grupo.sort(key=lambda i: (i.nombre != final, not i.pertenece_unam, i.pk))
                conservar, otros = grupo[0], grupo[1:]
                if otros:
                    fusionar(conservar, otros)
                if conservar.nombre != final or not conservar.pertenece_unam:
                    conservar.nombre, conservar.pertenece_unam = final, True
                    conservar._change_reason = 'Dependencia de la UNAM con sus siglas (el informe la escribe «IGg»)'
                    conservar.save()
                self.stdout.write(f'  «{final}» ← {len(otros)} duplicados')
            if not aplicar:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS('Correcciones aplicadas.' if aplicar else
                                             'Simulacro: nada se guardó (usa --aplicar).'))
