from django.db import models
from django.db.models import Count, Sum, Avg,Min,Q,F,Func


class Order_type(models.Model):
	name = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "order_type"

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {"id": self.pk,"name": self.name}

class Status(models.Model):
	name = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "status"

	def as_dict(self):
		return {"id": self.pk,"name": self.name}


class Company(models.Model):
	name = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "company"

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {"id": self.pk,"name": self.name}

class Credential(models.Model):
	user = models.ForeignKey("User")
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	company = models.ForeignKey("Company")
	is_deleted = models.BooleanField(default = False)
	remarks = models.TextField(null = True,blank = True)

	class Meta:
		app_label = "project"
		db_table  = "credential"

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {
			"id": self.pk,
			"username": self.username,
			"password": self.password,
			"company": self.company.as_dict(),
			"remarks": self.remarks,
		}
