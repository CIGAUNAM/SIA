from django.shortcuts import render, loader, Conte
from nucleo.models import Tag

# Create your views here.

def homepage(request):
    tag_lista = Tag.objects.all()
    template = loader.get_template('nucleo/tag_lista.html')
    context = {'tag_list': tag_lista}
    output = render(context)
    return output