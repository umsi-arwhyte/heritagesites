from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='add_leading_comma')
@stringfilter
def add_leading_comma(value):
	return ''.join([', ', value])


@register.filter(name='add_trailing_comma')
@stringfilter
def add_trailing_comma(value):
	return ''.join([value, ','])


@register.filter(name='add_parens')
@stringfilter
def add_parentheses(value):
	return ''.join(['(', value, ')'])
