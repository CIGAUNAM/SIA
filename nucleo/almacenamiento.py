from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class AlmacenamientoProtegido(FileSystemStorage):
    """Archivos fuera de MEDIA_URL: se descargan solo a través de una vista que revisa permisos."""

    def __init__(self):
        super().__init__(location=settings.PRIVATE_MEDIA_ROOT)

    def url(self, name):
        return reverse('admin:evidencia', args=[name])
