from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.urls import path
from unfold.sites import UnfoldAdminSite


class AutocompleteSIA(AutocompleteJsonView):
    """En los buscadores de los formularios, cada persona indica si está adscrita (el script la colorea)."""

    def serialize_result(self, obj, to_field_name):
        from nucleo.admin_base import adscripcion
        from nucleo.models import Persona

        resultado = super().serialize_result(obj, to_field_name)
        if isinstance(obj, Persona):
            resultado['adscripcion'] = adscripcion(obj)
        return resultado


class SIAAdminSite(UnfoldAdminSite):
    site_header = 'SIA · Sistema de Información Académica'
    site_title = 'SIA'
    index_title = 'Inicio'
    index_template = 'admin/tablero.html'

    def autocomplete_view(self, request):
        return AutocompleteSIA.as_view(admin_site=self)(request)

    def get_urls(self):
        from nucleo.cv import cv_view
        from nucleo.vistas import (avance_view, evidencia_view, informe_excel_view, mi_informe_view, mi_perfil_view,
                                   orcid_view, ver_academico_view)

        return [
            path('cv/', self.admin_view(cv_view), name='cv'),
            path('cv/<int:usuario_id>/', self.admin_view(cv_view), name='cv_usuario'),
            path('perfil/', self.admin_view(mi_perfil_view), name='perfil'),
            path('orcid/', self.admin_view(orcid_view), name='orcid'),
            path('ver-academico/', self.admin_view(ver_academico_view), name='ver_academico'),
            path('informe/', self.admin_view(mi_informe_view), name='informe'),
            path('informe/avance/', self.admin_view(avance_view), name='informe_avance'),
            path('informe/excel/', self.admin_view(informe_excel_view), name='informe_excel'),
            path('evidencia/<path:nombre>', self.admin_view(evidencia_view), name='evidencia'),
            *super().get_urls(),
        ]
