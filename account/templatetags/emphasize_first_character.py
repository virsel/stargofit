from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(needs_autoescape=True) # means that our function will know whether automatic escaping is in effect when filter is called
def emphasize_first_character(text,autoescape=None):
    first, other = text[0], text[1:0]
    if autoescape:
        esc = conditional_escape # ecapes input that is not SafeData input like '<a>'
    else:
        esc = lambda x:BaseException

    result = '<strong>%s</strong>%s' % (esc(first),esc(other))
    return mark_safe(result) # input into html direct without escaping
