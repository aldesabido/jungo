from django.db import models
from ..views.common import *
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

class Order_note(models.Model):
	order = models.ForeignKey("Order")
	note = models.TextField()
	created_by = models.ForeignKey("User",related_name = "note_changed_by")
	created_at = models.DateTimeField(auto_now_add = True)
	is_deleted = models.BooleanField(default = False)
	# edited_by = models.ForeignKey("User",related_name = "note_edited_by", null = True, blank= True)
	# last_modified = models.DateTimeField(auto_now = True)

	class Meta:
		app_label = "project"
		db_table  = "order_notes"

	def display_dict(self):
		row = {
			"id" : self.pk,
			"note" : self.note,
			"date" : self.created_at,
			"user_id" : self.created_by.pk,
			"user" : self.created_by.fullname,
		}

		print(self.note)

		return row

	def as_dict(self,include_order_dict = False):
		row = {
			"id" : self.pk,
			"note" : self.note,
			"order" : self.order.pk,
			"created_by":self.created_by.as_dict(),
			"created_at":self.created_at,
		}

		if include_order_dict:
			row["order"] = self.order.as_dict(),

		return row


class Order_photo(models.Model):
	order = models.ForeignKey("Order")
	filename = models.CharField(max_length=200,blank=True,null=True)
	photo = ProcessedImageField(upload_to = "orders/photos/",
								blank = True,
								null = True,
								processors = [ResizeToFit(600, 600)],
								format = 'JPEG',
								options = {'quality': 80})
	photo_thumb = ProcessedImageField(upload_to = "orders/photos/thumbs/",
											blank = True,
											null = True,
											processors = [ResizeToFit(150, 80)],
											format = 'JPEG',
											options = {'quality': 70})

	created_by = models.ForeignKey("User",related_name = "photo_created_by")
	created_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		app_label = "project"
		db_table  = "order_photos"

	def as_dict(self,include_order_dict = False):
		row = model_to_dict(self, fields = ["id","order","filename","photo","photo_thumb"])
		row["photo"] = str(row["photo"])
		row["photo_thumb"] = str(row["photo_thumb"])
		row["created_by"] = self.created_by.fullname
		row["url"] = self.get_url()

		if include_order_dict:
			row["order"] = self.order.as_dict(),
			row["created_by"] = self.created_by.as_dict()

		return row

	def get_url(self):
		return settings.MEDIA_ROOT+"/"+str(self.photo)



class Order_document(models.Model):
	order = models.ForeignKey("Order")
	filename = models.CharField(max_length=200,blank=True,null=True)
	filelocation		= models.FileField(upload_to = "orders/documents/")
	created_by = models.ForeignKey("User",related_name = "docs_created_by")
	created_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		app_label = 'project'
		db_table = "order_document"

	def as_dict(self,include_order_dict = False):
		row = model_to_dict(self, fields = ["id","order","filename","filelocation"])
		row["filelocation"] = str(row["filelocation"])
		row["created_by"] = self.created_by.fullname
		row["url"] = self.get_url()

		if include_order_dict:
			row["order"] = self.order.as_dict(),
			row["created_by"] = self.created_by.as_dict()

		return row

	def get_url(self):
		return settings.MEDIA_ROOT+"/"+str(self.filelocation)




class Order_qc(models.Model):
	order = models.ForeignKey("Order")
	note = models.TextField()
	created_by = models.ForeignKey("User",related_name = "qc_changed_by")
	edited_by = models.ForeignKey("User",related_name = "qc_edited_by")
	created_at = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "order_qcs"

	def as_dict(self,include_order_dict = False):
		row = {
			"id" : self.pk,
			"note" : self.note,
			"order" : self.order.pk,
			"created_by":self.changed_by.as_dict(),
			"created_at":self.created_at,
		}

		if include_order_dict:
			row["order"] = self.order.as_dict(),

		return row

class Order_hold(models.Model):
	order = models.ForeignKey("Order")
	note = models.TextField()
	created_by = models.ForeignKey("User",related_name = "hold_changed_by")
	edited_by = models.ForeignKey("User",related_name = "hold_edited_by")
	created_at = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "order_holds"

	def as_dict(self,include_order_dict = False):
		row = {
			"id" : self.pk,
			"note" : self.note,
			"order" : self.order.pk,
			"created_by":self.changed_by.as_dict(),
			"created_at":self.created_at,
		}

		if include_order_dict:
			row["order"] = self.order.as_dict(),

		return row

#Remove this in the future
class Order_attachment(models.Model):
	order = models.ForeignKey("Order")
	attachment = models.TextField()
	created_by = models.ForeignKey("User",related_name = "attachment_changed_by")
	created_at = models.DateTimeField(auto_now_add = True)
	is_deleted = models.BooleanField(default = False)

	class Meta:
		app_label = "project"
		db_table  = "order_attachments"

	def as_dict(self,include_order_dict = False):
		row = {
			"id" : self.pk,
			"attachment" : self.attachment,
			"order" : self.order.pk,
			"created_by":self.changed_by.as_dict(),
			"created_at":self.created_at,
		}

		if include_order_dict:
			row["order"] = self.order.as_dict(),

		return row