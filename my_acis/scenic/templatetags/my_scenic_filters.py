#some custom filters for dictionary lookup.
#from django.template.defaultfilters import register

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter(name='make_range')
def make_range(start, end):
    return range(int(start),int(end))

@register.filter(name='make_range_reversed')
def make_range_reversed(start, end):
    try:
        l = list(reversed(range(int(start), int(end))))
    except:
        l = []
    return l

@register.filter(name='to_int')
def to_int(string):
    try:
        integer = int(string)
    except:
        integer = None
    return integer

@register.filter(name='is_in')
def is_in(var, args):
    if args is None:
        return False
    arg_list = [str(arg.strip()) for arg in args.split(',')]
    return str(var) in arg_list

@register.filter(name='to_string')
def to_string(number):
    return str(number)

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
@register.filter(is_safe=True)
def safe_json(obj):
    return mark_safe(json.dumps(obj))


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
