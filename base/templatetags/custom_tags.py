import datetime

from django import template
from django.forms import CheckboxInput
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

# Custom tag para verificar se field é checkbox
@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter(is_safe=True)
def as_required(field):
    return 'required' if field.field.required else ''

# Custom tag para calcular a idade em anos
@register.filter
def age_year(birthday):
    today = datetime.date.today()
    year = today.year - birthday.year

    if today.month < birthday.month:
        year = year - 1
    elif today.month == birthday.month and today.day < birthday.day:
        year = year - 1
        
    return year

@register.filter
@stringfilter
def sigla_nome(name):
    nomes = name.split()
    if len(nomes) == 0:
        return ''
    elif len(nomes) == 1:
        return nomes[0][0]
    else:
        return nomes[0][0]+nomes[-1][0]

@register.filter
@stringfilter
def title_name(name):
    title = name.title()
    lst = title.split(' ')
    if len(lst) > 2:
        l = []
        l.append(lst[0])
        for s in lst[1:-1]:
            if len(s) < 4:
                l.append(s.lower())
            else:
                l.append(s)
        l.append(lst[-1])
        title = ' '.join(l)
    
    return title
