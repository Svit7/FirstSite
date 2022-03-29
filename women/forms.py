from django import forms
from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from captcha.fields import CaptchaField
from django.forms import Textarea
from mptt.forms import TreeNodeChoiceField

from .models import *


class AddPostForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['cat'].empty_label = "Category not selected"

	class Meta:
		model = Women
		fields = ['name', 'slug', 'content', 'photo', 'cat']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-input'}),
			'content': forms.Textarea(attrs={'cols': 68, 'rows': 10}),
		}

	def clean_title(self):
		name = self.cleaned_data['name']
		if len(name) > 200:
			raise ValidationError('Length exceeds 200 characters')
		return name


class RegisterUserForm(UserCreationForm):
	username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	password2 = forms.CharField(label='Password repeat', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
	username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = ('name', 'email', 'content')
		widgets = {
			'content': Textarea(
				attrs={
					'placeholder': 'Write your message here'
				}
			)
		}


class CommentForm(forms.ModelForm):
	parent = TreeNodeChoiceField(queryset=Comments.objects.all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['parent'].widget.attrs.update(
			{'class': 'd-none'})
		self.fields['parent'].label = ''
		self.fields['parent'].required = False

	class Meta:
		model = Comments
		fields = ('text', 'parent')

		widgets = {
			'text': forms.Textarea(attrs={'class': 'form-control'}),
		}

	# def save(self, *args, **kwargs):
	# 	Comments.objects.rebuild()
	# 	return super(CommentForm, self).save(*args, **kwargs)
