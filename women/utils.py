from django.contrib import messages
from django.db.models import Count
from django.core.cache import cache
from django.shortcuts import redirect

from .models import *


menu = [
		{'title': "About us", 'url_name': 'about'},
		{'title': "New post", 'url_name': 'add_page'},
		{'title': "Contact", 'url_name': 'contact'},
]


class DataMixin:
	paginate_by = 4

	def get_user_context(self, **kwargs):
		context = kwargs
		# cats = cache.get('cats')
		# if not cats:
		# 	cats = Category.objects.annotate(Count('women'))
		# 	cache.set('cats', cats, 60)
		cats = Category.objects.annotate(Count('women'))

		user_menu = menu.copy()
		if not self.request.user.is_authenticated:
			user_menu.pop(1)

		context['menu'] = user_menu
		context['cats'] = cats

		if 'cat_selected' not in context:
			context['cat_selected'] = 0
		return context


class CustomSuccessMessageMixin:
	@property
	def success_msg(self):
		return False

	def form_valid(self, form):
		messages.success(self.request, self.success_msg)
		return super().form_valid(form)

	def get_success_url(self):
		return '%s?id=%s' % (self.success_url, self.object.slug)


class ValidFormMixin:
	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			form = self.get_form()
			print(request.user.is_authenticated) # TODO
			if form.is_valid():
				print(form) # TODO
				return self.form_valid(form)
			else:
				print(form) # TODO
				return self.form_invalid(form)
		elif not request.user.is_authenticated:
			return redirect('login')
		else:
			raise Exception

	def form_valid(self, form):
		try:
			self.object = form.save(commit=False)
			self.object.author = self.request.user
			self.object.save()
			return super().form_valid(form)
		except Exception:
			raise print(Exception)
