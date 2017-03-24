from django.shortcuts import redirect, render, get_object_or_404



class LicenciaturaContext:
    contexto = {'tab_lista': 'Mis Licenciaturas', 'tab_agregar': 'Agregar Licenciatura', 'tab_detalle': 'Editar Licenciatura',
               'titulo_lista': 'Mis Licenciaturas', 'titulo_agregar': 'Agregar Licenciatura', 'titulo_detalle': 'Editar Licenciatura',
               'objeto': 'licenciatura', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Licenciaturas'}


class MaestriaContext:
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
            new_obj = bound_form.save(commit=False)
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux})


class ObjectUpdateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, usuario=request.user)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, usuario=request.user)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save(commit=False)
            det_obj.usuario = request.user
            det_obj = bound_form.save()
            return redirect(det_obj)
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



