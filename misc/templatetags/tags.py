from django import template
import re

register = template.Library()
@register.simple_tag
def current(request, pattern):
    if re.search(pattern, request.path):
        return 'current'
    return ''

@register.simple_tag
def active_tag(request, tag_name):
	pattern = '/'+tag_name+'/?$'
	if re.search(pattern, request.path):
		return 'active'
	return ''