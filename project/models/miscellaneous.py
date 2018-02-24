from django.db import models
from ..views.common import *


class Instructor(models.Model):
	code = models.TextField(unique = True)
	name = models.TextField()
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "instructors"

	def __str__(self):
		return "%s - %s"%(self.code,self.name)

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {"id": self.pk,"code": self.code,"name": self.name}


class Student(models.Model):
	code = models.TextField(unique = True)
	name = models.TextField()
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "student"

	def __str__(self):
		return "%s - %s"%(self.code,self.name)

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {"id": self.pk,"code": self.code,"name": self.name}


class Subject(models.Model):
	name = models.TextField()
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "subject"

	def __str__(self):
		return self.name

	def delete(self):
		# Validation here...
		self.is_deleted = True
		self.save()

	def as_dict(self):
		return {"id": self.pk,"name": self.name}


