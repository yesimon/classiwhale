from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return "active"
    return ""


@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
url_target_blank.is_safe = True

