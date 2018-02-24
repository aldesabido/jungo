from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'', include('project.urls')),
    url(r'^superradmin/', admin.site.urls),
]
