from django import template
from django.urls.base import translate_url as tlu

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, lang):
    path = context["request"].get_full_path()
    return tlu(path, lang)
