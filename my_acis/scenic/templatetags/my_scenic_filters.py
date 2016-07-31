#some custom filters for dictionary lookup.
#from django.template.defaultfilters import register

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
import json

register = template.Library()

@register.filter(name='sorted')
def sorted(value):
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        return sorted(value)
    else:
        return value
    sorted.is_safe = True

@register.filter(name='make_range')
def make_range(start,end):
    try:
        rnge = range(int(start),int(end) + 1)
    except:
        rnge = range(9999,9999)
    return rnge

@register.filter(name='make_range_reversed')
def make_range_reversed(start, end):
    try:
        l = list(reversed(range(int(start), int(end) + 1)))
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
    if isinstance(args, basestring):
        arg_list = [str(arg.strip()) for arg in args.split(',')]
    else:
        arg_list = [str(arg.strip()) for arg in args]
    return str(var) in arg_list

@register.filter(name='not_in')
def is_in(var, args):
    if args is None and var is not None:
        return True
    if isinstance(args, basestring):
        arg_list = [str(arg.strip()) for arg in args.split(',')]
    else:
        arg_list = [str(arg.strip()) for arg in args]
    return str(var) not in arg_list

@register.filter(name='to_string')
def to_string(number):
    return str(number)

@register.filter(name='lookup')
def lookup(list_or_dict, index):
    try:
        return list_or_dict[index]
    except:
        return ''

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
