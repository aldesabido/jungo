from django import forms
from ..models.users import *


class Users_create_form(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email','fullname','user_type','address','company','contact_no','password')

class Users_edit_form(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email','fullname','user_type','address','company','contact_no')

class Users_change_password_form(forms.ModelForm):
	class Meta:
		model = User
		fields = ('password',)

class Users_login_form(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email','password')


