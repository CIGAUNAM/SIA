from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


class MyWidget(Widget):
    template_name = 'my_widget.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)