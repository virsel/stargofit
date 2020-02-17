from django import template


register = template.Library()

@register.filter(name='loop_range')
def loop_range(int):
    list = ''
    while int > 0:
        list.append('x')
        int -= 1
    return list


@register.filter(name='is_not_star')
def is_star(stars,count):
    iNumber = 5-stars
    return count <= iNumber

@register.filter(name='is_star')
def is_star(stars,count):
    return count <= stars


