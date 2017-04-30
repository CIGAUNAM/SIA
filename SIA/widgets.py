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
                    'value': value,
                }}
        else:
            return {'widget': {
                'name': name,
            }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class wDateField2(DateTimeBaseInput):
    format_key = 'DATE_INPUT_FORMATS'



class wSelectSingle(Select):
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

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}


    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<div class="form-group" style="margin-top: -10px;">'
                                '<div class="input-group">'
                                    '<div class="input-group-addon">'
                                        '<i class="fa fa-calendar"></i>'
                                    '</div>'
                                    '<select{} class="js-placeholder-single" style="width: 100%;>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select>'
                        '<div class="input-group-addon">'
                            '<i class="fa fa-question-circle"></i>'
                        '</div>'
                      '</div>'
                      '</div>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = option_value
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, option_label)


    def render_options(self, selected_choices):
        # Normalize to strings.
        selected_choices = set(v for v in selected_choices)
        output = ['<option></option>\n<option></option>']
        for option_value, option_label in self.choices:
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', option_value))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)



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