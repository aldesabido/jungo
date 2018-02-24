from ..models.users import *
from ..views.common import *

# Common template
def firstpage(request):
	return render(request, 'firstpage.html')


def pagination(request):
	return render(request, 'common/pagination.html')