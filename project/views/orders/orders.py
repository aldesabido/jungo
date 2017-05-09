from ...forms.orders import *
from ...models.orders import *
from ...models.orders_misc import *
from ...views.common import *

def orders(request):
	return render(request, 'orders/orders.html',{"page_name": "Orders"})

def order_status_history_dialog(request):
	return render(request, 'orders/dialogs/order_status_history.html')

def order_assignment_dialog(request):
	return render(request, 'orders/dialogs/order_assignment.html')

def order_assignment_history_dialog(request):
	return render(request, 'orders/dialogs/order_assignment_history.html')

def order_details_dialog(request):
	return render(request, 'orders/dialogs/order_details_dialog.html')

def get_reference_no(user_id):
	order_number = str(user_id)
	if len(order_number) < 3:
		order_number = order_number.rjust(3,'0')

	orig_order_count = Order.objects.filter(client = user_id).count()

	order_count = str(orig_order_count + 1)
	if len(order_count) < 4:
		order_count = order_count.rjust(4,'0')

	order_number += order_count
	return order_number

def create_dialog(request,pid = None):
	dictt = {}
	user_type = request.user.user_type
	if not pid and user_type.code == "client":
		order_number = get_reference_no(request.user.id)
		dictt["order_number"] = str(order_number)

	return render(request, 'orders/dialogs/create_dialog.html',dictt)

def credential_dialog(request):
	return render(request, 'orders/dialogs/credential_dialog.html')


def notes_dialog(request):
	return render(request, 'orders/dialogs/notes_dialog.html')

def create(request):
	editing = False
	order_save = None
	try:
		'''
			Some validation here..
				Disable edit:
					Complete,Completed,Cancelled
		'''

		postdata = post_data(request)

		user_type = request.user.user_type
		if user_type.code == "client":
			postdata["client"] = request.user.id

		postdata = clean_obj(postdata)
		if not postdata.get("order_number",None):
			postdata["order_number"] = get_reference_no(postdata.get("client"))

		try:
			instance = Order.objects.get(id = postdata.get("id",None))
			form = Order_create_form(postdata,instance = instance)
			editing = True
		except Exception as e:
			form = Order_create_form(postdata)

		postdata = clean_obj(postdata)
		if form.is_valid():
			order_save = form.save()
			if not order_save.status:
				status_data = {
					"order": order_save.pk,
					"status": "active",
				}
				update_status(request,status_data)

			print(order_save)
			print(order_save.is_deleted)
			print(order_save.client)
			print(order_save.status)
			return success("Order # %s successfully saved."%(order_save.order_number))
		else:
			raise_error(form.errors,True)

	except Exception as e:
		if not editing and order_save:
			order_save.delete(True)

		return error(e)

def load_to_edit(request,pid):
	try:
		try:
			filters = {"id": pid}
			user_type = request.user.user_type
			if user_type.code == "client":
				filters["client"] = request.user.pk

			instance = Order.objects.get(**filters)
			record = instance.as_dict()
			return success_list(record,False)
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)



def read_pagination(request,from_export = False,filters = {}):
	try:
		if not from_export:
			filters = post_data(request)
			pagination = filters.pop("pagination",None)
		
		sort_by = generate_sorting(filters.pop("sort",None))

		filters["status"] = filters.pop("status","active")
		filters.update({"is_deleted" : False})

		user_type = request.user.user_type
		if user_type.code == "client":
			filters["client"] = request.user.pk
		if user_type.code == "cda":
			filters["current_assignee"] = request.user.pk



		filters = clean_obj(filters)
		success_filter = copy.copy(filters)
		success_filter["status"] = "completed"


		name_search = filters.pop("name","")
		filters = filter_obj_to_q(filters)
		filters &= (Q(order_number__icontains=name_search) | Q(address__icontains=name_search))

		results = {"data" : []}
		records = Order.objects.filter(filters).order_by(*sort_by)



		# Count completed
		success_filter.pop("name","")
		results["success_count"] = Order.objects.filter(**success_filter).count()
		
		if not from_export:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		for record in records:
			record.update_time()
			row = record.as_dict(True)
			row["qc_count"] = record.count_qc()
			row["notes_count"] = record.count_notes()
			row["docs_count"] = record.count_docs()
			row["photo_count"] = record.count_photos()

			row["assignee"] = "Unassigned"
			if record.assigned:
				row["assignee"] = record.current_assignee.as_dict()

			results["data"].append(row)

		if from_export:
			return results
		return success_list(results,False)
	except Exception as e:
		return error(e)

def update_status(request,data = None):
	try:
		try:
			if not data:
				postdata = post_data(request)
			else:
				postdata = data

			postdata["status"] = postdata.get("status","active")
			postdata["changed_by"] = request.user.pk
			filters = {
				"id": postdata.get("order",None),
			}
			order_instance = Order.objects.get(**filters)


			order_status_history_form = Order_status_history_form(postdata)
			if order_status_history_form.is_valid():
				save = order_status_history_form.save()
				order_instance.update_status()
				if data:
					return True
				return success("Status successfully changed.")
			else:
				raise_error(order_status_history_form.errors,True)
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		dprint(e)
		return error(e)



# Order assignment

# class Order_assignment_history(models.Model):
# 	order = models.ForeignKey("Order")
# 	assigned_by = models.ForeignKey("User",related_name = "Assigned_by")
# 	assignee = models.ForeignKey("User",related_name = "Assignee")
# 	date = models.DateTimeField(auto_now_add = True)
# 	remarks = models.TextField()

def set_assignee(request,pid = None):
	try:
		try:
			instance = Order.objects.get(id = pid)
			params = post_data(request)

			assignee = params.get("assignee",None)
			print(assignee)
			if assignee:
				form_data = {
					"order": instance.pk,
					"assigned_by": request.user.pk,
					"assignee": assignee.get("id"),
				}
				order_assignment_history_form = Order_assignment_history_form(form_data)
				if order_assignment_history_form.is_valid():
					order_assignment_history_save = order_assignment_history_form.save()
					instance.assigned = True
					instance.current_assignee = order_assignment_history_save.assignee
				else:
					raise_error(order_assignment_history_form.errors,True)
			else:
				instance.assigned = False
				instance.current_assignee = None

			print(instance.current_assignee)
			instance.save()
			return success()
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)

def get_assignee(request,pid = None):
	try:
		try:
			instance = Order.objects.get(id = pid)
			assignee = instance.current_assignee.as_dict() if instance.current_assignee else None
			if assignee:
				assignee["assigned"] = True

			return success_list(assignee,False)
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)


def read_order_assignment_history(request,pid = None):
	try:
		try:
			instance = Order.objects.get(id = pid)

			results = []
			records = instance.get_assignment_histories()

			for record in records:
				results.append(record.as_dict())


			return success_list(results)
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)

# Order details
def order_details(request,pid = None):
	try:
		try:
			filters = {"id": pid}
			user_type = request.user.user_type
			if user_type.code == "client":
				filters["client"] = request.user.pk

			instance = Order.objects.get(**filters)
			status_histories,assignment_histories = instance.get_details()

			results = {
				"status_histories": list(list_dates_to_str(status_histories)),
				"assignment_histories": list(list_dates_to_str(assignment_histories)),
			}
			return success_list(results,False)
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)

#status history
def show_history(request,pid = None):
	try:
		try:
			filters = {"id": pid}
			user_type = request.user.user_type
			if user_type.code == "client":
				filters["client"] = request.user.pk

			instance = Order.objects.get(**filters)


			return success_list(instance.get_status_history())
		except Order.DoesNotExist:
			raise_error("Order number doesn't exists.")
	except Exception as e:
		return error(e)


# Notes
def read_notes(request,order_id):
	filters = {"order": order_id,"is_deleted": False}
	user_type = request.user.user_type
	if user_type.code == "client":
		filters["order__client"] = request.user.pk

	notes = Order_note.objects.filter(**filters).order_by("-id")
	records = []

	for note in notes:
		row = note.display_dict()
		row["editable"] = True if row["user_id"] == request.user.pk else False

		records.append(row)

	return success_list(records)

def create_note(request,order_id):
	try:
		try:
			data = post_data(request)
			filters = {"id": order_id}
			user_type = request.user.user_type
			if user_type.code == "client":
				filters["client"] = request.user.pk

			instance = Order.objects.get(**filters)
			data.update({"order": instance.pk,"created_by": request.user.pk})
			order_note_form = Order_note_form(data)
			if order_note_form.is_valid():
				order_note_instance = order_note_form.save()

			return success_list(order_note_instance.display_dict(),False)
		except Order.DoesNotExist:
			raise_error("Order ID not found.")
	except Exception as e:
		return error(e)

def delete_note(request,order_id,pid):
	try:
		try:
			data = post_data(request)

			filters = {"id": pid}
			user_type = request.user.user_type
			if user_type.code == "client":
				filters["client"] = request.user.pk

			instance = Order.objects.get(**filters)
			try:
				note_instance = Order_note.objects.get(id = pid)
				note_instance.is_deleted = True
				note_instance.save()
				return success("Note successfully deleted.")
			except Order_note.DoesNotExist:
				raise_error("Note not found.")
		except Order.DoesNotExist:
			raise_error("Order not found.")
	except Exception as e:
		return error(e)