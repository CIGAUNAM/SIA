from . models import *
from django import forms
from django.core.exceptions import ValidationError

#


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['slug', ]

    def clean_tag(self):
        return self.cleaned_data['tag'].lower()



class TagForm1(forms.Form):
    tag = forms.CharField(max_length=50)

    def clean_tag(self):
        return self.cleaned_data['tag'].lower()

    def save(self):
        new_tag = Tag.objects.create(
        tag=self.cleaned_data['tag'],)

        return new_tag




