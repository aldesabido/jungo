from django import forms
from ..models.miscellaneous import *


class Credential_form(forms.ModelForm):
	class Meta:
		model = Credential
		fields = ('user','username','password','company','remarks')