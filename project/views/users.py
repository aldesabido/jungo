from ..forms.users import *
from ..models.users import *
from ..models.miscellaneous import *
from ..views.common import *


def home(request):
	return render(request, 'users/users.html',{"page_name": "Users"})

def create_dialog(request):
	return render(request, 'users/dialogs/create_dialog.html')

def change_password_dialog(request):
	return render(request, 'users/dialogs/change_password_dialog.html')

def change_password(request):
	try: 
		params = post_data(request)
		try:
			instance = User.objects.get(id = params.get("id",None))
			# params.update(model_to_dict(inventory,fields = ["email","fullname","user_type",]))
			# print(params)
			user_form = Users_change_password_form(params,instance = instance)
		except Exception as e:
			raise_error("Record not found.")

		if user_form.is_valid():
			user_save = user_form.save()
			return success()
		else:
			raise_error(user_form.errors,True)

	except Exception as err:
		return error(err)


def load_to_edit(request,pid):
	try:
		try:
			filters = {"id": pid}
			instance = User.objects.get(**filters)
			record = instance.as_dict()
			print(instance)
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
		filters.update({"deleted" : False})


		user_type = filters.pop("user_type","client")
		print(user_type)
		user_type = User_type.objects.get(code__iexact = user_type)
		filters["user_type"] = user_type.pk
		filters = clean_obj(filters)

		name_search = filters.pop("name","")
		filters = filter_obj_to_q(filters)
		filters &= (Q(fullname__icontains=name_search) | Q(email__icontains=name_search))

		results = {"data" : []}
		records = User.objects.filter(filters).order_by(*sort_by)

		if not from_export:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		for record in records:
			row = record.as_dict()
			results["data"].append(row)

		if from_export:
			return results
		return success_list(results,False)
	except Exception as e:
		return error(e)

def delete(request,pid):
	try:
		try:
			instance = Credential.objects.get(id = pid,user = request.user.pk)
			instance.delete()
			return success()
		except Credential.DoesNotExists:
			raise_error("Credential doesn't exists.")
	except Exception as e:
		return error(e)