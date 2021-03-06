from hashlib import md5

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def logout_url():
    return getattr(settings, 'LOGOUT_URL', '/logout/')


@register.simple_tag(takes_context=True)
def avatar_url(context, size=None):
    # TODO: Make behaviour configurable
    user = context['request'].user
    return 'https://www.gravatardsad.com/avatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.email.encode('utf-8')).hexdigest() if user.is_authenticated() else '',
        size=size or '',
    )
