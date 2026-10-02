"""Activa las cuentas del personal vigente de la entidad y desactiva las de quienes ya no están.

Solo tiene cuenta el personal de la entidad (los externos figuran como personas). Quien deja la entidad conserva su
cuenta, desactivada: su producción sigue en el SIA y en su CV, pero ya no entra al sistema. Es vigente:
- un investigador o técnico con situación académica del año más reciente y sin fecha de egreso pasada;
- un posdoc (u otro tipo) cuya estancia no ha terminado, o recién dado de alta sin fechas (lo trae el último informe).
No se tocan los superusuarios ni el personal administrativo (sus cuentas las gestiona Administración a mano).
Sin --aplicar es un simulacro.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from nucleo.models import SituacionAcademica, User
from nucleo.permisos import GRUPO_ADMINISTRACION

#: Una cuenta sin fechas de estancia creada hace menos de esto se considera vigente (alta del último informe).
ALTA_RECIENTE = timedelta(days=365)


def vigente(usuario, anio_corte, hoy):
    if usuario.egreso_entidad and usuario.egreso_entidad < hoy:
        return False
    if usuario.tipo in (User.Tipo.INVESTIGADOR, User.Tipo.TECNICO):
        return SituacionAcademica.objects.filter(usuario=usuario, anio=anio_corte).exists()
    if usuario.egreso_entidad:
        return True
    return usuario.ingreso_entidad is None and usuario.date_joined.date() >= hoy - ALTA_RECIENTE


class Command(BaseCommand):
    help = 'Activa las cuentas del personal vigente y desactiva las de quienes ya no están en la entidad.'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true')

    def handle(self, aplicar=False, **options):
        hoy = timezone.localdate()
        anio_corte = SituacionAcademica.objects.order_by('-anio').values_list('anio', flat=True).first()
        cambios = {True: [], False: []}
        with transaction.atomic():
            for u in (User.objects.filter(is_superuser=False).exclude(tipo=User.Tipo.ADMINISTRATIVO)
                      .exclude(groups__name=GRUPO_ADMINISTRACION).order_by('last_name')):
                activo = vigente(u, anio_corte, hoy)
                if u.is_active != activo:
                    u.is_active = activo
                    u.save(update_fields=['is_active'])
                    cambios[activo].append(u)
            if not aplicar:
                transaction.set_rollback(True)
        for activo, titulo in ((True, 'Se activan'), (False, 'Se desactivan (ya no están en la entidad)')):
            self.stdout.write(self.style.MIGRATE_HEADING(f'{titulo}: {len(cambios[activo])}'))
            for u in cambios[activo]:
                self.stdout.write(f'  {u} ({u.get_tipo_display().lower()})')
        self.stdout.write(self.style.SUCCESS('Cuentas actualizadas.' if aplicar else 'Simulacro: nada se guardó (usa --aplicar).'))
