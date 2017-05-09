from ..forms.miscellaneous import *
from ..models.miscellaneous import *
from ..views.common import *


def credentials(request):
	return render(request, 'settings/credentials.html',{"page_name": "Settings"})

def credentials_create_dialog(request):
	return render(request, 'settings/dialogs/credentials_create_dialog.html')


def create_credentials(request):
	try:
		postdata = post_data(request)

		try:
			instance = Credential.objects.get(id = postdata.get("id",None))
			form = Credential_form(postdata,instance = instance)
		except Exception as e:
			form = Credential_form(postdata)

		postdata["user"] = request.user.id
		postdata = clean_obj(postdata)
		if form.is_valid():
			form_save = form.save()
		else:
			raise_error(form.errors,True)

		return success()
	except Exception as e:
		return error(e)

def delete_credentials(request,pid):
	try:
		try:
			instance = Credential.objects.get(id = pid,user = request.user.pk)
			instance.delete()
			return success()
		except Credential.DoesNotExists:
			raise_error("Credential doesn't exists.")
	except Exception as e:
		return error(e)