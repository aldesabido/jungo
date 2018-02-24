from django.db import models
from django.contrib.auth import hashers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import JSONField,ArrayField


class User_Manager(BaseUserManager):
	
	def create_user(self, email, password):
		password = hashers.make_password(self.password)
		user = self.model(email = email, password = password)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email = email, password = password)
		user.is_staff = False
		user.is_superuser = True
		user.save()
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length = 254, null = False, blank = False, unique = True)
	fullname = models.CharField(max_length = 50, null = False, blank = False)
	address = models.TextField(null = True,blank = True)
	company = models.CharField(max_length = 250,null = True,blank = True)
	contact_no = models.CharField(max_length = 250,null = True,blank = True)
	is_active = models.BooleanField(default = True)
	created_on = models.DateTimeField(auto_now_add = True)
	edited_on = models.DateTimeField(auto_now = True)
	is_staff = models.BooleanField(default = True)
	is_superuser = models.BooleanField(default = False)
	deleted = models.BooleanField(default = False)
	USERNAME_FIELD = 'email'
	objects = User_Manager()

	class Meta:
		app_label = "project"
		db_table = "User"
		ordering = ["email"]

	def __str__(self):
		return self.fullname

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		if self.password:
			self._old_password = self.password
		else:
			self._old_password = None

	def as_dict(self):
		return {
			"id": self.pk,
			"email": self.email,
			"fullname": self.fullname,
			"user_type": self.user_type.as_dict(),
			"address": self.address,
			"company": self.company,
			"contact_no": self.contact_no,
		}

	def delete(self, hard_delete = False):
		self.deleted = True
		self.save()

	def get_full_name(self): 
		return self.fullname

	def get_short_name(self):
		substrings = this.get_full_name().split(' ')
		if substring[0]:
			return substring[0]
		else:
			return ""

	def get_absolute_url(self):
		return "/user/%s/" % urlquote(self.email)