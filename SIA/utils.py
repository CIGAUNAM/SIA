from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import (Http404, HttpResponse)
from nucleo.models import User
from nucleo.forms import *

from django.contrib import messages

#

class NucleoObjectCreateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form})


class ObjectCreateMixinNucleo:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.success(request, "Registro creado con éxito")
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class ObjectUpdateMixinNucleo:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            messages.success(request, "Registro actualizado con éxito")
            return redirect(det_obj)
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class ObjectCreateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            messages.success(request, "Registro creado con éxito")
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class ObjectUpdateMixin:
    form_class = None
    template_name = ''
    aux = {}
    institucion = None

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
            messages.success(request, "Registro actualizado con éxito")
            return redirect(det_obj)
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



class ObjectCreateVarMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.success(request, "Registro creado con éxito")
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class ObjectUpdateVarMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            messages.success(request, "Registro actualizado con éxito")
            return redirect(det_obj)
        else:
            messages.error(request, "Hubo un error")
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})