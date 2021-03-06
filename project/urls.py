
from django.conf.urls import url, handler404,include
from django.conf import settings as root_settings
from django.conf.urls.static import static

from project.views import (
		common,
		common_requests,
	)
urlpatterns = [
	url(r'^$', common_requests.firstpage, name='firstpage'),
	url(r'^logout/', common_requests.logout, name='logout'),
]
urlpatterns += static(root_settings.STATIC_URL,document_root=root_settings.STATIC_ROOT)
urlpatterns += static(root_settings.MEDIA_URL,document_root=root_settings.MEDIA_ROOT)
