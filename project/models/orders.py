from django.db import models
from ..views.common import *
from ..models.orders_misc import *


'''
	Status:
		Active
			Hold
			Assigned
		Completed
			QC
			Submitted
			Assigned
		Cancelled			
			Assigned
'''

class Order(models.Model):
	client = models.ForeignKey("User",related_name = "Own_by")
	order_number = models.CharField(max_length=200)
	date = models.DateTimeField(default=timezone.now)
	address = models.TextField()
	credential = models.ForeignKey("Credential")
	order_type = models.ForeignKey("Order_type")
	assigned = models.BooleanField(default = False)
	current_assignee = models.ForeignKey("User",related_name = "Current_assignee", null = True)
	time_remaining = models.IntegerField(null = True)
	status = models.CharField(max_length=200)
	is_hold = models.BooleanField(default = False)
	is_qc = models.BooleanField(default = False)
	is_submit = models.BooleanField(default = False)
	is_rush = models.BooleanField(default = False)
	is_rental = models.BooleanField(default = False)
	notes_count = models.IntegerField(null = True,blank = True)
	docs_count = models.IntegerField(null = True,blank = True)
	photos_count = models.IntegerField(null = True,blank = True)
	paid = models.BooleanField(default = False)
	is_deleted = models.BooleanField(default = False)
	last_modified = models.DateTimeField(auto_now = True)

	class Meta:
		app_label = "project"
		db_table  = "orders"
		unique_together = ('client', 'order_number')

	def __str__(self):
		return self.order_number


	def delete(self,hard_delete = False):
		if hard_delete:
			super(Order, self).delete()
		else:
			self.is_deleted = True
			self.order_number += "__"+str(time.time())
			self.save()

	def filename(self,prefix = None):
		filename = self.order_number
		if prefix:
			filename = prefix+" - "+self.order_number
		return filename

	def save(self):
		super(Order, self).save()
		self.update_time()
		

	def update_time(self):
		hours_used = float((timezone.now() - self.date).total_seconds() / 3600)
		total_hours = 24
		if self.is_rush:
			total_hours = 6
		total_hours = float(total_hours)
		time_remaining = total_hours - hours_used

		if time_remaining < 0:
			time_remaining = 0

		self.time_remaining = time_remaining
		super(Order, self).save()




	def as_dict(self,for_display = False):
		if not self.time_remaining:
			self.update_time()

		row = model_to_dict(self)

		if for_display:
			row["client"] = self.client.get_full_name()
			row["company"] = self.credential.company.name
			row["credential"] = self.credential.as_dict()
			row["order_type"] = self.order_type.name
			row["current_assignee"] = self.current_assignee.get_full_name() if self.current_assignee else None
		else:
			row["client"] = self.client.as_dict()
			row["company"] = self.credential.company.as_dict()
			row["credential"] = self.credential.as_dict()
			row["order_type"] = self.order_type.as_dict()
			row["current_assignee"] = self.current_assignee.as_dict() if self.current_assignee else None

		row["date"] = self.date.date()
		return row


	def update_status(self):
		last_status = self.get_status_history(True)
		self.status = last_status
		self.save()

	'''
		Returns all connected from this order
			Status history
			Credentials
			Assignment history
			...

	'''
	def get_details(self,status_history = True,assignment_history = True):
		status_histories = self.get_status_history()
		assignment_histories = self.get_assignment_histories(return_instances = False)

		return status_histories,assignment_histories





	'''
		Return status history or return last status only.
	'''
	def get_status_history(self,return_last = False,return_instances = False):
		order_Status_histories = Order_status_history.objects.filter(order = self.pk).order_by("id")
		if return_last:
			order_Status_histories = order_Status_histories.last()
			return order_Status_histories.status

		if return_instances:
			return order_Status_histories
		else:
			histories = []
			for history in order_Status_histories:
				print(history)
				histories.append(history.as_dict())

			return histories


	def get_assignment_histories(self,return_last = False,return_instances = True):
		records = Order_assignment_history.objects.filter(order = self.pk).order_by("date","id")
		if return_instances:
			return records
		else:
			results = []
			for record in records:
				results.append(record.as_dict())
			return results

	def get_photos(self):
		photos = Order_photo.objects.filter(order = self.pk).order_by("id")
		rows = []

		for photo in photos:
			rows.append(photo.as_dict())

		return rows

	def get_docs(self):
		documents = Order_document.objects.filter(order = self.pk).order_by("id")
		rows = []

		for document in documents:
			rows.append(document.as_dict())

		return rows

	def qc_status(self):
		pass

	def count_qc(self):
		return 0

	def count_notes(self):
		return Order_note.objects.filter(order = self.pk).count()

	def count_docs(self):
		return Order_document.objects.filter(order = self.pk).count()

	def count_photos(self):
		return Order_photo.objects.filter(order = self.pk).count()


	def get_time_remaining(self):
		pass

class Order_assignment_history(models.Model):
	order = models.ForeignKey("Order")
	assigned_by = models.ForeignKey("User",related_name = "Assigned_by")
	assignee = models.ForeignKey("User",related_name = "Assignee")
	date = models.DateTimeField(auto_now_add = True)
	remarks = models.TextField()

	class Meta:
		app_label = "project"
		db_table  = "order_assignment_history"

	def as_dict(self):
		row = {
			"id" : self.pk,
			"order" : self.order.as_dict(),
			"assigned_by" : self.assigned_by.as_dict(),
			"assignee" : self.assignee.as_dict(),
			"date":self.date,
			"remarks":self.remarks,
		}
		return row

class Order_status_history(models.Model):
	order = models.ForeignKey("Order")
	status = models.CharField(max_length = 200)
	changed_by = models.ForeignKey("User",related_name = "Status_changed_by")
	date = models.DateTimeField(auto_now_add = True)

	class Meta:
		app_label = "project"
		db_table  = "order_status_history"

	def as_dict(self):
		row = {
			"id" : self.pk,
			"order" : self.order.as_dict(),
			"status":self.status,
			"changed_by":self.changed_by.as_dict(),
			"date":self.date,
		}
		return row