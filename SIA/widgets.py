from django.forms.widgets import Select, DateInput, URLInput, Textarea, EmailInput, TextInput, NumberInput, Widget
from django.utils.encoding import force_text
from django.utils import formats, six
from django import forms
from django.conf import settings
from itertools import chain
from django_select2.forms import Select2Mixin
from django.forms.widgets import ChoiceWidget

class wDateInput(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'widgets/wdate.html'

    def format_value(self, value):
        if value is not None:
            return formats.localize_input(value, self.format or formats.get_format(self.format_key)[3])



class dialogDateInput(DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'widgets/wdate.html'

    def format_value(self, value):
        if value is not None:
            return formats.localize_input(value, self.format or formats.get_format(self.format_key)[1])


class wSortedChoiceWidget(ChoiceWidget):
    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        id_value = []
        if value == ['']:
            value = []
        for i in value:
            #if i != '':
            #    id_value.append(int(i))
            id_value.append(int(i))
        sorted_choices = []

        for i in id_value:
            for j in chain(self.choices):
                if i == j[0]:
                    sorted_choices.append(j)

        for i in chain(self.choices):
            if i not in sorted_choices:
                sorted_choices.append(i)

        for index, (option_value, option_label) in enumerate(chain(sorted_choices)):
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




class wSortedSelect(wSortedChoiceWidget):
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


class wSortedSelectMultiple(wSortedSelect):
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


class wSortedSelect2MultipleWidget(Select2Mixin, wSortedSelectMultiple):
    """
    Select2 drop in widget for multiple select.

    Works just like :class:`.Select2Widget` but for multi select.
    """

    pass

