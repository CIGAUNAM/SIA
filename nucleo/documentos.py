"""Generación de documentos (CV y formatos) a partir de plantillas HTML con WeasyPrint."""

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


class ErrorDocumento(Exception):
    pass


def html_a_pdf(html):
    try:
        from weasyprint import HTML
    except OSError as error:  # Faltan las bibliotecas de sistema (Pango).
        raise ErrorDocumento(f'WeasyPrint no está disponible: instala Pango en el servidor ({error}).')
    return HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf()


def respuesta_documento(request, plantilla, contexto, nombre_archivo, formato='pdf'):
    """Responde con el documento en PDF, o con el HTML (vista previa) si `formato == 'html'`."""
    contexto = {**contexto, 'para_pdf': formato != 'html'}  # El PDF lee imágenes del disco; el HTML, por URL.
    html = render_to_string(plantilla, contexto, request=request)
    if formato == 'html':
        return HttpResponse(html)
    respuesta = HttpResponse(html_a_pdf(html), content_type='application/pdf')
    respuesta['Content-Disposition'] = f'inline; filename="{nombre_archivo}.pdf"'
    return respuesta
