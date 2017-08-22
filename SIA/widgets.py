from django.forms.widgets import Select, DateInput, URLInput, Textarea, EmailInput, TextInput, NumberInput
from django.utils.safestring import mark_safe
import copy
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils import formats, six
from django import forms
from django.conf import settings
from itertools import chain
from django_select2.forms import Select2Mixin, ModelSelect2Mixin, HeavySelect2Mixin
from django.utils.datastructures import MultiValueDict
from django.utils.translation import get_language
from django.core import signing



class wDateInput(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'widgets/wdate.html'

    def format_value(self, value):
        if value is not None:
            return formats.localize_input(value, self.format or formats.get_format(self.format_key)[2])






class wOrderedSelect(Select, TextInput):
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
        final_attrs = self.build_attrs(attrs)
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
        selected_choices = [force_text(v) for v in selected_choices]
        output = []

        for i in selected_choices:
            for option_value, option_label in self.choices:
                if str(option_value) == i:
                    if isinstance(option_label, (list, tuple)):
                        output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                        for option in option_label:
                            output.append(self.render_option(selected_choices, *option))
                        output.append('</optgroup>')
                    else:
                        output.append(self.render_option(selected_choices, option_value, option_label))

        for option_value, option_label in self.choices:
            if str(option_value) not in selected_choices:
                if isinstance(option_label, (list, tuple)):
                    output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                    for option in option_label:
                        output.append(self.render_option(selected_choices, *option))
                    output.append('</optgroup>')
                else:
                    output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)











class wOrderedSelectMultiple(wOrderedSelect):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs)
        output = [format_html('<select style="width: 100%; line-height: 22px;" multiple="multiple"{}>', flatatt(final_attrs))]
        options = self.render_options(value)

        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return False




class Select3MultipleWidgetOrdered(Select2Mixin, wOrderedSelectMultiple):
    """
    Select2 drop in widget for multiple select.

    Works just like :class:`.Select2Widget` but for multi select.
    """

    pass




