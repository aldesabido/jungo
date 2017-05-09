
from django.conf.urls import url, handler404,patterns,include
from django.conf import settings as root_settings
from django.conf.urls.static import static

from project.views import (
		index,
		settings,
		common,
		common_requests,
		users,
		reports,
	)

from project.views.orders import (
		orders,photos,notes,documents
	)


urlpatterns = [
	url(r'^$', index.landingpage,name="landingpage"),
	url(r'^login/$', index.loginpage,name="loginpage"),
	url(r'^login/submit/$', index.login),
	url(r'^logout/$', index.logout),
	url(r'^register/create_dialog/$', index.registration_dialog),
	url(r'^register/$', index.register),


	#Common Requests & Common templates
	url(r'^common/pagination/$', common_requests.pagination),
	url(r'^common_requests/read_companies/$', common_requests.read_companies),
	url(r'^common_requests/read_credentials/$', common_requests.read_credentials),
	url(r'^common_requests/read_order_types/$', common_requests.read_order_types),
	url(r'^common_requests/read_clients/$', common_requests.read_clients),
	url(r'^common_requests/read_cdas/$', common_requests.read_cdas),



	url(r'^home/$', index.home,name="home"),
	url(r'^dashboard/$', index.dashboard),


	#Orders
	url(r'^orders/$', orders.orders),
	url(r'^orders/create_dialog/$', orders.create_dialog),
	url(r'^orders/create_dialog/(?P<pid>[0-9]+)/$$', orders.create_dialog),
	url(r'^orders/create/$$', orders.create),
	url(r'^orders/load_to_edit/(?P<pid>[0-9]+)$$', orders.load_to_edit),
	url(r'^orders/read_pagination/$', orders.read_pagination),
	url(r'^orders/update_status/$', orders.update_status),
	url(r'^orders/order_details/(?P<pid>[0-9]+)$', orders.order_details),
	url(r'^orders/order_details_dialog/$', orders.order_details_dialog),
	url(r'^orders/show_history/(?P<pid>[0-9]+)$', orders.show_history),
	url(r'^orders/order_status_history_dialog/$', orders.order_status_history_dialog),
	url(r'^orders/credential_dialog/$', orders.credential_dialog),

	#Order assignments
	url(r'^orders/order_assignment_dialog/$', orders.order_assignment_dialog),
	url(r'^orders/get_assignee/(?P<pid>[0-9]+)$', orders.get_assignee),
	url(r'^orders/set_assignee/(?P<pid>[0-9]+)$', orders.set_assignee),
	url(r'^orders/order_assignment_history_dialog/$', orders.order_assignment_history_dialog),
	url(r'^orders/read_order_assignment_history/(?P<pid>[0-9]+)$', orders.read_order_assignment_history),


	# Notes
	url(r'^orders/notes_dialog/$', orders.notes_dialog),
	url(r'^orders/read_notes/(?P<order_id>[0-9]+)$', orders.read_notes),
	url(r'^orders/create_note/(?P<order_id>[0-9]+)$', orders.create_note),
	url(r'^orders/delete_note/(?P<order_id>[0-9]+)/(?P<pid>[0-9]+)$', orders.delete_note),

	# Photos
	url(r'^orders/photos_dialog/$', photos.photos_dialog),
	url(r'^orders/upload/(?P<order_id>[0-9]+)/$', photos.upload),
	url(r'^orders/photos_read/(?P<order_id>[0-9]+)/$', photos.read),
	url(r'^orders/photos_remove/(?P<order_id>[0-9]+)/(?P<pid>[0-9]+)/$', photos.remove),
	url(r'^orders/photo_download/(?P<order_id>[0-9]+)/(?P<pid>[0-9]+)/$', photos.download),
	url(r'^orders/photo_batch_download/(?P<order_id>[0-9]+)/$', photos.batch_download),

	# Documents
	url(r'^orders/docs_dialog/$', documents.docs_dialog),
	url(r'^orders/docs_read/(?P<order_id>[0-9]+)/$', documents.read),
	url(r'^orders/docs_remove/(?P<order_id>[0-9]+)/(?P<pid>[0-9]+)/$', documents.remove),
	url(r'^orders/docs_upload/(?P<order_id>[0-9]+)/$', documents.upload),
	url(r'^orders/docs_download/(?P<order_id>[0-9]+)/(?P<pid>[0-9]+)/$', documents.download),
	url(r'^orders/docs_batch_download/(?P<order_id>[0-9]+)/$', documents.batch_download),





	#Settings
	url(r'^settings/$', settings.credentials),
	url(r'^credentials/create_dialog/$', settings.credentials_create_dialog),
	url(r'^credentials/create/$', settings.create_credentials),
	url(r'^credentials/delete/(?P<pid>[0-9]+)/$', settings.delete_credentials),


	#Settings
	url(r'^users/$', users.home),
	url(r'^users/create_dialog/$', users.create_dialog),
	url(r'^users/change_password_dialog/$', users.change_password_dialog),
	url(r'^users/change_password/$', users.change_password),
	url(r'^users/read_pagination/$', users.read_pagination),
	url(r'^users/load_to_edit/(?P<pid>[0-9]+)$$', users.load_to_edit),
	url(r'^users/delete/(?P<pid>[0-9]+)/$', users.delete),

	#Settings
	url(r'^reports/$', reports.home),
]
urlpatterns += static(root_settings.STATIC_URL,document_root=root_settings.STATIC_ROOT)
urlpatterns += static(root_settings.MEDIA_URL,document_root=root_settings.MEDIA_ROOT)
