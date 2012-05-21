#some custom filters for dictionary lookup.
from django.template.defaultfilters import register

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

@register.filter(name='in_double_quotes')
def in_double_quotes(d_name):
    return "%s" % d_name

@register.filter(name='in_single_quotes')
def in_single_quotes(d_name):
    return '%s' % d_name
