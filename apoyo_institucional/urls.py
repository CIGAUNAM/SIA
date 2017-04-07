from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^cargos-academico-dministrativos/json/', CargoAcademicoAdministrativoJSON.as_view(), name='cargo_academico_administrativo_lista__json'),
    #url(r'^memorias-in-extenso/json-otros/', MemoriaInExtensoJSON.as_view(otros=True), name='memoria_in_extenso_lista_otros__json'),
    url(r'^cargos-academico-dministrativos/$', CargoAcademicoAdministrativoLista.as_view(), name='cargo_academico_administrativo_lista'),
    url(r'^cargos-academico-dministrativos/(?P<pk>[\w\-]+)/$', CargoAcademicoAdministrativoDetalle.as_view(), name='cargo_academico_administrativo_detalle'),


]