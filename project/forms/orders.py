from django import forms
from ..models.orders import *


class Order_create_form(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('client','order_number','address','order_type','credential','is_rush','is_rental',)

class Order_assignment_history_form(forms.ModelForm):
	class Meta:
		model = Order_assignment_history
		fields = ('order','assigned_by','assignee')

class Order_status_history_form(forms.ModelForm):
	class Meta:
		model = Order_status_history
		fields = ('order','status','changed_by')

class Order_note_form(forms.ModelForm):
	class Meta:
		model = Order_note
		fields = ('order','note','created_by')

class Order_photo_form(forms.ModelForm):
	class Meta:
		model = Order_photo
		fields = ('order','filename','photo','photo_thumb','created_by')

class Order_document_form(forms.ModelForm):
	class Meta:
		model = Order_document
		fields = ('order','filename','filelocation','created_by')

