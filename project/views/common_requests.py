from ..models.users import *
from ..views.common import *
from django.contrib.auth import authenticate, hashers, logout as logoutt

# Common template
def firstpage(request):
	return render(request, 'firstpage.html')


def pagination(request):
	return render(request, 'common/pagination.html')

def logout(request):
	"""Logs out the user and redirects them to the login page."""
	logoutt(request)
	return redirect("firstpage")