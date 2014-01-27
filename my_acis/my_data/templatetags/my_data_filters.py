#some custom filters for dictionary lookup.
#from django.template.defaultfilters import register

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='lookup')
def lookup(list_or_dict, index):
    try:
        return list_or_dict[index]
    except:
        return ''

'''
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''
'''

@register.filter(name='greater_than')
def greater_than(a, b):
    return a > b

@register.filter(name='g_e')
def greater_than(a, b):
    return a >= b

@register.filter(name='less_than')
def less_than(a, b):
    return a < b

@register.filter(name='l_e')
def less_than(a, b):
    return a <= b


@register.filter(name='get_id')
@stringfilter
def get_id(tbl_instance):
    return tbl_instance.split("_")[-1]

@register.filter(name='in_double_quotes')
@stringfilter
def in_double_quotes(d_name):
    return "%s" % d_name

@register.filter(name='in_single_quotes')
@stringfilter
def in_single_quotes(d_name):
    return '%s' % d_name

@register.filter(name='is_false')
def is_false(arg):
    return arg is False

@register.filter(name='is_true')
def is_true(arg):
    return arg is True

@register.filter(name='string_sub')
@stringfilter
def string_sub(arg):
    return '%s' % arg
