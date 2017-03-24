from django.shortcuts import redirect, render

class LicenciaturaContext():
    contexto = {'tab_lista': 'Mis Licenciaturas', 'tab_agregar': 'Agregar Licenciatura', 'tab_detalle': 'Editar Licenciatura',
               'titulo_lista': 'Mis Licenciaturas', 'titulo_agregar': 'Agregar Licenciatura', 'titulo_detalle': 'Editar Licenciatura',
               'objeto': 'licenciatura', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Licenciaturas'}


class MaestriaContext():
    contexto = {'tab_lista': 'Mis Maestrías', 'tab_agregar': 'Agregar Maestría', 'tab_detalle': 'Editar Maestría',
               'titulo_lista': 'Mis Maestrías', 'titulo_agregar': 'Agregar Maestría', 'titulo_detalle': 'Editar Maestría',
               'objeto': 'maestría', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Maestrías'}


class ObjectCreateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_object = bound_form.save(commit=False)
            new_object.usuario = request.user
            new_object = bound_form.save()
            return redirect(new_object)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux})
