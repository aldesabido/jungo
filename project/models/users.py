from django.db import models
from django.contrib.auth import hashers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import JSONField,ArrayField


class User_Manager(BaseUserManager):
	
	def create_user(self, email, password):
		user = self.model(email = email, password = password)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email = email, password = password)
		super_admin_role = Role.objects.get(name = 'Admin')
		user.add(super_admin_role, level = 1)
		user.save()
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length = 254, null = False, blank = False, unique = True)
	fullname = models.CharField(max_length = 50, null = False, blank = False)
	user_type = models.ForeignKey("User_type")
	address = models.TextField(null = True,blank = True)
	company = models.CharField(max_length = 250,null = True,blank = True)
	contact_no = models.CharField(max_length = 250,null = True,blank = True)
	is_active = models.BooleanField(default = True)
	created_on = models.DateTimeField(auto_now_add = True)
	edited_on = models.DateTimeField(auto_now = True)
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

	def save(self, *args, **kwargs):
		if self._old_password is None or self._old_password != self.password:
			if "pbkdf2_sha256" not in self.password:
				self.password = hashers.make_password(self.password)

		super(User, self).save(*args, **kwargs)

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
		return "/User/%s/" % urlquote(self.email)


	'''
		Only available to Client	
		Returns all orders unpaid

			return amount : instead of returning all orders, it will return total_amount
		
	'''
	def get_unpaid(self,filters = {},return_amount = False):
		pass


	'''
		Only available to Admin and CDA	
		Returns all orders unpaid
			return amount : instead of returning all orders, it will return total_amount
		
	'''
	def get_receivable(self,filters = {},return_amount = False):
		pass


	'''
		Only available to Admin
		return the net income
		
	'''
	def get_net(self,filters = {},return_amount = False):
		pass

	
class User_type(models.Model):
	code = models.CharField(max_length=200)
	name = models.CharField(max_length=200)

	class Meta:
		app_label = "project"
		db_table  = "user_type"

	def __str__(self):
		return self.name

	def as_dict(self):
		return {"id": self.id,"code": self.code,"name": self.name}

