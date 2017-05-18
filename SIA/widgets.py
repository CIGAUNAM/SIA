from django.forms.widgets import Widget, Select, Input, DateTimeBaseInput, DateInput
from django.template import loader
from django.utils.safestring import mark_safe
import copy
from django.utils.html import conditional_escape, format_html, html_safe
from django.forms.utils import flatatt, to_current_timezone
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.utils import datetime_safe, formats, six
from django import forms
from django.conf import settings
from itertools import chain
from django_select2.forms import Select2Mixin, ModelSelect2Widget, ModelSelect2Mixin, HeavySelect2Widget, HeavySelect2Mixin

class wCharField(Widget):
    template_name = 'widgets/CharField.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)

        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

class wNumberField(Widget):
    template_name = 'widgets/NumberField.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class wTextarea(Widget):
    template_name = 'widgets/Textarea.html'
    is_required = False

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class wDateField(DateInput):
    template_name = 'widgets/DateField.html'
    format_key = 'DATE_INPUT_FORMATS'
    format = None

    def get_context(self, name, value, attrs=None):

        if value:
            tfecha = str(formats.localize_input(value, formats.get_format(self.format_key)[0]))
            try:
                tfecha = tfecha.split("/")
                fecha = str(tfecha[2]) + "-" + str(tfecha[1]) + "-" + str(tfecha[0])
                return {'widget': {
                    'name': name,
                    'value': fecha,
                }}
            except:
                return {'widget': {
                    'name': name,
                    'value': None,
                }}
        else:
            return {'widget': {
                'name': name,
                'value': None,
            }}


    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        print("hola")
        return mark_safe(template)





class wInput(Input):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = None  # Subclasses must define this.

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<input{} />', flatatt(final_attrs))

class Select3Mixin(Select2Mixin):
    """
    The base mixin of all Select2 widgets.

    This mixin is responsible for rendering the necessary
    data attributes for select2 as well as adding the static
    form media.
    """

    def build_attrs(self, *args, **kwargs):
        """Add select2 data attributes."""
        attrs = super(Select3Mixin, self).build_attrs(*args, **kwargs)
        if self.is_required:
            attrs.setdefault('data-allow-clear', 'false')
        else:
            attrs.setdefault('data-allow-clear', 'true')
            attrs.setdefault('data-placeholder', '')

        attrs.setdefault('data-minimum-input-length', 0)
        if 'class' in attrs:
            attrs['class'] += ' django-select2'
        else:
            attrs['class'] = 'django-select2'
        return attrs

    def optgroups(self, name, value, attrs=None):
        """Add empty option for clearable selects."""
        if not self.is_required and not self.allow_multiple_selected:
            self.choices = list(chain([('', '')], self.choices))
        return super(Select3Mixin, self).optgroups(name, value, attrs=attrs)

    def render_options(self, *args, **kwargs):
        """Render options including an empty one, if the field is not required."""
        output = '<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else ''
        output += super(Select3Mixin, self).render_options(*args, **kwargs)
        return output

    def _get_media(self):
        """
        Construct Media as a dynamic property.

        .. Note:: For more information visit
            https://docs.djangoproject.com/en/1.8/topics/forms/media/#media-as-a-dynamic-property
        """
        return forms.Media(
            js=(settings.SELECT2_JS, 'django_select2/django_select2.js'),
            css={'screen': (settings.SELECT2_CSS,)}
        )

    media = property(_get_media)


class wSelect(Select):
    allow_multiple_selected = False

    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        obj.choices = copy.copy(self.choices)
        memo[id(self)] = obj
        return obj

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select style="width: 100%; line-height: 22px;"{}>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

    def render_options(self, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)



class Select3Widget(Select2Mixin, wSelect):
    """
    Select2 drop in widget.

    Example usage::

        class MyModelForm(forms.ModelForm):
            class Meta:
                model = MyModel
                fields = ('my_field', )
                widgets = {
                    'my_field': Select2Widget
                }

    or::

        class MyForm(forms.Form):
            my_choice = forms.ChoiceField(widget=Select2Widget)

    """

    pass

class HeavySelect3Widget(HeavySelect2Mixin, Select3Widget):
    """
    Select2 widget with AJAX support that registers itself to Django's Cache.

    Usage example::

        class MyWidget(HeavySelect2Widget):
            data_view = 'my_view_name'

    or::

        class MyForm(forms.Form):
            my_field = forms.ChoicesField(
                widget=HeavySelect2Widget(
                    data_url='/url/to/json/response'
                )
            )

    """

    pass


class ModelSelect3Widget(ModelSelect2Mixin, HeavySelect3Widget):
    search_fields = [
        'nombre__icontains',
    ]
    """
    Select2 drop in model select widget.

    Example usage::

        class MyWidget(ModelSelect2Widget):
            search_fields = [
                'title__icontains',
            ]

        class MyModelForm(forms.ModelForm):
            class Meta:
                model = MyModel
                fields = ('my_field', )
                widgets = {
                    'my_field': MyWidget,
                }

    or::

        class MyForm(forms.Form):
            my_choice = forms.ChoiceField(
                widget=ModelSelect2Widget(
                    model=MyOtherModel,
                    search_fields=['title__icontains']
                )
            )

    .. tip:: The ModelSelect2(Multiple)Widget will try
        to get the QuerySet from the fields choices.
        Therefore you don't need to define a QuerySet,
        if you just drop in the widget for a ForeignKey field.
    """

    pass


#test