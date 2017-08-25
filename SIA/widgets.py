from django.forms.widgets import Select, DateInput, URLInput, Textarea, EmailInput, TextInput, NumberInput, Widget
from django.utils.safestring import mark_safe
import copy
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils import formats, six
from django import forms
from django.conf import settings
from itertools import chain
from django_select2.forms import Select2Mixin, ModelSelect2Mixin, HeavySelect2Mixin, Select2MultipleWidget
from django.utils.datastructures import MultiValueDict
from django.utils.translation import get_language
from django.core import signing
from django.forms.models import ModelChoiceIterator


class wDateInput(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'widgets/wdate.html'

    def format_value(self, value):
        if value is not None:
            return formats.localize_input(value, self.format or formats.get_format(self.format_key)[2])


class wSelect2Mixin(object):
    """
    The base mixin of all Select2 widgets.

    This mixin is responsible for rendering the necessary
    data attributes for select2 as well as adding the static
    form media.
    """

    def build_attrs(self, *args, **kwargs):
        """Add select2 data attributes."""
        attrs = super(wSelect2Mixin, self).build_attrs(*args, **kwargs)
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
        return super(wSelect2Mixin, self).optgroups(name, value, attrs=attrs)

    def render_options(self, *args, **kwargs):
        """Render options including an empty one, if the field is not required."""
        output = '<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else ''
        output += super(wSelect2Mixin, self).render_options(*args, **kwargs)
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
            i18n_file = ('%s/%s.js' % (settings.SELECT2_I18N_PATH, settings.SELECT2_I18N_AVAILABLE_LANGUAGES[i]),)
        except ValueError:
            i18n_file = ()
        return forms.Media(
            js=(settings.SELECT2_JS,) + i18n_file + ('django_select2/django_select2.js',),
            css={'screen': (settings.SELECT2_CSS,)}
        )

    media = property(_get_media)


class wChoiceWidget(Widget):
    allow_multiple_selected = False
    input_type = None
    template_name = None
    option_template_name = None
    add_id_index = True
    checked_attribute = {'checked': True}
    option_inherits_attrs = True

    def __init__(self, attrs=None, choices=()):
        super(wChoiceWidget, self).__init__(attrs)
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

    def subwidgets(self, name, value, attrs=None):
        """
        Yield all "subwidgets" of this widget. Used to enable iterating
        options from a BoundField for choice widgets.
        """
        value = self.format_value(value)
        for option in self.options(name, value, attrs):
            yield option

    def options(self, name, value, attrs=None):
        """Yield a flat list of options for this widgets."""
        for group in self.optgroups(name, value, attrs):
            for option in group[1]:
                yield option


    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        #print(self.choices)
        #for i in self.choices:
        #    print(i)

        for index, (option_value, option_label) in enumerate(chain(self.choices)):
            if option_value is None:
                option_value = ''

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    force_text(subvalue) in value and
                    (has_selected is False or self.allow_multiple_selected)
                )
                if selected is True and has_selected is False:
                    has_selected = True
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                ))
                if subindex is not None:
                    subindex += 1
        return groups


    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }

    def get_context(self, name, value, attrs):
        context = super(wChoiceWidget, self).get_context(name, value, attrs)
        context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)
        context['wrap_label'] = True
        print(context)
        return context

    def id_for_label(self, id_, index='0'):
        """
        Use an incremented id for each option where the main widget
        references the zero index.
        """
        if id_ and self.add_id_index:
            id_ = '%s_%s' % (id_, index)
        return id_

    def value_from_datadict(self, data, files, name):
        getter = data.get
        if self.allow_multiple_selected:
            try:
                getter = data.getlist
            except AttributeError:
                pass
        return getter(name)

    def format_value(self, value):
        """Return selected values as a list."""
        if not isinstance(value, (tuple, list)):
            value = [value]
        return [force_text(v) if v is not None else '' for v in value]



class wSortedSelect(wChoiceWidget):
    input_type = 'select'
    template_name = 'widgets/w_select.html'
    option_template_name = 'widgets/w_select_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False

    def get_context(self, name, value, attrs):
        context = super(wSortedSelect, self).get_context(name, value, attrs)
        if self.allow_multiple_selected:
            context['widget']['attrs']['multiple'] = 'multiple'
        return context

    @staticmethod
    def _choice_has_empty_value(choice):
        """Return True if the choice's value is empty string or None."""
        value, _ = choice
        return (
            (isinstance(value, six.string_types) and not bool(value)) or
            value is None
        )

    def use_required_attribute(self, initial):
        """
        Don't render 'required' if the first <option> has a value, as that's
        invalid HTML.
        """
        use_required_attribute = super(wSortedSelect, self).use_required_attribute(initial)
        # 'required' is always okay for <select multiple>.
        if self.allow_multiple_selected:
            return use_required_attribute

        first_choice = next(iter(self.choices), None)
        return use_required_attribute and first_choice is not None and self._choice_has_empty_value(first_choice)


class wSelectMultiple(wSortedSelect):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return False


class wSortedSelect2MultipleWidget(wSelect2Mixin, wSelectMultiple):
    """
    Select2 drop in widget for multiple select.

    Works just like :class:`.Select2Widget` but for multi select.
    """

    pass


'''
    def render_options2(self, *args, **kwargs):
        """Render options including an empty one, if the field is not required."""
        output = '<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else ''
        output += super(Select2Mixin, self).render_options(*args, **kwargs)
        output = [2,1,5,3,4]
        return output

    def render_options12(self, *args):
        """Render only selected options and set QuerySet from :class:`ModelChoiceIterator`."""

        try:
            selected_choices, = args
            print(selected_choices)
        except ValueError:
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {force_text(v) for v in selected_choices}
        output = ['<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else '']
        if isinstance(self.choices, ModelChoiceIterator):
            if self.queryset is None:
                self.queryset = self.choices.queryset
            selected_choices = {c for c in selected_choices
                                if c not in self.choices.field.empty_values}
            choices = [(obj.pk, self.label_from_instance(obj))
                       for obj in self.choices.queryset.filter(pk__in=selected_choices)]
        else:
            choices = [(k, v) for k, v in choices if force_text(k) in selected_choices]
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def render_options1(self, selected_choices):
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
'''
