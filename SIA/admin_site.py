from django.urls import path
from unfold.sites import UnfoldAdminSite


class SIAAdminSite(UnfoldAdminSite):
    site_header = 'SIA · Sistema de Información Académica'
    site_title = 'SIA'
    index_title = 'Inicio'
    index_template = 'admin/tablero.html'

    def get_urls(self):
        from nucleo.cv import cv_view
        from nucleo.vistas import avance_view, evidencia_view, informe_excel_view, mi_informe_view, mi_perfil_view

        return [
            path('cv/', self.admin_view(cv_view), name='cv'),
            path('cv/<int:usuario_id>/', self.admin_view(cv_view), name='cv_usuario'),
            path('perfil/', self.admin_view(mi_perfil_view), name='perfil'),
            path('informe/', self.admin_view(mi_informe_view), name='informe'),
            path('informe/avance/', self.admin_view(avance_view), name='informe_avance'),
            path('informe/excel/', self.admin_view(informe_excel_view), name='informe_excel'),
            path('evidencia/<path:nombre>', self.admin_view(evidencia_view), name='evidencia'),
            *super().get_urls(),
        ]
