"""Busca en ORCID, por su correo, el ORCID de las cuentas cuya persona aún no lo tiene."""

from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo.externos import ErrorServicio, orcid_por_correo
from nucleo.models import Persona, User
from nucleo.sugerencias_orcid import asignar_orcid


class Command(BaseCommand):
    help = ('Busca en ORCID (por el correo de la cuenta, si la persona lo hizo público) el ORCID de las cuentas que '
            'no lo tienen. Sin --aplicar solo muestra lo encontrado.')

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Guarda los ORCID encontrados.')

    def handle(self, *args, aplicar=False, **options):
        encontrados = 0
        cuentas = (User.objects.filter(persona__orcid='').exclude(email__endswith='.invalid')
                   .select_related('persona').order_by('persona__nombre'))
        total = cuentas.count()
        for cuenta in cuentas:
            try:
                resultado = orcid_por_correo(cuenta.email)
            except ErrorServicio as error:
                self.stderr.write(f'{cuenta.email}: {error}')
                continue
            if resultado is None:
                continue
            orcid, nombre = resultado
            persona = cuenta.persona
            otra = Persona.objects.filter(orcid=orcid).exclude(pk=persona.pk).first()
            if otra is not None and otra.tiene_cuenta:
                self.stderr.write(f'{cuenta.email}: {orcid} ya es de la cuenta {otra.usuario}; se omite.')
                continue
            nota = f' (se unirá «{otra}», que ya tenía ese ORCID)' if otra else ''
            self.stdout.write(f'{cuenta.email}: {orcid} — ORCID lo nombra «{nombre}», figura como «{persona}»{nota}')
            if aplicar:
                with transaction.atomic():
                    asignar_orcid(persona, orcid)
            encontrados += 1
        accion = 'guardados' if aplicar else 'encontrados (usa --aplicar para guardarlos)'
        self.stdout.write(self.style.SUCCESS(f'{encontrados} de {total} cuentas sin ORCID: {accion}.'))
