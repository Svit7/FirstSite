from django import template
from women.models import *
from women.utils import menu


register = template.Library()

@register.simple_tag(name='getcats') # Simple tag
def get_categories(filter=None):
	if not filter:
		return Category.objects.all()
	else:
		return Category.objects.filter(slug=filter)


@register.inclusion_tag('women/main_menu.html', takes_context=True)
def main_menu(context):
	m = menu.copy()
	if not context['request'].user.is_authenticated:
		m.pop(1)
	else:
		context['menu'] = m
	return context
