from django.forms.widgets import Widget, Select, Input, DateTimeBaseInput, DateInput, URLInput, Textarea, EmailInput, TextInput, NumberInput
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
from django.utils.datastructures import MultiValueDict
from django.utils.translation import get_language



class wTextInput(TextInput):
    input_type = 'text'
    template_name = 'widgets/wtext.html'

class wPasswordInput(wTextInput):
    input_type = 'password'
    template_name = 'widgets/wtext.html'

class wURLInput(URLInput):
    input_type = 'url'
    template_name = 'widgets/wtext.html'

class wEmailInput(EmailInput):
    input_type = 'email'
    template_name = 'widgets/wtext.html'

class wNumberInput(NumberInput):
    input_type = 'number'
    template_name = 'widgets/wtext.html'

class wNoNegativeNumberField(wNumberInput):
    template_name = 'widgets/NoNegativeNumberField.html'

class wTextarea(Textarea):
    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        return format_html('<div class="form-group" style="margin-top: -10px;"><textarea class="form-control" rows="3" {}>\r\n{}</textarea></div>', flatatt(final_attrs), force_text(value))


class wDateField(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'widgets/wdate.html'

    def format_value(self, value):
        if value is not None:
            return formats.localize_input(value, self.format or formats.get_format(self.format_key)[2])





class Select3Mixin(Select2Mixin):
    """
    The base mixin of all Select2 widgets.

    This mixin is responsible for rendering the necessary
    data attributes for select22222 as well as adding the static
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
        try:
            # get_language() will always return a lower case language code, where some files are named upper case.
            i = [x.lower() for x in settings.SELECT2_I18N_AVAILABLE_LANGUAGES].index(get_language())
            i18n_file = ('%s/%s.js' % (settings.SELECT2_I18N_PATH, settings.SELECT2_I18N_AVAILABLE_LANGUAGES[i]), )
        except ValueError:
            i18n_file = ()
        return forms.Media(
            js=(settings.SELECT2_JS,) + i18n_file + ('django_select2/django_select2.js',),
            css={'screen': (settings.SELECT2_CSS,)}
        )

    media = property(_get_media)


class wSelect(Select):
    input_type = 'select'
    template_name = 'widgets/wselect.html'
    option_template_name = 'django/forms/widgets/select_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False




class wSelect1(Select, TextInput):
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


class wSelectMultiple(wSelect):
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


class Select3MultipleWidget(Select2Mixin, wSelectMultiple):
    """
    Select2 drop in widget for multiple select.

    Works just like :class:`.Select2Widget` but for multi select.
    """

    pass


class Select3MultipleWidgetOrdered(Select2Mixin, wOrderedSelectMultiple):
    """
    Select2 drop in widget for multiple select.

    Works just like :class:`.Select2Widget` but for multi select.
    """

    pass


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


class ModelSelect3Widget(ModelSelect2Widget, HeavySelect3Widget):
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




"""
class wTextInput(Widget):
    input_type = 'text'  # Subclasses must define this.

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<input{} class="form-control pull-right"/>', flatatt(final_attrs))


class wTextInput(TextInput):
    input_type = 'text'
    template_name = 'django/forms/widgets/text.html'
"""

"""
class wUrlField1(URLInput):
    input_type = 'url'

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<input{} class="form-control pull-right"/>', flatatt(final_attrs))
"""

"""
class wEmailField1(EmailInput):
    input_type = 'email'

    def format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<input{} class="form-control pull-right"/>', flatatt(final_attrs))
"""

"""
class wNumberField1(Widget):
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
"""

"""
class wTextarea1(Widget):
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
"""


"""
class Textarea11(Widget):
    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html('<textarea{}>\r\n{}</textarea>', flatatt(final_attrs), force_text(value))
"""

"""
class wDateField1(DateInput):
    template_name = 'widgets/DateField.html'
    format_key = 'DATE_INPUT_FORMATS'
    format = None

    def get_context(self, name, value, attrs=None):

        if value:
            tfecha = str(formats.localize_input(value, formats.get_format(self.format_key)[0]))
            try:
                tfecha = tfecha.split("/")
                fecha = str(tfecha[2]) + "-" + str(tfecha[1]) + "-" + str(tfecha[0])
                fecha = "la fecha aqui"
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

    def format_value(self, value):
        return formats.localize_input(value, self.format or formats.get_format(self.format_key)[2])

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))

        return format_html('<input{} style="padding-left: 18px"; data-provide="datepicker" class="datepicker form-control pull-right"/>', flatatt(final_attrs))
"""