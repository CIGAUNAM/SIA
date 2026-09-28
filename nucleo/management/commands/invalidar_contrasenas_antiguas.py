"""Invalida las contraseñas heredadas del SIA anterior (sus hashes estuvieron públicos en el historial de git).

Se reconocen porque su hash usa menos iteraciones que las actuales de Django: una contraseña asignada en el
sistema nuevo ya usa las actuales. Ojo: Django actualiza el hash cuando alguien inicia sesión, así que conviene
correrlo antes de que los académicos vuelvan a entrar con su contraseña vieja.
"""

from django.contrib.auth.hashers import get_hasher, identify_hasher
from django.core.management.base import BaseCommand

from nucleo.models import User


def es_antigua(hash_contrasena):
    if not hash_contrasena or hash_contrasena.startswith('!'):
        return False  # Ya sin contraseña utilizable.
    try:
        hasher = identify_hasher(hash_contrasena)
    except ValueError:
        return True  # Formato desconocido: no se puede confiar en él.
    actual = get_hasher()
    if hasher.algorithm != actual.algorithm:
        return True
    return int(hasher.decode(hash_contrasena).get('iterations', 0)) < actual.iterations


class Command(BaseCommand):
    help = ('Invalida las contraseñas heredadas del SIA anterior; las asignadas en el sistema nuevo no se tocan. '
            'Sin --aplicar solo muestra las cuentas afectadas.')

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Invalida las contraseñas.')

    def handle(self, *args, aplicar=False, **options):
        cuentas = [u for u in User.objects.order_by('email') if es_antigua(u.password)]
        conservan = sum(1 for u in User.objects.filter(is_active=True)
                        if u.has_usable_password() and not es_antigua(u.password))
        for cuenta in cuentas:
            marca = ' (superusuario)' if cuenta.is_superuser else ''
            self.stdout.write(f'{cuenta.email} — {cuenta.get_full_name() or "sin nombre"}{marca}')
            if aplicar:
                cuenta.set_unusable_password()
                cuenta.save(update_fields=['password'])
        if aplicar:
            self.stdout.write(self.style.SUCCESS(
                f'{len(cuentas)} contraseñas invalidadas. Para que entren, asígnales una en Usuarios → '
                f'"Establecer contraseña". {conservan} cuentas activas conservan la suya.'))
        else:
            self.stdout.write(self.style.WARNING(
                f'{len(cuentas)} contraseñas por invalidar; {conservan} cuentas activas conservan la suya. '
                f'Usa --aplicar para hacerlo.'))
