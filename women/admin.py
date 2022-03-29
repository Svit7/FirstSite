from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import *


class WomenAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'time_create', 'get_html_photo', 'is_published')
	list_display_links = ('id', 'name')
	list_editable = ('is_published',)
	list_filter = ('is_published', 'time_create')
	search_fields = ('name', 'content')
	prepopulated_fields = {'slug': ('name',)}
	fields = ('name', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
	readonly_fields = ('time_create', 'time_update', 'get_html_photo')
	save_on_top = True

	def get_html_photo(self, object):
		if object.photo:
			return mark_safe(f"<img src='{object.photo.url}' width=50>")

	get_html_photo.short_description = 'Photo'


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_display_links = ('id', 'name')
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}


class ContactAdmin(admin.ModelAdmin):
	list_display = ('author', 'email', 'time_create')


# class CommentAdmin(admin.ModelAdmin):
# 	list_display = ('time_create', 'author',)
# 	search_fields = ('text',)
# 	list_filter = ('author',)
# 	date_hierarchy = 'time_create'


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, MPTTModelAdmin)
admin.site.register(Contact, ContactAdmin)

admin.site.site_title = 'OVERLORD panel '
admin.site.site_header = 'OVERLORD panel '
