from ..models.users import *
from ..models.orders import *
from ..models.miscellaneous import *
from ..views.common import *


# Common template
def pagination(request):
	return render(request, 'common/pagination.html')



# Common Requests
def read_companies(request):
	try:
		companies = Company.objects.filter(is_deleted = False).values("id","name")
		return success_list(list(companies))
	except Exception as e:
		return error(e)

def read_credentials(request):
	try:
		params = post_data(request)
		params["is_deleted"] = False

		user_type = request.user.user_type
		if user_type.code == "client":
			params["user"] = request.user.id


		if not params.get("user",None):
			return success_list([])

		params = clean_obj(params)

		credentials = Credential.objects.filter(**params)
		records = []
		for credential in credentials:
			records.append(credential.as_dict())
		return success_list(records)
	except Exception as e:
		return error(e)

def read_order_types(request):
	try:
		records = Order_type.objects.filter(is_deleted = False).values("id","name")
		return success_list(list(records))
	except Exception as e:
		return error(e)

def read_clients(request):
	try:
		records = User.objects.filter(
			deleted = False,
			is_active = True,
			user_type__code = "client"
		).values("id","email","fullname")

		return success_list(list(records))
	except Exception as e:
		return error(e)

def read_cdas(request):
	try:
		records = User.objects.filter(
			deleted = False,
			is_active = True,
			user_type__code__iexact = "cda"
		).values("id","email","fullname")
		
		return success_list(list(records))
	except Exception as e:
		return error(e)


